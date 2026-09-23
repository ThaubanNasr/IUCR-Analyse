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

Wenn der User eine MISTA möchte — egal wie formuliert, auch ohne festes Schlüsselwort — die KBV-Kategorisierungs-Analyse durchführen und `mista_TT-MM-JJJJ.html` erstellen. Bei Unklarheit kurz nachfragen.

### Datenquelle — automatisch wählen

- **MCP verfügbar (bevorzugt):** IUCR per `mcp__iucr-mcp-prod__query` abrufen. Standard-Filter:
  - Sortierung: `LIFECYCLE__CREATED_DATE desc`
  - **Kein** STATUS-, SOLUTION_TYPE- oder SERVICE_PACKAGE-Filter für My Action Required
- **Fallback (kein MCP):** Neueste `*.xlsx` aus `data/`, Sheet „SAPUI5 Export", nur WoCCo-Filter.

### Standard-MISTA — Modi

**Standard (ohne weitere Angabe):**
- Nur „My Action Required": Einziger Filter: `APR__WOCCO__STATUS = 'Waiting for WoCCo Feedback'`
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
1. My Action Required per MCP abrufen (WoCCo-Filter via `mcp__iucr-mcp-prod__query`), ggf. zusätzliche Cases je nach Angabe
2. **Vollständigkeit prüfen (Pflicht):** Den `count`-Wert aus der Query-Antwort lesen. Wenn `count` größer ist als die Anzahl zurückgelieferter Datensätze → mit `offset` weiter paginieren bis alle Cases vorhanden sind. Erst danach fortfahren.
   - Außerdem: `getUseCaseById` liefert bei IDs mit mehreren Versionen (z.B. Obsolete + aktive Neuauflage) **immer nur eine Version**. Wenn die Query einen Case mit `STATUS = 'In Development'` und `APR__WOCCO__STATUS = 'Waiting for WoCCo Feedback'` liefert, aber `getUseCaseById` eine Obsolete-Version zurückgibt → den Case **nicht ausschließen**, sondern die Query-Daten direkt verwenden.
3. **Duplikat-Prüfung (Pflicht) vor jedem Case-Einfügen:** Bevor ein neuer Case-Block in die HTML eingefügt wird, per `grep` prüfen ob die Case-ID (z.B. `IRPA-R2216`) bereits in der Datei vorkommt. Nur einfügen wenn kein Treffer.
4. **Für jeden Case `getUseCaseById` aufrufen** — liefert vollständige Felder (Description, Business Value, Other Process, Labels, Using UiPath etc.). Die Query-Ergebnisse sind teils abgeschnitten und unvollständig.
5. JIRA-Tickets per MCP abrufen falls INTAI-ID im Namen vorhanden
6. Jeden Case vollständig analysieren → KBV-Kategorie S / M / L bestimmen
7. **Sortierung:** Cases in der HTML exakt in IUCR-Reihenfolge ausgeben — absteigende Sortierung nach `LIFECYCLE__CREATED_DATE` (neueste oben, älteste unten), identisch zur IUCR-Oberfläche
8. MISTA-Datei speichern:
   - **Dateiname:** `mista_TT-MM-JJJJ.html` (z. B. `mista_06-08-2026.html`)
   - **Zielpfad:** `C:\Users\I777951\WoCCo\Automate\IUCR-Analyse\`
   - Datei des **gleichen Tages** überschreiben — Dateien anderer Tage **niemals** anfassen
   - **Niemals** Dateien löschen (`rm` ist verboten)

### Statistik — Waiting-Verlauf

Bei jeder MISTA-Erstellung:

1. **Vorherige MISTA lesen:** Neueste `mista_*.html` im Projektverzeichnis suchen (nicht die des heutigen Tages). Darin den Block `<script id="wocco-stats" type="application/json">` extrahieren und als JSON parsen.

2. **Aktuellen Snapshot erstellen:** Liste aller aktuellen „Waiting for WoCCo Feedback" IDs mit `APR__WOCCO__LATEST_STATUS_CHANGE_DATE` (= wann auf Waiting gesetzt).

3. **Differenz berechnen:**
   - **Neu:** IDs im aktuellen Snapshot, die im vorherigen nicht waren
   - **Bearbeitet:** IDs im vorherigen Snapshot, die aktuell nicht mehr „Waiting" sind

4. **Stats-Block aktualisieren:** Vorherige `snapshots`-Liste übernehmen, neuen Eintrag anhängen:
```json
{
  "snapshots": [
    {
      "date": "2026-08-14",
      "waiting": ["IRPA-R123", "IRPA-R456"],
      "new": ["IRPA-R123", "IRPA-R456"],
      "processed": [],
      "count": 2
    }
  ]
}
```

5. **In neue MISTA einbetten:** Den Block als `<script id="wocco-stats" type="application/json">` unsichtbar in die HTML einbauen (wird nicht angezeigt, nur maschinell gelesen).

6. **Statistik-Widget im Header anzeigen:** Unterhalb der Stat-Badges eine kompakte Tabelle:

| Datum | Waiting | Neu | Bearbeitet |
|-------|---------|-----|-----------|
| 21.08.2026 | 7 | 3 | 2 |
| 14.08.2026 | 6 | 6 | 0 |

- Neueste Zeile oben
- Nur anzeigen wenn mindestens 1 Snapshot vorhanden
- Style: kompakt, passend zum Header-Design (dunkler Hintergrund, helle Schrift)

---

## Design & Layout (verbindlich)

Immer dieses Design verwenden — nicht ändern außer der User bittet explizit darum:

**Header:** Dunkler Gradient (`#1a1a2e → #16213e`), links Titel + Stat-Badges, rechts oben Live-Suchfeld (sucht nach Titel, Case-ID, JIRA-ID).

**Cases — standardmäßig eingeklappt:** Kategorie-Badge, Titel, Case-ID, JIRA-Link, Meta-Tags, Chevron `▶`. Klick auf Header klappt auf/zu. JIRA-Link und Gutachten-Button mit `event.stopPropagation()`.

**Aufgeklappt:**
1. 2-spaltiges Grid: Karte „Personenbezogene Daten" (blauer Rand) + Karte „Auswirkungen auf Mitarbeitende" (lila Rand)
2. Kein „Fehlende KBV-Pflichtpunkte"-Block
3. Mitigation-Block: 2-spaltig bei S, 3-spaltig bei M/L (mit Upgrade-Spalte)
4. Zwei Buttons nebeneinander (gleicher Style):
   - **„Case-Details ▾"**: klappt Block auf mit allen IUCR-Feldern direkt aus den Rohdaten (`getUseCaseById`). **Ganz oben** im Block: falls eine INTAI-ID vorhanden (`METADATA__REFERENCE_DEPENDENCY_FIELD`), einen direkten Jira-Link einfügen: `<a href="https://jira.tools.sap/browse/INTAI-XXXX" ...>🔗 INTAI-XXXX in Jira öffnen</a>`. Pflichtfelder darunter: **Use Case Name, Description, Business Value, Board Area, Main affected Business Process, Other Important Business Process, Solution Type, Service Package, Using UiPath, Labels**. Felder ohne Wert mit „—" kennzeichnen. Format: `white-space: pre-wrap`, grauer linker Rand (`border-left: 4px solid #94a3b8`). Button + Inhalt mit `event.stopPropagation()`.
   - **„Gutachten ▾"**: separat aufklappbar, `white-space: pre-wrap` (unverändert)

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
