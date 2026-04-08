# Enhancement Opportunities Analysis — agent-kb-linter

**Scanner:** DreamBot v1.0 | **Date:** 2026-04-07 | **Agent type:** Memory agent (Inspector)

---

## Agent Understanding

Inspector is a knowledge base quality auditor with persistent memory — it learns which findings the owner cares about, suppresses recurring false positives, and tracks quality trends over time. The primary user is a solo knowledge worker or researcher who maintains a personal wiki with a `raw/` + `wiki/` + `outputs/` structure. The core assumption is that the user actively maintains their wiki and wants Inspector to be a recurring partner, not a one-shot tool.

---

## User Journeys

### The First-Timer
**Narrative:** Arrives with a messy wiki, has heard about "linting" but isn't sure what to expect. Invokes Inspector for the first time.

**First Breath experience:** Strong. Urgency detection is present — if they say "my wiki is a mess, help," Inspector should run a health check first. The discovery questions are well-organized. No friction on entry.

**Friction point:** The First Breath asks about vault path, wiki maturity, and quality priorities — but doesn't help the user understand what "good" looks like before they answer. A first-timer may not know if their wiki is "mature" or what "pedantic vs. pragmatic" checking means. The agent would benefit from a brief orientation: "Here's what I can check, here's what matters most for most people — does that match your situation?"

**Bright spot:** "Make sure they know they can teach you new checks anytime" — this framing is welcoming and positions Inspector as a collaborator, not a fixed tool.

### The Expert
**Narrative:** Power user, maintains a 300-article wiki, runs health checks quarterly. Wants fast results without ceremony.

**Friction point:** Inspector has no fast-path invocation. Every health check goes through the same discovery flow even after rebirth. An expert who types "HC" expects immediate execution, not a preamble. The HC capability correctly has a "What Success Looks Like" outcome definition, but doesn't specify an explicit fast-path when the owner is a known repeat user (BOND.md exists, preferences known).

**Suggestion:** Add to health-check.md: "If BOND.md exists and vault path is known, begin scanning immediately without preamble. Present findings when complete."

**Bright spot:** The memory system means Inspector already knows their false-positive patterns. Second and subsequent runs should feel dramatically faster than the first.

### The Confused User
**Narrative:** Invoked Inspector by accident while asking about their wiki. Actually wants to write a new article, not audit the existing ones.

**Gap:** Inspector has no graceful "that's not what I do" redirect. If a user says "help me write an article about X," Inspector currently has no path except to explain it can't help — there's no suggestion of what agent could. A simple redirect ("I'm a quality auditor — if you want to write new content, [skill] might be more useful, but I can tell you what the wiki currently says about X first") would prevent dead-ends.

**Suggestion:** Add a brief off-scope redirect pattern to CREED.md standing orders or SKILL.md.

### The Edge-Case User
**Narrative:** Uses a non-standard wiki structure — no `raw/` folder, everything in a flat `notes/` directory. Inspector's health-check references specific paths (`raw/`, `wiki/`, `outputs/`).

**Gap:** Inspector assumes a specific vault structure. If the owner's wiki doesn't have the `raw/` + `wiki/` split, several checks (uncompiled sources, source index sync) will either fail or produce false positives. First Breath asks for vault structure but the capability prompts don't adapt based on what was learned.

**Suggestion:** In health-check.md, add: "Check BOND.md for vault structure before running path-specific checks. If structure differs from defaults, adapt check categories accordingly."

### The Hostile Environment
**Narrative:** Wiki vault path is wrong (moved), or MEMORY.md has become corrupted, or the wiki is enormous (1000+ files) and the health check times out.

**Gap:** No graceful degradation for vault-not-found. Inspector would either error out or try to scan the wrong path. No fallback pattern is defined.

**Gap:** No guidance on what to do if MEMORY.md is over 200 lines (the token discipline limit in memory-guidance.md). Should the agent compress it? Alert the owner?

**Suggestion:** Add a "Vault not found" recovery path to health-check.md. Add a MEMORY.md bloat detection note to memory-guidance.md.

### The Automator
**Narrative:** A CI pipeline wants to run a weekly health check and post results to a dashboard. Wants headless invocation: no confirmation dialogs, structured JSON output.

**Current state:** Inspector declares a headless path (`--headless` → load PULSE.md) but PULSE-template.md doesn't exist. The headless mode is declared but not built.

**Gap:** Health-check produces markdown output (correct for human reading) but no structured/machine-readable output variant. A headless invocation that returns JSON (issue count by severity, list of broken links) would enable dashboard integration.

**Suggestion:** Create PULSE-template.md with a default autonomous action: run HC, write report to `outputs/health-{date}.md`, output JSON summary to stdout. This unlocks the automator use case completely.

---

## Headless Assessment

**Level: Easily adaptable** — Inspector's core value (health check, fix, suggest) is deliverable without human interaction if the owner's preferences are in BOND.md.

| Interaction Point | Auto-resolvable? | What's needed |
|------------------|-----------------|---------------|
| Vault path | Yes | Read from BOND.md |
| Which checks to run | Yes | Default: all structural; defer content to human |
| Fix confirmation | Partial | Auto-fix safe issues; skip "needs confirmation" |
| Report verbosity | Yes | Read from BOND.md preference |
| Article suggestions | Yes | Generate and write to MEMORY.md queued list |

**What headless invocation needs:**
- PULSE-template.md defining autonomous action (what to run, what to write, what to output)
- A `--headless` flag check in capability prompts, not just SKILL.md
- JSON output variant for health-check (counts + critical issues list)
- Skip all "Needs confirmation" fixes; log them for next human session

**Output contract:** `{"status": "warn|pass|fail", "files_scanned": N, "critical": N, "warnings": N, "suggestions": N, "report_path": "outputs/health-{date}.md"}`

---

## Key Findings

### [High-Opportunity] PULSE-template.md missing — headless mode non-functional
**Area:** `assets/PULSE-template.md` (does not exist)  
Inspector declares `--headless → Quiet Rebirth. Load PULSE.md from sanctum, execute, exit.` but the template that would create PULSE.md in the sanctum doesn't exist. Any user trying to run Inspector headlessly will fail silently at the PULSE.md load step.  
**Suggestion:** Create PULSE-template.md with a minimal autonomous action: run health check on vault, write report, output JSON summary, log session. ~30 lines.

### [High-Opportunity] No "vault not found" recovery path
**Area:** `references/health-check.md`, `references/fix-issues.md`  
If the vault path in BOND.md is wrong or the vault has moved, Inspector has no defined behavior. It will likely scan the wrong path and produce confusing results.  
**Suggestion:** Add to On Activation (SKILL.md): "If vault path from config or BOND.md is not accessible, alert the owner immediately and ask for the correct path before proceeding."

### [Medium-Opportunity] No "done when" completion signals in capabilities
**Area:** All operational capabilities  
Each capability describes what to do but not when it's finished. After a health check, should Inspector wait for questions? Offer to fix issues? Transition to suggestions?  
**Suggestion:** Add a 2-3 line "After this capability" section to HC, FX, SA, CC suggesting the natural next step. HC → "Want me to fix the critical issues now? [FX]". FX → "Health check is now cleaner — run another HC to confirm?" This creates a guided workflow.

### [Medium-Opportunity] First-timer orientation gap
**Area:** `references/first-breath.md`, lines 28–50  
First Breath's discovery questions assume the owner knows what "pedantic vs. pragmatic" checking means and whether their wiki is "mature." A brief orientation before the questions would help: "Most owners care most about broken links and orphaned articles — should I start with those, or do you have different priorities?"  
**Suggestion:** Add a 3-line orientation before "Questions to Explore" that names the most common priorities and asks if they apply.

### [Medium-Opportunity] Suggest Articles doesn't offer to draft
**Area:** `references/suggest-articles.md`  
After surfacing article suggestions, there's no offer to draft the highest-priority one. This is a dead-end — the owner has a list but must switch to writing mode themselves.  
**Suggestion:** Add "Offer to draft a skeleton for any suggestion the owner immediately accepts — title, summary, frontmatter, and 3-5 concept anchors."

### [Low-Opportunity] No off-scope redirect for content creation requests
**Area:** SKILL.md / CREED.md  
If a user asks Inspector to "write an article about X," the agent has no graceful path. Should note this in persona or principles.  
**Suggestion:** Add to CREED Anti-Patterns (Behavioral): "Don't pretend to be a content creation agent — redirect clearly and offer what you can (what the wiki currently says about X, whether coverage is thin)."

### [Low-Opportunity] MEMORY.md bloat handling
**Area:** `references/memory-guidance.md`  
The 200-line limit is stated but the agent has no behavior defined for when it's exceeded.  
**Suggestion:** Add: "If MEMORY.md exceeds 200 lines, alert the owner and offer to archive older false-positive patterns to a dated file in `sessions/`."

---

## Top Insights

1. **The PULSE gap is the highest-leverage fix.** Inspector is one template file away from being automatable. A weekly cron-triggered health check with JSON output would transform this from a manual audit tool into a continuous quality monitor.

2. **The natural next-step chain (HC → FX → SA) is implicit but never surfaced.** Inspector has a beautiful workflow arc — audit, fix, grow — but doesn't guide users through it. Adding "what's next?" transitions at the end of each capability would dramatically improve the experience without adding complexity.

3. **Memory makes Inspector compound over time — but this value is invisible.** Users won't feel the benefit of false-positive suppression until they've used Inspector 3-4 times. Surfacing the memory value explicitly ("I suppressed 7 issues today because you've dismissed similar ones before") would make the investment in First Breath and rebirth feel worth it.

---

## Facilitative Patterns Check

| Pattern | Present | Assessment |
|---------|---------|------------|
| Soft Gate Elicitation | No | First Breath uses structured questions, not soft gates. Low priority for a configuration-style agent. |
| Intent-Before-Ingestion | Partial | Urgency Detection is present, but First Breath could more clearly ask "what's most important to you today?" before diving into questions |
| Capture-Don't-Interrupt | No | If the owner shares information out-of-scope during discovery, no capture-and-defer mechanism exists |
| Dual-Output | No | Health check produces markdown only. JSON/machine-readable output would unlock automation |
| Parallel Review Lenses | No | Inspector analyzes from one perspective. A "skeptic lens" and "coverage spotter lens" before finalizing health check findings would improve recall |
| Three-Mode Architecture | Partial | Interactive (current) and headless declared but not built. Guided mode not present |
| Graceful Degradation | No | No fallback paths when vault is unavailable or MEMORY.md is corrupted |

**Highest value missing patterns:** Dual-Output (enables automation) and Graceful Degradation (prevents silent failures).
