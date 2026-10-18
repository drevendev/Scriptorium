"""Atomic, no-clobber publication of an already-validated local static-site tree.

Linux renameat2 is intentionally required. Unsupported platforms fail closed rather
than removing the last valid published tree or silently changing a first publish into
an overwrite. This module does not activate GitHub Pages.
"""
from __future__ import annotations

from contextlib import contextmanager
import ctypes
import errno
from hashlib import sha256
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Iterator


_RENAME_NOREPLACE = 1
_RENAME_EXCHANGE = 2
_AT_FDCWD = -100


def _atomic_rename(source: Path, destination: Path, *, replacing: bool) -> None:
    if not sys.platform.startswith("linux"):
        raise OSError(errno.ENOTSUP, "atomic directory publication requires Linux renameat2")
    library = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(library, "renameat2", None)
    if renameat2 is None:
        raise OSError(errno.ENOTSUP, "atomic directory publication unavailable")
    renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    renameat2.restype = ctypes.c_int
    mode = _RENAME_EXCHANGE if replacing else _RENAME_NOREPLACE
    if renameat2(_AT_FDCWD, os.fsencode(source), _AT_FDCWD, os.fsencode(destination), mode):
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code))


@contextmanager
def staged_site(repo_root: Path, destination: Path) -> Iterator[Path]:
    """Yield a disposable staging directory and atomically publish on clean exit.

    The original directory survives rendering failures. An initially absent output
    never overwrites an output created by a competing process during rendering.
    """
    build_dir = repo_root / "build"
    if build_dir.is_symlink():
        raise OSError(errno.ELOOP, "build directory must not be a symlink")
    build_dir.mkdir(exist_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.parent.absolute() != destination.parent.resolve(strict=False):
        raise OSError(errno.ELOOP, "site destination cannot traverse symlinks")
    relative = destination.relative_to(repo_root)
    lock = build_dir / (".site-publish-" + sha256(relative.as_posix().encode()).hexdigest()[:20] + ".lock")
    # Keep a stable lock inode. An auto-released flock survives SIGKILL without
    # permanently stranding the publisher; unlinking it would introduce an inode race.
    if not sys.platform.startswith("linux"):
        raise OSError(errno.ENOTSUP, "atomic directory publication requires Linux")
    import fcntl  # Linux-only: keep the rest of the library importable elsewhere.
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError(errno.EINVAL, "site publication lock must be a regular file")
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise OSError(errno.EBUSY, "site publication already in progress") from exc
        replacing = destination.exists()
        with tempfile.TemporaryDirectory(prefix=".site-stage-", dir=build_dir) as temporary:
            stage = Path(temporary)
            yield stage
            if destination.is_symlink() or destination.absolute() != destination.resolve(strict=False):
                raise OSError(errno.ELOOP, "site destination cannot traverse symlinks")
            _atomic_rename(stage, destination, replacing=replacing)
    finally:
        os.close(fd)
