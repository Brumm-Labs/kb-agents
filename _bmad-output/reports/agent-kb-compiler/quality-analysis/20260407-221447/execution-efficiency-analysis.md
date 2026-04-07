# Execution Efficiency Analysis — agent-kb-compiler

## Assessment

The execution-deps pre-pass found zero issues — no dependency graph violations, no sequential patterns flagged, no circular dependencies, no subagent chain violations. For a memory agent of this scope, this is the expected and correct result. The agent's capabilities are largely sequential by domain necessity (read source → write summary → update index), and none of the prompts invoke subagents or delegate to parallel workers. Efficiency concerns are minor and architectural rather than structural.

## Pre-Pass Findings

**Total issues: 0** (status: pass)

No sequential patterns, no dependency cycles, no transitive redundancies, no parallel group opportunities were detected by the pre-pass script. The dependency graph is empty — stages, hard/soft dependencies, and parallel groups are all absent. This reflects that the capability prompts do not have explicit orchestration steps that could be analyzed for parallelization.

## Memory Loading Strategy

**Pattern: Memory agent (sanctum architecture)**

On Activation correctly routes to batch-load of 6 identity files on rebirth: `INDEX.md`, `PERSONA.md`, `CREED.md`, `BOND.md`, `MEMORY.md`, `CAPABILITIES.md`. This is correct and not wasteful — all 6 are needed for the agent to become itself. Session logs are NOT loaded on rebirth (correct). `memory-guidance.md` is loaded at session close via the Session Close directive.

The MEMORY.md template enforces a 200-line cap (noted in `references/memory-guidance.md`), which is a strong efficiency discipline — this ensures the sanctum identity batch-load stays bounded as the wiki grows.

Capability references (`compile-sources.md`, `manage-concepts.md`, etc.) are in `references/` and loaded on-demand when capabilities trigger — not at startup. This is the correct pattern.

## Key Findings

**[Medium] compile-sources.md:17-22 — Sequential source processing without parallelization guidance**

The Approach section instructs: "For each source, read the full content from `raw/`" then process it. If an owner has 10+ uncompiled sources, the agent will process them one at a time. For small batches (1-5) this is fine. For larger batches, parallel subagent delegation per source would be dramatically faster.

Current pattern:
```
1. Read source index to find uncompiled sources
2. For each source, read full content
3. Create or update a summary
4. Update source status
5. Update wiki index
```

Suggested pattern for 5+ sources:
- Delegate each source to a subagent (parallel): "Read `raw/{source}`, write summary to `wiki/summaries/{name}.md`, return the concept names identified"
- Parent aggregates: update source index statuses, update wiki index, note new concepts

Estimated savings: 50-70% latency reduction for batch compilations of 5+ sources. Token cost roughly neutral (same reads/writes, just parallel). **This is the highest-value efficiency improvement available.**

Fix: Add to `compile-sources.md`: "For batches of 5+ uncompiled sources, delegate each source to a parallel subagent. Each subagent should: (1) read the source, (2) write the summary file, (3) return the title, concepts identified, and new concept flags. Parent aggregates results to update the source index and wiki index."

**[Low] maintain-wiki.md — "Check links" operation is sequential by nature but could pre-extract**

The "Check links" operation (find broken `[[wiki-links]]` and orphaned files) asks the LLM to scan wiki files and identify broken links. This is a deterministic operation that a script could do faster and more reliably. This is primarily an intelligence-placement concern (flagged in script-opportunities), but it also creates unnecessary sequential file reads.

**[Low] manage-concepts.md — "Inventory" operation reads all concept files**

The Inventory operation ("list all concepts with their status and source count") would require reading every file in `wiki/concepts/`. For a large knowledge base (50+ concepts), this creates significant sequential reading. A pre-pass script that extracts frontmatter status and source count from all concept files would serve this much better.

## Optimization Opportunities

### Batch Compilation Parallelization (High Impact)

The `compile-sources.md` capability is the agent's primary workhorse. As the knowledge base grows, batch compilations of 10-20 sources will be common. The current sequential pattern will be the bottleneck for every large indexing session.

Adding a `{headless_mode}` or batch-size check to `compile-sources.md` that switches to parallel subagent delegation above a threshold (e.g., 5 sources) would make this agent dramatically more scalable.

Output contract for a compile subagent:
```json
{
  "source": "raw/filename.md",
  "summary_path": "wiki/summaries/filename.md",
  "concepts_identified": ["concept-a", "concept-b"],
  "new_concepts": ["concept-c"],
  "status": "compiled"
}
```

### Link Checking via Script (Medium Impact)

The "Check links" operation in `maintain-wiki.md` is deterministic. A Python script using pathlib and regex to extract all `[[wiki-links]]` from wiki files and verify their targets exist would be faster, more accurate, and free up context. See script-opportunities-analysis.md for detailed specification.

## What's Already Efficient

- 6-file batch load on rebirth is correctly parallel (single message with 6 reads)
- Capability reference files are demand-loaded, not startup-loaded
- `memory-guidance.md` is loaded only at session close — not on every activation
- MEMORY.md has a hard token cap (200 lines), preventing unbounded memory growth
- Session logs are NOT loaded on rebirth — raw material, not identity
- The agent doesn't pre-read files before delegating — each capability prompt loads its own context
