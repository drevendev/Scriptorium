# SCRIP-CORPUS-020 — frozen `poemx1` parser-control reachability

- Issue: #109
- Draft PR: #116
- Authored semantic head: `23b3152f8bf97decdcf95a0021c950682cfd4125`
- Status: `POEMX1_CONTROL_FLOW_AUTHORED_REVIEW_PENDING`
- Scope: corpus/provenance correctness; no FantLab source-match or M2 promotion.

## Bounded result

The six previously frozen `poemx1` calls share one exact source-free frame class: parameter `1` is defined empty, parameter `2` is defined non-empty, and `3`, `fixed`, `poem`, `small`, and `width` are omitted. PR #116 validates that frame against the pinned template/transclusion/parameter/binding manifests and resolves only the MediaWiki `#if` / `#ifeq` branches determined by those states.

From the pinned static graph (`#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1), the frozen frame reaches `#if` x4, `#ifeq` x3 and the single `#tag:poem`. Both `#expr` calls and the `#iferror` call are unreachable, as are one nested `#if` and two nested `#ifeq` occurrences. This means generic arithmetic/error-function emulation is not a prerequisite for these six calls and must not be manufactured solely from the static inventory.

The committed source-free evidence is `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-template.control.json`. It records frame states, invocation SHA-256 identities, branch decisions, reachable/unreachable construct counts and the remaining live extension operation without committing literary argument text.

## Evidence boundary

Current official MediaWiki ParserFunctions documentation confirms that `#if` treats empty/whitespace-only input as false, ParserFunctions trim leading/trailing whitespace, and non-numeric `#ifeq` operands compare as case-sensitive text. MediaWiki magic-word documentation identifies `#tag` as the alias for XML-style parser/extension tags and notes that tag calls in unselected conditional paths are not parsed.

This bounded slice does **not** recursively expand parameter `2`, render the live `#tag:poem`, prove historical render equivalence, freeze resolved Part 2 bytes, define the four-part literary-body extraction/composition contract, or advance the unknown FantLab source identity.

## Verification

Exact semantic head `23b3152f8bf97decdcf95a0021c950682cfd4125` completed successfully on workflows `35273911005` (new poemx1 control replay), `35273911132` (invocation bindings), `35273911079` (historical template dependency), `35273911025` (Klim source revisions), `35273911000` (Pages), and `35273911044` (frozen diagnostic). The dedicated control job checked out the exact head, ran the full standard-library suite, regenerated the new manifest from committed prerequisite evidence and byte-compared it to the committed artifact. PR #116 remains Draft for independent later-run review.

## Next trigger

Independently review PR #116. If clean, merge it without closing #109. The next implementation layer is only the one live path: recursive expansion of parameter `2` as required by `#tag:poem` plus evidenced historical `<poem>` extension behavior. Resolved Part 2 remains forbidden until that path replays deterministically.
