---
name: MISTA — KBV-Kategorisierung
description: >
  Erstellt eine MISTA-Analyse (KBV-Kategorisierung S/M/L) für IUCR AI-Cases.
  Aktiviert bei: "erstell eine MISTA", "my action required", "KBV-Analyse",
  "kategorisiere Cases", "neue Cases analysieren", "MISTA erstellen".
allowed-tools:
  - write_file
  - read_file
  - run_python
required_mcp_servers: "*.hana.ondemand.com/mcp/iucr *.jira.tools.sap/mcp"
---

# MISTA — KBV-Kategorisierungsanalyse

## Ziel
Erstelle eine vollständige KBV-Kategorisierungsanalyse als HTML-Datei `mista_DDMMYYYY.html`
im Working Directory (heutiges Datum im Dateinamen, z. B. `mista_06082026.html`).

---

## Schritt 1 — Modus bestimmen

**Standard (keine weiteren Angaben):**
- Nur „My Action Required": Filter `APR__WOCCO__STATUS in ('Waiting for WoCCo Feedback', 'Input Required')`
- Sortierung: `LIFECYCLE__CREATED_DATE desc`
- Kein zweiter Abschnitt

**Mit Anzahl (z. B. „5 neueste" oder „10 neueste"):**
- Abschnitt 1 — My Action Required: WoCCo-Filter, IDs merken
- Abschnitt 2 — Neue Cases: kein WoCCo-Filter, absteigende Sortierung, genannte Anzahl, My-Action-Required-IDs per `not in` ausschließen

**Mit expliziten IDs (IRPA-R... oder INTAI-...):**
- Nur diese Cases abrufen, kein WoCCo-Filter, keine Zweiteilung

---

## Schritt 2 — Daten abrufen

### IUCR Cases (MCP)
- Connector: IUCR MCP
- Kein STATUS-, SOLUTION_TYPE- oder SERVICE_PACKAGE-Filter für My Action Required
- Pflichtfelder: ID, Titel, Beschreibung, Solution Type, Service Package, Status, Created Date,
  APR__WOCCO__STATUS, AI Ethics Klassifizierung, geplante Mitigationsmaßnahmen

### JIRA-Tickets (falls INTAI-ID vorhanden)
- Connector: JIRA MCP
- Felder: Summary, Status, Description, Labels, Priority
- Informationen zur Kategorisierung nutzen

---

## Schritt 3 — Jeden Case analysieren

Für jeden Case vollständig analysieren gemäß `references/kbv_logic.md`:

1. Verarbeitung personenbezogener Daten prüfen
2. Auswirkungen auf Arbeitsprozesse / Mitarbeitende prüfen
3. KBV-Kategorie S / M / L bestimmen
4. Gutachten im Fließtext-Format erstellen (siehe unten)

### Gutachten-Format (Fließtext, `white-space: pre-wrap`)

```
Kategorisierung: Kategorie [S/M/L]
Der KI-Anwendungsfall "[Name]" fällt in Kategorie [X] basierend auf folgender Analyse:

Begründung der Kategorisierung

1. Verarbeitung personenbezogener Daten
[Kernbefund als Unterüberschrift]:
- Punkt 1
- Punkt 2

2. Auswirkungen auf Arbeitsprozesse
[Einschätzung der Eingriffstiefe]:
- Punkt 1
- Punkt 2

Erforderliche Mitigationsmaßnahmen

Folgende Mitigationsmaßnahmen sollten implementiert werden:

1. Bereits geplante/implementierte Maßnahmen:
[Maßnahme]: [Beschreibung]

2. Empfohlene zusätzliche Mitigationsmaßnahmen:
[Maßnahme]: [Beschreibung]

3. Mögliche Mitigation zur Kategorie S:   ← nur bei M oder L
Der Anwendungsfall könnte in Kategorie S eingeordnet werden, wenn:
[Bedingung]

Fazit
[farbiger div-Block: fazit-s grün / fazit-m gelb / fazit-l rot]
```

---

## Schritt 4 — HTML-Datei erstellen

HTML-Struktur gemäß `references/html_template.md` verwenden.

Alte `mista_*.html`-Dateien im Working Directory vorher löschen.

Datei per `write_file` ins Working Directory schreiben → erscheint als Artifact-Chip im Chat.
