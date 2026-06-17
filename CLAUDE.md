# CLAUDE.md — Projektregeln

## Sprache
Immer auf Deutsch antworten.

## JIRA-Filter (Standard)
Bei allen JQL-Abfragen folgende Filter verwenden:
- **Status:** In Development
- **Issue Type:** Feature
- **Service Package:** 1–4 (Do It Yourself / Operations / Development & Operations / Full Service Package)
- **Sortierung:** neueste zuerst (ORDER BY created DESC)

## Excel-Filter (Standard)
Beim Einlesen der Excel immer die **neueste IUCR_*.xlsx** im Projektverzeichnis verwenden (nach Dateiänderungsdatum). Folgende Filter anwenden:
- **botStatusId:** In Development
- **servicePackageId:** beginnt mit 1, 2, 3 oder 4
- **technologiesId:** `Artificial Intelligence` oder `Joule Studio Agent`
- **Sortierung:** neueste zuerst (nach `dataCreated` DESC)
- **Anzahl:** 15 neueste Einträge

---

## Übersichts-Befehl
Wenn der User **„übersicht"** (oder „/übersicht") schreibt:
1. Im Projektverzeichnis `C:\Users\I777951\WoCCo\Automate\IUCR-Analyse` die **neueste IUCR_*.xlsx** suchen (nach Dateiänderungsdatum — neueste gewinnt). Diese Datei einlesen (Sheet: "SAPUI5 Export").
2. Die **15 neusten Einträge** nach den **Excel-Filtern (Standard)** filtern: botStatusId = In Development, servicePackageId 1–4, technologiesId = `Artificial Intelligence` oder `Joule Studio Agent`
3. Für jeden Eintrag: falls eine JIRA-Ticket-ID in der Spalte `botName` enthalten ist, das Ticket per Jira MCP abrufen und in die Analyse einbeziehen
4. Jedes Ticket vollständig analysieren (Excel-Daten + ggf. JIRA-Ticket + KBV-Prüfung: personenbezogene Daten, Leistungs-/Verhaltenskontrolle, fehlende Pflichtpunkte, Ampel)
5. Die Datei `kbv_uebersicht.html` vollständig neu schreiben — alle Zeilen ausgefüllt
6. Ampel-Logik: ROT = kritische KBV-Lücken | GELB = kleinere Lücken | GRÜN = keine offenen Pflichtpunkte

### HTML-Layout (verbindlich)
So wird die `kbv_uebersicht.html` immer aufgebaut — nicht ändern, außer der User bittet explizit darum:

**Übersichtstabelle (kompakt):**
- Eine Zeile pro Case: RequestID (+ JIRA-Link falls vorhanden) | Name/Use Case | LOB | Ampel
- Zeile ist klickbar → klappt Detailpanel auf/zu (nur ein Panel gleichzeitig offen)
- Aktive Zeile wird visuell hervorgehoben, Chevron dreht sich

**Detailpanel (aufklappbar unter der Zeile):**
- Überschrift mit RequestID, Name und ggf. JIRA-Referenz
- 2-spaltiges Grid mit Karten:
  - Karte 1: Personenbezogene Daten (Liste + DPIA-Status)
  - Karte 2: Leistungs-/Verhaltenskontrolle (Risiko-Badge HOCH/MITTEL/GERING + Liste)
  - Karte 3 (volle Breite): Fehlende KBV-Pflichtpunkte (Liste in rot)
- E-Mail-Entwurf darunter mit Betreff-Anzeige und zwei Buttons:
  - **„In Outlook öffnen"** → `mailto:`-Link mit vorausgefülltem Empfänger, Betreff und Body — öffnet nur den Entwurf in Outlook, schickt NICHTS automatisch ab
  - **„Kopieren"** → kopiert Betreff + Text in die Zwischenablage

**Primärschlüssel:** `requestId` aus der Excel als `id`-Attribut der `<tr>` (`<tr id="IRPA-R491">`)

**Ampel-Logik:** ROT = kritische KBV-Lücken | GELB = kleinere Lücken | GRÜN = keine offenen Pflichtpunkte

**Risiko-Badges:** HOCH (rot), MITTEL (orange), GERING (grün)

---
- `requestId` → Primärschlüssel (HTML-ID)
- `botName` → Titel / ggf. JIRA-Ticket-Link
- `botStatusId` → Status
- `servicePackageId` → Filter
- `controlBehaviour` → Leistungs-/Verhaltenskontrolle (Hinweis aus Excel)
- `process_PersonalData` → personenbezogene Daten (Hinweis aus Excel)
- `germanEmployees` → deutsche Mitarbeitende betroffen
- `botDescription` → Beschreibung
- `woccoRemarks` / `woccoCategory` → WoCCo-Status
- `coDetermination` → Mitbestimmungsrelevanz

---

## JIRA-Issue-Analyse

### Trigger
Wenn der User nur eine Ticketnummer nennt (z. B. „INTAI1120", „intai 1120", „1120" im INTAI-Kontext, mit oder ohne Bindestrich), automatisch die vollständige Analyse inkl. KBV-Prüfung und E-Mail-Entwurf durchführen — ohne Rückfrage.

### Scope
Nur das direkt angefragte Ticket analysieren — keine verlinkten Sub-Tasks, Parent-Issues oder referenzierte Tickets eigenständig abrufen oder analysieren, außer der User fragt explizit danach.

### KBV-Prüfung (automatisch bei jeder Analyse)
Bei jeder Analyse eines JIRA-Issues die **Interims-Konzernbetriebsvereinbarung über KI (Interims-KBV, datiert 31.10.2025)** automatisch mitberücksichtigen — ohne dass der User explizit danach fragen muss.

Die KBV-PDF liegt unter: `C:\Users\I777951\WoCCo\Automate\ManualCateg\Interims_KI_KBV_14102025.docx.pdf`

Nach der inhaltlichen Issue-Analyse immer folgendes prüfen:
- Welche personenbezogenen Daten werden verarbeitet? (→ DPIA erforderlich?)
- Ist Leistungs- oder Verhaltenskontrolle möglich? (→ Nutzungsausschluss nötig?)
- Was fehlt im Ticket laut KBV (DPIA, Nutzungsausschluss, IUCR-Eintrag, Disclaimer, Mitigationsmaßnahmen)?

**Nicht automatisch prüfen:** KBV-Kategorisierung (S / M / L) — nur wenn der User explizit danach fragt.

### E-Mails
E-Mail-Entwürfe nur erstellen, niemals ohne ausdrückliche Genehmigung abschicken.

Keine einleitenden Höflichkeitsfloskeln wie „Vielen Dank für die Einreichung..." oder „Der Use Case adressiert einen relevanten Pain Point...". Direkt mit den offenen Punkten beginnen. Kein Satz wie „Bitte melde dich bis [Datum einsetzen] mit einem Update." — keine Platzhalter für Deadlines. Nicht „bitte im Ticket ergänzen" — stattdessen den Empfänger bitten, die offenen Fragen per Antwort auf die Mail zu beantworten.
