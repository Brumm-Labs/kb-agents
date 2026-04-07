# Enhancement Opportunities Analysis — agent-kb-compiler

## Agent Understanding

Cartographer is a memory agent that transforms raw research sources into a structured, navigable wiki — creating summaries, concept articles, connection analyses, and maintaining the overall structure using Obsidian wiki-links. The primary user is a researcher or knowledge worker who ingests sources regularly and wants to build a coherent understanding of their domain over time. The key assumption: sources already exist in `raw/` and the owner initiates sessions knowing what they want to work on.

## User Journeys

### The First-Timer

**Narrative:** A graduate student who's been bookmarking papers for months wants to finally organize them into something navigable. They hear about this agent and activate it for the first time.

**Friction points:**
- First Breath is warm and well-designed, but it asks about vault location, source depth, concept preferences, writing style, and workflow preferences before the owner has seen any output. They don't know what "preferred summary depth" means yet.
- The agent never shows them an example of what a compiled wiki looks like. A sample summary or concept article in the first breath would help.
- After First Breath, they're handed capabilities but have no concrete "here's what to do first."

**Bright spots:** Urgency detection is excellent — if they arrive with "I have 10 papers to compile," the agent gets to work immediately. "Save As You Go" means a cut-short first conversation isn't wasted.

**Suggestion:** Add a "Show Me An Example" moment in First Breath. After the owner describes their domain, the agent could say: "Here's what a compiled summary for a paper like that might look like..." — then show a brief example using their described domain. This grounds their preferences in something concrete.

### The Expert

**Narrative:** A researcher who has been using the wiki for 6 months. They have 40 compiled sources, 25 concept articles, and a rich connections map. They open a session and want to do deep synthesis work.

**Friction points:**
- Rebirth loads identity correctly, but then waits. The expert has to recall which capability to invoke.
- No capability for querying the existing wiki. "What do I currently understand about embodied cognition?" requires manually browsing wiki files rather than asking the agent.
- The "Inventory" operation gives counts but not prioritization. The expert can't easily ask "which concepts have the most open questions?" or "which connection candidates in my queue are most promising?"

**Bright spots:** The connection types taxonomy (Convergence, Contradiction, Evolution, Pattern, Comparison) is exactly what a sophisticated researcher needs — it gives them language to request specific types of synthesis.

**Suggestion:** Add a rebirth continuation hook: after loading identity, if no immediate request, the agent proactively surfaces: pending uncompiled sources (from source index), connection candidates from MEMORY.md, and concept stubs that need enrichment. Turns passive rebirth into active session planning.

### The Confused User

**Narrative:** Someone who activated this agent thinking it would help them brainstorm or take notes. They want to "organize their thoughts" but don't have structured raw sources.

**Friction points:**
- The agent assumes sources exist in `raw/`. A user without a structured `raw/` folder is immediately lost.
- First Breath asks about vault location early, but a confused user might not have an Obsidian vault at all.
- There's no "you might be looking for a different kind of agent" redirect.

**Bright spots:** The urgency detection gives the confused user a path — they can try to use the agent and it will help them figure out what they actually need.

**Suggestion:** Add an early disambiguation check in First Breath: "Do you have raw source files ready to compile, or are you starting from scratch?" This opens two paths: the current configuration flow (sources exist) or a quick "here's what you need to set up first" explanation.

### The Edge-Case User

**Narrative:** A researcher whose knowledge base is in Notion, not Obsidian. They want the synthesis capabilities but Obsidian `[[wiki-links]]` don't apply to their setup.

**Friction points:**
- The agent is deeply Obsidian-specific — wiki-links, graph view, Obsidian frontmatter. This is in the CREED as a core value ("Obsidian-native").
- First Breath asks how they browse (graph view, search, index) but doesn't ask what tool they use.
- There's no graceful adaptation path for non-Obsidian wikis.

**Suggestion:** Add a tool-detection question in First Breath: "What are you using for your wiki? Obsidian, Notion, plain markdown?" If non-Obsidian, note in BOND.md and adapt link format accordingly. The synthesis capabilities work the same — only the link syntax changes.

### The Hostile Environment

**Narrative:** The owner's vault is large (500+ files), sources are in inconsistent formats, the source index is out of date, and some raw files are PDFs or web captures rather than clean markdown.

**Friction points:**
- `compile-sources.md` reads `raw/_source-index.md` first — if this file is missing or malformed, the capability has no starting point.
- No handling for sources that aren't markdown (PDFs, HTML captures, images).
- No graceful path if a concept article write fails (disk full, permission error, etc.).

**Suggestion:** Add fallback to `compile-sources.md`: "If the source index doesn't exist or is empty, offer to scan `raw/` directly to discover unindexed sources and create/repair the index." This makes the agent resilient to the most common setup failure.

### The Automator

**Narrative:** A CI pipeline that runs nightly: new papers added to `raw/` by a scraper, and the wiki should automatically update with new summaries and concept links.

**Friction points:**
- Headless mode is declared (`--headless` → load PULSE.md from sanctum) but PULSE-template.md doesn't exist. The headless path is broken.
- Even if PULSE existed, compile-sources.md requires reading the source index and making judgment calls about concept linking — this works headlessly, but the agent needs a clear "auto-compile all new sources" contract.
- No structured output (JSON or log) from headless compilation that the CI system could parse.

**Headless assessment:** Easily adaptable. The core compilation workflow (read source, write summary, update index) is deterministic enough to work headlessly. What's needed: a PULSE.md that wakes up, checks for uncompiled sources, compiles them all, and exits with a structured log.

## Headless Assessment

**Level: Easily Adaptable**

Compile Sources, Maintain Wiki, and Manage Concepts (Inventory operation) could all work headlessly today with minimal changes:

- What headless would need: PULSE.md specifying the autonomous task (check for new sources, compile them, update the index, write session log)
- What inputs it needs upfront: vault path (from config), sanctum path
- What it would return: a session log with count of sources compiled, concepts created/updated, connection candidates spotted
- Which operations need human input even headlessly: Write Connections (judgment-heavy) and First Breath (obviously)

**Critical blocker:** `PULSE-template.md` doesn't exist. The `--headless` path in On Activation loads PULSE.md from the sanctum, but it's never created. This means headless mode silently fails.

## Key Findings

**[High-Opportunity] Create PULSE-template.md for headless compilation**
Headless mode is declared but non-functional. The most natural autonomous task for Cartographer is: wake up, compile all new sources, write a session summary, exit. This would allow cron-based wiki updates when new sources arrive.
Suggestion: Create `assets/PULSE-template.md` with a task: scan source index for uncompiled sources, run compile-sources flow for each, write session log, note connection candidates identified.

**[High-Opportunity] Add Search/Query capability**
The agent builds a navigable wiki but can't help the owner navigate it. "What do I know about X?" is one of the most natural questions for a researcher. Without a query capability, the wiki's value is only realized when the owner browses it manually.
Suggestion: `[SQ] Search & Query` — loads MEMORY.md concept inventory, scans wiki index, answers questions with referenced concept articles and summaries.

**[Medium-Opportunity] Add "What's Next" rebirth hook**
After rebirth, the agent has its identity but no agenda. Proactively surfacing: uncompiled source count, connection queue, stub count — would make every session intentional without requiring the owner to remember what to ask for.
Suggestion: Add to On Activation rebirth path: "Check source index for uncompiled count. Check MEMORY.md for connection candidates. Open with a brief status and offer to begin."

**[Medium-Opportunity] Show-an-example in First Breath**
First-time users are asked about preferences they haven't developed yet. A brief "here's what output looks like" moment in First Breath anchors the discovery conversation in concrete reality.
Suggestion: After the owner describes their domain, generate a 3-sentence sample summary in their stated style before asking further questions.

**[Medium-Opportunity] Source index resilience**
`compile-sources.md` assumes `raw/_source-index.md` exists. If it doesn't, the capability has no starting point. A fallback (scan `raw/` directly) would make the agent robust to the most common setup issue.

**[Low-Opportunity] Concept status visualization**
The manage-concepts.md "Inventory" operation lists concepts but doesn't visualize coverage. A formatted output showing stub/draft/mature counts, most-linked concepts, and concepts with open questions would give the owner a strategic view of their knowledge base.

**[Low-Opportunity] Soft gate elicitation in First Breath**
First Breath asks questions in four groups (Knowledge Base, Wiki Preferences, Writing Style, Workflow). These are presented as lists within groups. Adding soft gates ("Does that cover the basics for now, or is there something important I'm missing?") after each group would draw out information the owner didn't know they had.

## Top Insights

1. **Headless mode is declared but broken.** The `--headless` routing exists in On Activation but PULSE-template.md doesn't exist. This is the highest-priority fix — it blocks an entire class of automation use cases (nightly wiki updates, CI integration) that are perfectly suited to this agent.

2. **The agent builds knowledge it can't retrieve.** Cartographer creates a rich wiki but has no query capability. This is a meaningful gap for researchers who want to ask "what do I currently understand about X?" The agent is write-only from the owner's question-asking perspective.

3. **First Breath asks for preferences before the user has seen outcomes.** "How deep should summaries be?" is hard to answer without seeing an example summary. A brief demonstration moment mid-First Breath would dramatically improve the quality of the preferences captured — and create a memorable "aha" moment at the start of the relationship.

## Facilitative Patterns Check

| Pattern | Present? | Assessment |
|---------|---------|------------|
| Soft Gate Elicitation | Partial | First Breath uses question groups but no explicit "anything else or move on?" gates |
| Intent-Before-Ingestion | Yes | Urgency Detection and "What to Achieve" section exist |
| Capture-Don't-Interrupt | Not assessed (text conversation) | Not applicable for this agent's interaction style |
| Dual-Output | Missing | Agent produces wiki articles but no LLM-optimized distillate for downstream agents |
| Parallel Review Lenses | Missing | Write Connections capability has no multi-perspective review before finalizing |
| Three-Mode Architecture | Missing | Only one interaction style — could benefit from Guided (interview-style) vs Yolo (auto-compile all) modes |
| Graceful Degradation | Partial | No subagent use currently, so no degradation needed — but compile-sources has no fallback for missing source index |

**Highest value pattern to add:** Dual-Output for `write-connections.md`. Connection articles are high-synthesis outputs that often feed downstream — into presentations, papers, or other agents. Offering a token-efficient distillate (thesis + key evidence in compact format) alongside the full article would enable downstream consumption.
