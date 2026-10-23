# Private batch analysis · Reader 0.4

The installed Reader can analyze up to **16 explicitly named UTF-8 manuscripts**
without uploading them. This is a local report workflow, **not** corpus admission,
scientific FantLab parity or a public site dataset.

Create `manuscripts/manifest.json` next to the selected files:

```json
{"schema_version":"scriptorium-private-batch-manifest-v1",
 "files":["novel-one.txt","novel-two.txt","novel-one.txt"]}
```

Run from any directory after installing the Reader wheel:

```sh
scriptorium batch manuscripts/manifest.json --output-dir private-batch-output
```

The output directory is created with POSIX mode 0700; regular reports use 0600.
It must already have private permissions if reused. Python 3.13+ and POSIX
`O_NOFOLLOW`/directory-relative operations are required; other platforms
fail closed rather than silently claiming equivalent path-safety guarantees.
Input path components, the manifest itself and output destinations may not be symlinks.
Manifest file paths are relative to its directory. Traversal, implicit directory
discovery and absolute input paths are prohibited. Maximum 16 entries,
32 MiB per work and 64 MiB total; manifest at most 64 KiB.

For each distinct SHA-256 the Reader creates `work-<sha256>.json` and
`work-<sha256>.html`, then a `batch-<manifest-sha-prefix>.csv` and
`.html` index, committing its `.json` index **last**.
JSON report metrics use the existing `build_local_analysis()` and
its versioned profiles; no shadow analyzer or morphology substitution.
Duplicate input bytes share the same reports. Manifest entry order is preserved.
No manuscript bytes, private file names or absolute paths appear in the index.
Hashes can identify known works; share derived reports deliberately.

The exit code is **0** when every item succeeds, **1** if one or more
items fail (their rows say `error` and contain no metrics/routes), and **2**
for a rejected manifest, unsafe destination or publishing conflict.
Existing results and complete indexes are never overwritten. Identical
results are reused on retry; conflicting content is rejected. If interrupted,
rerun the same command: absent files are created without destroying existing
complete outputs. A partial run can leave a derived report without an index;
the final JSON index is the completion marker. Change the output directory
for new versions or different report settings. Indexed failures remain failures
until the input/manifest changes.

No secret path or manuscript text is printed in operational errors. Report
source hashes and aggregate metrics are not authenticated provenance.
Even long works need separate rights, source-identity and scientific
evidence for M2; short works have explicit representativeness limits.
