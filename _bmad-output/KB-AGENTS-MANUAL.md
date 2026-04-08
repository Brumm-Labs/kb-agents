# KB Agents — User Manual

Technical reference for the three Knowledge Base agents: **Archivist** (Ingest), **Cartographer** (Compiler), **Inspector** (Linter).

---

## 1. Setup: New Knowledge Base

### 1.1 Init-Script (empfohlen)

Ein Befehl erstellt alles — Vault-Struktur, Agents, Sanctums:

```bash
./kb-init.sh ~/vaults/my-research "My Research"
```

Das Script:
1. Erstellt die Vault-Struktur (`raw/`, `wiki/`, `outputs/`)
2. Kopiert BMAD-Konfiguration
3. Installiert alle 3 Agents als Claude Code Skills
4. Initialisiert die Sanctums (Agent-Gedächtnis)
5. Initialisiert ein Git-Repo

Danach:

```bash
cd ~/vaults/my-research
# Öffne den Ordner als Obsidian Vault
claude   # Agents sind bereit — First Breath startet beim ersten Aktivieren
```

**Beispiele:**

```bash
# Lokal
./kb-init.sh ~/vaults/ai-safety "AI Safety Research"

# iCloud
./kb-init.sh ~/Library/Mobile\ Documents/com~apple~CloudDocs/vaults/ml "Machine Learning"

# Beliebiger Pfad
./kb-init.sh /path/to/my-kb
```

### 1.2 Vault-Struktur (Referenz)

Das Init-Script erstellt diese Struktur:

```
my-research/
├── raw/                    # Rohdaten hierhin droppen
│   ├── articles/
│   ├── papers/
│   └── images/
├── wiki/                   # Vom Compiler gepflegt
│   ├── _index.md
│   ├── summaries/
│   ├── concepts/
│   └── connections/
├── outputs/                # Query-Ergebnisse, Slides, Reports
├── _bmad/                  # Agent-Konfiguration + Gedächtnis
├── .claude/skills/         # Installierte Agents
├── .kb-config.yaml         # KB-Metadaten
└── .gitignore
```

### 1.3 First Breath — Agents kennenlernen

Beim ersten Aktivieren startet jeder Agent eine Kennenlern-Konversation (First Breath). Er lernt deinen Namen, Vault-Pfad, Präferenzen und Workflow.

**Reihenfolge empfohlen:** Ingest → Compiler → Linter

### 1.4 Manuelles Setup (alternativ)

Falls du das Init-Script nicht nutzen willst:

```bash
# Struktur anlegen
mkdir -p my-kb/{raw/{articles,papers,images},wiki/{summaries,concepts,connections},outputs}

# Agents kopieren
cp -r _bmad-output/agent-kb-ingest my-kb/.claude/skills/
cp -r _bmad-output/agent-kb-compiler my-kb/.claude/skills/
cp -r _bmad-output/agent-kb-linter my-kb/.claude/skills/

# Sanctums initialisieren
python3 my-kb/.claude/skills/agent-kb-ingest/scripts/init-sanctum.py my-kb my-kb/.claude/skills/agent-kb-ingest
python3 my-kb/.claude/skills/agent-kb-compiler/scripts/init-sanctum.py my-kb my-kb/.claude/skills/agent-kb-compiler
python3 my-kb/.claude/skills/agent-kb-linter/scripts/init-sanctum.py my-kb my-kb/.claude/skills/agent-kb-linter
```

Danach den jeweiligen Agent aktivieren — er startet die "First Breath"-Konversation, in der er deinen Namen, Vault-Pfad, Präferenzen und Workflow lernt.

**Reihenfolge empfohlen:** Ingest → Compiler → Linter

---

## 2. Täglicher Workflow: Daten rein

### 2.1 Dateien droppen + Auto-Discover — `[AD]`

**Das ist der Standardweg.** Droppe Dateien in `raw/` (oder Unterordner) und starte den Ingest Agent:

```
Du: (Ingest Agent aktivieren)
Agent: "Hey Björn! Let me check for new sources... Found 3 new files in raw/. Processing them now."
```

Der Agent findet automatisch alle neuen Dateien die noch nicht im Index sind. Kein manuelles Angeben von Dateipfaden nötig.

**Zwei Modi (wird beim First Breath festgelegt):**
- **Auto-Mode:** Verarbeitet alles automatisch, zeigt Summary am Ende
- **Review-Mode:** Zeigt Liste der neuen Dateien, du wählst welche verarbeitet werden

**Unterstützte Formate:** `.md`, `.txt`, `.html`, `.pdf`, `.png`, `.jpg`, `.svg`

### 2.2 Einzelne Quelle manuell — `[IN]`

Für spezifische Quellen, z.B. URLs oder gepasteten Text:

- **URL:** "Ingest https://example.com/article"
- **Paste:** Kopiere den Text direkt in den Chat
- **Bild:** "Ingest `raw/images/diagram.png`" (erstellt Beschreibungs-Datei)

### 2.3 Batch-Import — `[BI]`

Für einen spezifischen Ordner:

"Batch-ingest alles in `raw/articles/new/`"

Summary-Report: X ingested, Y übersprungen (Duplikate), Z brauchen Review

### 2.4 Frontmatter-Schema

Jede aufgenommene Quelle bekommt dieses Frontmatter:

```yaml
---
title: "Titel der Quelle"
author: "Autor(en)"
date_published: 2025-03-15      # oder "unknown"
date_ingested: 2026-04-07
source_url: "https://..."        # oder "local"
source_type: article             # article|paper|repo|dataset|note|image|video
tags: [machine-learning, transformers]
summary: "1-2 Sätze Zusammenfassung"
status: raw                      # raw → summarized → compiled
related: []                      # wird vom Compiler gefüllt
---
```

### 2.5 Index verwalten — `[IX]`

| Befehl | Was passiert |
|--------|-------------|
| "Zeig mir den Index" | Durchsuchbare Übersicht aller Quellen |
| "Index rebuild" | Regeneriert Index aus Frontmatter (Script: `manage-index-tools.py {vault} rebuild`) |
| "Index stats" | Counts nach Typ, Tag-Frequenz, Status (Script: `manage-index-tools.py {vault} stats`) |
| "Orphan check" | Findet Dateien ohne Index-Eintrag (Script: `manage-index-tools.py {vault} orphans`) |

---

## 3. Wiki aufbauen

### 3.1 Quellen kompilieren — `[CS]`

Starte den Compiler Agent:

"Kompiliere die neuen Quellen"

Der Agent:
1. Findet alle Quellen mit `status: raw` oder `summarized`
2. Liest jede Quelle vollständig
3. Erstellt eine Summary in `wiki/summaries/` mit:
   - Obsidian `[[wiki-links]]` zu relevanten Konzepten
   - Backlink zur Raw-Quelle
   - Key Takeaways
4. Markiert Quellen als `compiled` im Source Index
5. Aktualisiert `wiki/_index.md`

### 3.2 Konzept-Artikel pflegen — `[MC]`

| Befehl | Was passiert |
|--------|-------------|
| "Erstelle einen Konzept-Artikel über Transformers" | Neuer Artikel in `wiki/concepts/` |
| "Update den Artikel über Attention Mechanisms" | Ergänzt mit neuen Quellen |
| "Promote alle Stubs mit 3+ Quellen" | Stub → Draft hochstufen |
| "Merge Attention und Self-Attention" | Zwei Artikel zusammenführen |
| "Concept inventory" | Übersicht aller Konzepte mit Status |

**Konzept-Lebenszyklus:** `stub` → `draft` → `mature`

### 3.3 Verbindungen schreiben — `[WC]`

"Schreib eine Verbindung zwischen Transformers und CNNs"

**Verbindungstypen:**
- **Convergence** — verschiedene Ansätze, gleiche Schlussfolgerung
- **Contradiction** — Quellen widersprechen sich
- **Evolution** — wie sich Verständnis über Zeit verändert hat
- **Pattern** — wiederkehrendes Thema über unzusammenhängende Quellen
- **Comparison** — strukturierter Vergleich von Ansätzen

### 3.4 Wiki pflegen — `[MW]`

| Befehl | Script | Was passiert |
|--------|--------|-------------|
| "Check links" | `wiki-tools.py {vault} check-links` | Broken Links + Orphans finden |
| "Uncompiled sources" | `wiki-tools.py {vault} uncompiled` | Noch nicht kompilierte Quellen |
| "Concept inventory" | `wiki-tools.py {vault} inventory` | Status aller Konzepte |
| "Rebuild index" | — | `wiki/_index.md` neu generieren |
| "Update backlinks" | — | Bidirektionale Links sicherstellen |

### 3.5 Wiki abfragen — `[QW]`

"Was sagen meine Quellen über Scaling Laws?"

**Output-Formate:**
- **Inline** (Standard) — Antwort direkt im Chat mit `[[wiki-links]]`
- **Markdown** — "Schreib die Antwort als Datei in `outputs/`"
- **Slides** — "Erstell eine Marp-Präsentation dazu"
- **Tabelle** — "Vergleiche X und Y in einer Tabelle"

---

## 4. Qualität sichern

### 4.1 Health Check — `[HC]`

Starte den Linter Agent:

"Health Check"

**Ablauf:**
1. Script `prepass-wiki-health.py {vault}` läuft (deterministische Checks → JSON)
2. Agent interpretiert Ergebnisse und ergänzt LLM-basierte Analyse
3. Report: Summary → Critical → Warnings → Suggestions → Stats

**Health-Status:** 🟢 Good | 🟡 Needs attention | 🔴 Issues found

### 4.2 Issues fixen — `[FX]`

"Fix die Issues aus dem Health Check"

**Drei Stufen:**

| Stufe | Beispiele | Verhalten |
|-------|-----------|-----------|
| **Auto-fix** | Fehlende Backlinks, Index-Updates, Frontmatter-Dates | Ohne Nachfrage |
| **Bestätigung** | Broken Links entfernen, Stubs promoten, Orphans löschen | Fragt nach |
| **Owner-Entscheidung** | Widersprüche auflösen, Kategorisierung wählen | Zeigt Optionen |

### 4.3 Artikel vorschlagen — `[SA]`

"Was könnte die Wiki verbessern?"

Der Agent analysiert:
- Tags in 3+ Quellen ohne Konzept-Artikel
- Widersprüche die einen Connection-Artikel verdienen
- Stubs die genug Quellen für ein Upgrade haben
- Lücken in deinen Forschungsinteressen

**Neu:** Kann direkt Stub-Artikel erstellen für akzeptierte Vorschläge.

### 4.4 Konsistenz-Check — `[CC]`

"Deep consistency check"

Prüft:
- **Fakten:** Widersprüche zwischen Artikeln und Quellen
- **Terminologie:** Gleicher Begriff, verschiedene Namen
- **Attribution:** Claims ohne Quellenangabe
- **Struktur:** Frontmatter-Verstöße, inkonsistente Formatierung

---

## 5. Regelmäßige Routinen

### Täglich empfohlen

| Was | Agent | Wie | Dauer |
|-----|-------|-----|-------|
| Neue Quellen aufnehmen | Ingest | Dateien droppen, Agent starten → `[AD]` läuft automatisch | 2-5 min |
| Quellen kompilieren | Compiler | `[CS]` interaktiv | 10-20 min |

### Wöchentlich empfohlen

| Was | Agent | Wie | Dauer |
|-----|-------|-----|-------|
| Health Check | Linter | `[HC]` → `[FX]` | 10 min |
| Konzepte pflegen | Compiler | `[MC]` Promote stubs, merge | 10-15 min |
| Verbindungen schreiben | Compiler | `[WC]` für neue Connections | 10-15 min |
| Artikel-Vorschläge | Linter | `[SA]` | 5 min |

### Monatlich empfohlen

| Was | Agent | Wie | Dauer |
|-----|-------|-----|-------|
| Deep Consistency Check | Linter | `[CC]` | 15-20 min |
| Wiki reorganisieren | Compiler | `[MW]` Kategorien prüfen | 10 min |
| Index rebuild | Ingest | `[IX]` rebuild + stats | 5 min |

### Headless / Cron (optional)

Für automatische Hintergrund-Pflege:

```bash
# Täglich: Neue Quellen auto-ingest
agent-kb-ingest --headless

# Täglich (nach Ingest): Pending sources kompilieren
agent-kb-compiler --headless

# Wöchentlich: Health Check + Auto-Fix
agent-kb-linter --headless
```

**Named Tasks:**

| Agent | Task | Trigger |
|-------|------|---------|
| Ingest | Nur ingest | `-H:ingest` |
| Ingest | Index rebuild | `-H:reindex` |
| Ingest | Memory curation | `-H:curate` |
| Compiler | Alle pending kompilieren | `-H:compile` |
| Compiler | Stubs promoten | `-H:concepts` |
| Compiler | Index rebuild | `-H:index` |
| Compiler | Memory curation | `-H:curate` |
| Linter | Health Check + Fix | `-H:health` |
| Linter | Konsistenz-Analyse | `-H:consistency` |
| Linter | Artikel-Vorschläge | `-H:suggest` |
| Linter | Memory curation | `-H:curate` |

---

## 6. Daten-Pipeline im Überblick

```
Quellen (Web, Papers, Notes)
         │
         ▼
┌─────────────────┐
│  📚 Archivist   │  raw/articles/
│  [IN] [BI] [IX] │  raw/papers/
│                  │  raw/_source-index.md
└────────┬────────┘
         │ status: raw → compiled
         ▼
┌─────────────────┐
│  🗺️ Cartographer │  wiki/summaries/
│  [CS][MC][MW]   │  wiki/concepts/
│  [WC][QW]       │  wiki/connections/
│                  │  wiki/_index.md
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  🔍 Inspector   │  Health Reports
│  [HC][FX][SA]   │  Fix Issues
│  [CC]           │  Suggestions
└─────────────────┘
```

---

## 7. Mehrere Knowledge Bases

Jede KB ist ein eigener Obsidian Vault. Die Agents kennen den Vault-Pfad aus dem First Breath (in BOND.md gespeichert).

**Optionen für mehrere KBs:**
- **Gleiche Agent-Instanzen, verschiedene Vaults:** Gib beim Aktivieren den Vault-Pfad an. Der Agent wechselt den Kontext.
- **Separate Agent-Instanzen pro KB:** Kopiere die Agent-Skills und erstelle separate Sanctums. Jeder Agent lernt die spezifischen Konventionen einer KB.

**Empfehlung:** Starte mit einer KB, optimiere den Workflow, dann repliziere für weitere.

---

## 8. Tipps

- **Obsidian Web Clipper** für Artikel → direkt in `raw/articles/` speichern, dann `[IN]` zum Normalisieren
- **Tags konsistent halten** — der Archivist warnt bei Tag-Drift, aber hilf ihm durch klare Konventionen
- **Query vor neuem Ingest** — `[QW]` prüfen ob das Thema schon abgedeckt ist
- **Connections sind der eigentliche Wert** — plane regelmäßig Zeit für `[WC]` ein
- **Health Check vor großen Sessions** — `[HC]` am Wochenanfang, dann die Woche über ohne Qualitäts-Sorgen arbeiten
- **Agents lernen dazu** — sie werden über Sessions besser. Je mehr du mit ihnen arbeitest, desto besser kennen sie deine Konventionen
