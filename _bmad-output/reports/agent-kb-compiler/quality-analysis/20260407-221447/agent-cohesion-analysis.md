# Agent Cohesion & Alignment Analysis — agent-kb-compiler

## Assessment

Cartographer is a cohesive, well-purposed agent. The persona (synthesizer who thinks in connections) aligns strongly with the capabilities (compile, manage concepts, write connections, maintain structure). The wiki compilation domain is well-understood and reflected throughout — from the CREED's core values to the specific YAML frontmatter fields in capability templates. The agent feels authentic: it has a point of view, not just a function list. The one notable gap is the absence of a search/retrieval capability — the agent can build the wiki but cannot help the owner navigate or query it.

## Cohesion Dimensions

### 1. Persona-Capability Alignment: Strong

The Cartographer identity ("synthesizer who thinks in connections," "every new source is an opportunity to strengthen the web") maps cleanly to each capability:
- **Compile Sources** → the practical act of synthesis
- **Manage Concepts** → building the conceptual framework
- **Write Connections** → the highest expression of the synthesizer identity
- **Maintain Wiki** → the stewardship role

The CREED reinforces this: "Connections are the product," "Let structure emerge," "Synthesis over aggregation." These values are reflected in the Operations within each capability prompt (e.g., manage-concepts.md's Merge/Split operations, write-connections.md's taxonomy of connection types).

### 2. Capability Completeness: Moderate

The core compilation workflow is fully covered. What's missing:

- **Search/Query** — the agent can build a wiki but can't help the owner find things in it. "What do I know about X?" is a natural question for any knowledge base user. This is a meaningful gap.
- **Source Ingest** — `compile-sources.md` reads from `raw/` but assumes sources are already there. There's no capability to add a URL, file, or paste to `raw/` and register it in the source index. The agent references "ingest agent's domain" in CREED Dominion (Deny Zones), suggesting this is intentionally out of scope, but it's worth noting.
- **Export/Output** — the agent builds a wiki but has no capability for extracting structured output from it (e.g., "generate a reading list for concept X," "export a summary of my research on Y"). `outputs/` is mentioned in Deny Zones, again suggesting intentional scope limitation.

### 3. Redundancy Detection: Strong (No Redundancies)

The four capabilities are cleanly differentiated:
- CS operates on raw → summaries
- MC operates on summaries → concept articles
- WC operates on concepts/summaries → connection articles
- MW operates on the entire wiki → structural integrity

These form a natural pipeline with no overlap. The Operations list within MC (Create, Update, Promote, Merge, Split, Inventory) and MW (Rebuild index, Check links, Update backlinks, Reorganize, Stats) are distinct and non-redundant.

### 4. External Skill Integration: Neutral

No external skill references detected in the agent. The CAPABILITIES-template.md mentions "User-Provided Tools" (MCP servers, APIs) and first-breath.md asks about web search and image generation tools. The agent is designed to be self-contained with optional tool augmentation — appropriate for its purpose.

### 5. Capability Granularity: Strong

The four capabilities are at the right level of abstraction. Each represents a meaningful work unit:
- CS handles a batch of sources in one session
- MC handles the concept layer
- WC produces insight articles
- MW handles structural health

Not too granular (no separate "Create concept" vs "Update concept" capabilities — these are Operations within MC). Not too broad (wiki maintenance is separate from content creation).

### 6. User Journey Coherence: Moderate

**A new user's journey:**
First Breath → establish identity and vault path → compile first sources (CS) → concepts emerge → create concept articles (MC) → discover connections → write connection articles (WC) → periodic wiki maintenance (MW)

This is a coherent loop. The journey works end-to-end for the core use case.

**Gap:** There's no re-entry journey for returning users. The "rebirth" path loads identity and then... waits. The owner has to know to say "compile new sources" or "manage concepts." There's no capability equivalent to "what should we work on today?" — no session planning or priority surfacing.

## Per-Capability Cohesion

| Capability | Fits Identity? | Unique Purpose? | Natural for this Agent? | Notes |
|-----------|----------------|-----------------|------------------------|-------|
| Compile Sources | Yes | Yes | Yes | Core function, well-aligned |
| Manage Concepts | Yes | Yes | Yes | Synthesis at the concept layer — perfectly on-brand |
| Maintain Wiki | Yes | Yes | Yes | Stewardship role fits the "living map" philosophy |
| Write Connections | Yes | Yes | Yes | The highest expression of the synthesizer identity |
| Capability Authoring | Yes | Yes | Yes | Meta-capability, appropriate for evolvable agent |

## Key Findings

**[Medium] Missing: Search/Query capability**
The agent builds a navigable wiki but provides no way to query it. "What have I compiled about machine learning?" or "What do I know about the relationship between X and Y?" are natural owner requests that the agent currently can't serve directly. The owner could ask freeform, but without a capability prompt, the agent has no guidance on how to answer (check MEMORY.md concept inventory? scan wiki/concepts/? use the index?).
Fix: Add a `[SQ] Search & Query` capability. Prompt: load the wiki index, check MEMORY.md concept inventory, then answer the question with references to relevant concept articles, summaries, and connections.

**[Low] Missing: Compilation planning / "what's next?" session opener**
After rebirth, the agent knows its identity and capabilities but has no guidance on how to propose what to work on. A returning owner with 5 new sources in `raw/` shouldn't have to remember to say "compile sources" — the agent should surface this proactively.
Fix: Add a note to the On Activation → Rebirth path or to `maintain-wiki.md`: "After rebirth, if the session has no stated agenda, check the source index for uncompiled sources and offer to begin."

**[Suggestion] Connection Hunting standing order is brilliant but passive**
The CREED has "Connection Hunting" as a standing order — always look for connections while compiling. This is excellent identity work. It could be made more active: when the agent surfaces a compelling connection candidate during compile, it could immediately draft a connection article stub rather than just adding to MEMORY.md.

**[Suggestion] The "Inventory" operation in manage-concepts.md is the strongest probe**
Running "Inventory" gives the owner a full picture of knowledge base coverage. This could be elevated to a first-class capability or included in every rebirth greeting: "Since last time: 3 new sources compiled, 2 concept stubs created, 1 connection identified."

## Strengths

- The four built-in capabilities form a genuine knowledge compilation pipeline — each stage feeds the next
- CREED core values are domain-specific and non-generic ("Synthesis over aggregation," "Connections are the product," "Obsidian-native")
- The synthesizer identity creates a consistent voice and decision framework across all capabilities
- `capability-authoring.md` enables the agent to grow — users can teach it new domain-specific capabilities
- The two-tier memory architecture (session logs → MEMORY.md curation) prevents memory bloat while preserving continuity
- Deny Zones in CREED clearly scope the agent's responsibilities, preventing drift into source ingestion or output generation

## Creative Suggestions

1. **The "What's Changed" rebirth hook:** On rebirth, the agent reads the source index, compares to MEMORY.md concept inventory, and opens with: "Welcome back. Since we last spoke: X new sources are waiting to be compiled, and there are Y connection candidates in your queue." Makes every session feel intentional.

2. **Connection Confidence scoring:** When writing connection articles, the agent could rate its own confidence in the connection (High/Medium/Speculative) and include this in the article frontmatter. Helps the owner distinguish solid synthesis from interesting hypotheses.

3. **Concept lifecycle dashboard:** A periodic "Inventory" session that produces a visual summary: how many stubs vs drafts vs mature articles, which concepts have the most sources, which are most heavily linked. Could be a natural output of MW "Stats" operation.
