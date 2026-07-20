# CLAUDE.md — Projektregeln

## Sprache
Immer auf Deutsch antworten.

---

## Excel-Filter (Fallback — nur wenn MCP nicht verfügbar)
Neueste `*.xlsx` im Unterordner `data/` des Projektverzeichnisses verwenden (Dateiname egal, bei mehreren → nach Dateiänderungsdatum neueste). Sheet: „SAPUI5 Export". Folgende Filter anwenden:
- **botStatusId:** In Development
- **servicePackageId:** beginnt mit 1, 2, 3 oder 4
- **technologiesId:** `Artificial Intelligence` oder `Joule Studio Agent`
- **Sortierung:** neueste zuerst (nach `dataCreated` DESC)

---

## JIRA-Filter (Standard)
Bei allen JQL-Abfragen:
- **Status:** In Development
- **Issue Type:** Feature
- **Service Package:** 1–4
- **Sortierung:** neueste zuerst (ORDER BY created DESC)

---

## Cases analysieren / MISTA erstellen

Wenn der User eine MISTA möchte — egal wie formuliert, auch ohne festes Schlüsselwort — die KBV-Kategorisierungs-Analyse durchführen und `mista_DDMMYYYY.html` erstellen. Bei Unklarheit kurz nachfragen.

### Datenquelle — automatisch wählen

- **MCP verfügbar (bevorzugt):** IUCR per `mcp__iucr-mcp-prod__query` abrufen. Standard-Filter:
  - `STATUS = 'In Development'`
  - `SOLUTION_TYPE in ('Artificial Intelligence', 'Joule Studio Agent')`
  - `SERVICE_PACKAGE in ('1 - Do It Yourself (Citizen Development)', '2 - Operations Package', '3 - Development & Operations Package', '4 - PoC, Development & Ops (Full Service Package)')`
  - Sortierung: `LIFECYCLE__CREATED_DATE desc`
- **Fallback (kein MCP):** Neueste `*.xlsx` aus `data/`, Sheet „SAPUI5 Export", gleiche Filter.

### Standard-MISTA — Modi

**Standard (ohne weitere Angabe):**
- Nur „My Action Required": Standard-Filter + `APR__WOCCO__STATUS in ('Waiting for WoCCo Feedback', 'Input Required')`
- Kein zweiter Abschnitt

**Mit Anzahl (z.B. „5 neueste" oder „10 neueste"):**
- Abschnitt 1 — „My Action Required": Standard-Filter + WoCCo-Filter (IDs merken)
- Abschnitt 2 — „Neue Cases": Standard-Filter, kein WoCCo-Filter, absteigende Sortierung nach `LIFECYCLE__CREATED_DATE`, genannte Anzahl, My Action Required IDs per `not in` ausschließen

**Mit expliziten IDs oder anderem Filter:**
- Nur die genannten Cases / den genannten Filter verwenden, kein WoCCo-Filter, keine Zweiteilung

### Modi — automatisch erkennen

- **Nur Screenshot** → MISTA mit genau den im Bild sichtbaren Cases erstellen.
- **Mit IDs** → Nur genannte Cases (IRPA-R... oder INTAI-...), per `mcp__iucr-mcp-prod__query` oder JIRA abrufen.
- **Mit Bild(ern)** → Informationen direkt aus dem Bild extrahieren, ggf. MCP/JIRA ergänzend abrufen.

### Ablauf
1. My Action Required per MCP abrufen (WoCCo-Filter), ggf. zusätzliche Cases je nach Angabe
2. JIRA-Tickets per MCP abrufen falls INTAI-ID im Namen vorhanden
3. Jeden Case vollständig analysieren → KBV-Kategorie S / M / L bestimmen
4. Alte `mista_*.html` löschen (Bash: `rm mista_*.html`), dann neue `mista_DDMMYYYY.html` mit heutigem Datum erstellen

---

## Design & Layout (verbindlich)

Immer dieses Design verwenden — nicht ändern außer der User bittet explizit darum:

**Header:** Dunkler Gradient (`#1a1a2e → #16213e`), links Titel + Stat-Badges, rechts oben Live-Suchfeld (sucht nach Titel, Case-ID, JIRA-ID).

**Cases — standardmäßig eingeklappt:** Kategorie-Badge, Titel, Case-ID, JIRA-Link, Meta-Tags, Chevron `▶`. Klick auf Header klappt auf/zu. JIRA-Link und Gutachten-Button mit `event.stopPropagation()`.

**Aufgeklappt:**
1. 2-spaltiges Grid: Karte „Personenbezogene Daten" (blauer Rand) + Karte „Auswirkungen auf Mitarbeitende" (lila Rand)
2. Kein „Fehlende KBV-Pflichtpunkte"-Block
3. Mitigation-Block: 2-spaltig bei S, 3-spaltig bei M/L (mit Upgrade-Spalte)
4. Gutachten-Button: separat aufklappbar, `white-space: pre-wrap`

**Style:** Hintergrund `#f1f4f8`, weiße Cards, System-Font, 14px, responsive unter 700px, keine externen Frameworks.

---

## Gutachten-Format (Fließtext, `white-space: pre-wrap`)

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

## Kategorisierungslogik

- **Kategorie S:** Keine personenbezogenen Mitarbeiterdaten im Arbeitsprozess ODER reine Authentifizierungsdaten; geringe Auswirkung auf Aufgaben; Disclaimer + Enablement vorhanden oder leicht ergänzbar
- **Kategorie M:** Personenbezogene Mitarbeiterdaten im Arbeitsprozess; überschaubare bis mittlere Auswirkung; keine vollständige Aufgabenübernahme
- **Kategorie L:** Weitreichende personenbezogene Datenverarbeitung; hohe Auswirkung; Entscheidungsersatz durch KI; starke Leistungs-/Verhaltenskontrolle möglich
