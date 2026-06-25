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
Beim Einlesen der Excel immer die **neueste `*.xlsx`** im Unterordner `data/` des Projektverzeichnisses verwenden — der Dateiname kann variieren (z.B. `IUCR_15June.xlsx`, `IUCR_July.xlsx` usw.). Falls mehrere `.xlsx`-Dateien vorhanden sind, die nach **Dateiänderungsdatum neueste** nehmen. Folgende Filter anwenden:
- **botStatusId:** In Development
- **servicePackageId:** beginnt mit 1, 2, 3 oder 4
- **technologiesId:** `Artificial Intelligence` oder `Joule Studio Agent`
- **Sortierung:** neueste zuerst (nach `dataCreated` DESC)
- **Anzahl:** 15 neueste Einträge

---

## Übersichts-Befehl
Wenn der User **„übersicht"** (oder „/übersicht") schreibt:
1. Im Unterordner `data/` des Projektverzeichnisses `C:\Users\I777951\WoCCo\Automate\IUCR-Analyse\data` die **neueste `*.xlsx`** suchen (nach Dateiänderungsdatum — neueste gewinnt, Dateiname egal). Diese Datei einlesen (Sheet: "SAPUI5 Export").
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

## Go-Live-Filter (optional)

Nur anwenden, wenn der User **explizit** danach fragt (z.B. „zeig auch Go-Live-Cases", „mit Go-Live-Filter", „bald live").

Wenn aktiv: Zusätzlich zu den 15 Standard-Einträgen alle weiteren Cases einbeziehen, bei denen `goLiveDate` **oder** `estimatedGoLiveDate` innerhalb der nächsten 10 Wochen ab heute liegen (also zwischen heute und heute + 70 Tage). Diese Cases kommen **oben** in der Übersicht und werden mit einem Badge **„⚠️ Go-Live bald"** markiert.

Bei diesen Cases zusätzlich folgende Spalten auf Anmerkungen prüfen und im Detailpanel anzeigen (falls befüllt):
- `addComments`
- `historyComments`
- `WC_remarks`
- `DPP_remarks`
- `AI Ethics_remarks`

---

## Go-Live-Prioritätsliste (`golive`)

Wenn der User **„golive"** (oder „/golive") schreibt:

1. Die **neueste `*.xlsx`** aus `data/` einlesen (Sheet: "SAPUI5 Export") — gleiche Datei wie bei `übersicht`.
2. **Excel-Filter (Standard)** anwenden: botStatusId = In Development, servicePackageId 1–4, technologiesId = `Artificial Intelligence` oder `Joule Studio Agent`
3. Zusätzlich: nur Cases bei denen `goLiveDate` **oder** `estimatedGoLiveDate` im folgenden Zeitfenster liegen:
   - **Untere Grenze:** Beginn des aktuellen Quartals (Q1 = 01.01., Q2 = 01.04., Q3 = 01.07., Q4 = 01.10.)
   - **Obere Grenze:** Ende des nächsten Quartals + 6 Wochen Puffer (z.B. Q2 läuft → nächstes Quartal Q3 endet 30.09. + 6 Wochen = ca. 11.11.)
   - Das Fenster bleibt im Quartal stabil — es springt erst beim Quartalswechsel weiter
   - Cases deren Datum bereits in der Vergangenheit liegt trotzdem anzeigen, aber mit Badge **„✅ bereits live"** kennzeichnen
4. Sortierung: aufsteigend nach Go-Live-Datum (nächstes Datum oben).
5. Die Datei `golive_prioritaeten.html` neu schreiben.

### HTML-Layout `golive_prioritaeten.html`

**Schlanke Tabelle — kein aufklappbares Detailpanel:**

Eine Zeile pro Case mit folgenden Spalten:
- **Datum** (`goLiveDate` oder `estimatedGoLiveDate`, je nachdem welches näher liegt) — mit Dringlichkeits-Färbung:
  - 🔴 Rot = unter 3 Wochen
  - 🟠 Orange = 3–6 Wochen
  - 🟡 Gelb = 6–10 Wochen
- **RequestID** — klickbar, verlinkt zur entsprechenden Zeile in `kbv_uebersicht.html` (Anker `#requestId`)
- **Name / Use Case** (`botName`)
- **LOB**
- **KBV-Ampel** (ROT / GELB / GRÜN — gleiche Logik wie in der Übersicht)
- **Anmerkung** — ein Satz aus `addComments`, `WC_remarks` oder `historyComments` (erste befüllte Spalte, gekürzt auf ~100 Zeichen)

Oben auf der Seite: Anzahl der Cases + heutiges Datum als Hinweis „Stand: TT.MM.JJJJ".

---

## Kategorisierungs-Prototyp (`kategorisierung` / `analysiere` / flexibel)

Wenn der User **„kategorisierung"**, **„analysiere"**, **„erstelle proto"**, **„schau dir die Cases an"** oder ähnliches schreibt — oder einfach Cases nennt ohne expliziten Befehl — immer die Kategorisierungs-Analyse erstellen. Der Befehl ist bewusst flexibel gehalten.

- **Screenshot** → Proto mit genau den im Bild sichtbaren Cases erstellen.
- **„letzte Woche bis IRPA-RXXX"** (oder INTAI-ID) → Delta-Modus: neue Excel einlesen, Standard-Filter, alle Cases ab der genannten ID aufwärts, Proto erstellen.
- **Beides zusammen** (Screenshot + „letzte Woche bis...") → Eine Proto-Datei mit zwei Abschnitten: oben „My Action Required" (Cases aus dem Screenshot), darunter „Neue Cases seit letzter Woche" (Delta aus Excel). Jeder Abschnitt hat eigene Überschrift, gleiches Layout und Design.



- **Ohne Angabe von Cases:** Die 15 neuesten Cases aus der Excel (Standard-Filter, nach `dataCreated` DESC)
- **Mit Angabe von Cases:** Wenn der User konkrete IDs nennt (z.B. `kategorisierung IRPA-R2487 IRPA-R2312` oder `kategorisierung INTAI-1688 INTAI-2091`), dann **nur diese Cases** analysieren — keine Excel-Filterung, stattdessen die genannten Cases direkt per JIRA MCP abrufen bzw. aus der Excel suchen. Die Anzahl ist dabei unbegrenzt.
- **Mit Bild(ern):** Wenn der User ein oder mehrere Bilder einfügt (Screenshot eines JIRA-Tickets, Excel-Ausschnitt, E-Mail, Dokument), die relevanten Informationen **direkt aus den Bildern** extrahieren und für die Analyse nutzen — kein JIRA-Abruf nötig, sofern alle Informationen im Bild enthalten sind. Mehrere Bilder werden kombiniert ausgewertet. IDs und Textangaben aus Bildern werden genauso behandelt wie direkt eingetippte.

1. Die **neueste \*.xlsx** einlesen (Sheet: "SAPUI5 Export") — gleiche Datei und Filter wie bei `übersicht`.
2. **Excel-Filter (Standard)** anwenden (nur im Modus „ohne Angabe"): botStatusId = In Development, servicePackageId 1–4, technologiesId = `Artificial Intelligence` oder `Joule Studio Agent`, 15 neueste Einträge.
3. Für jeden Eintrag: falls eine JIRA-Ticket-ID in `botName` enthalten ist (oder direkt genannt wurde), das Ticket per Jira MCP abrufen.
4. Jeden Case vollständig analysieren und **KBV-Kategorie (S / M / L)** bestimmen.
5. Die Datei `kbv_kategorisierung_proto.html` vollständig neu schreiben.

### Design & Layout (verbindlich)

Die HTML-Datei folgt immer diesem Design — nicht ändern außer der User bittet explizit darum:

**Header:** Dunkler Gradient (`#1a1a2e → #16213e`), links Titel + Stat-Badges, rechts oben Live-Suchfeld (sucht nach Titel, Case-ID, JIRA-ID).

**Cases — standardmäßig eingeklappt:** Jede Card zeigt nur Kategorie-Badge, Titel, Case-ID, JIRA-Link, Meta-Tags, Chevron `▶` rechts. Klick auf Header klappt auf/zu. JIRA-Link und Gutachten-Button mit `event.stopPropagation()`.

**Aufgeklappter Inhalt:** 2-spaltiges Karten-Grid (Personenbezogene Daten blau + Auswirkungen auf Mitarbeitende lila) → **kein** „Fehlende KBV-Pflichtpunkte"-Block → Mitigation-Block (2-spaltig bei S, 3-spaltig bei M/L) → Gutachten-Button mit `white-space: pre-wrap` Fließtext.

**Style:** Hintergrund `#f1f4f8`, weiße Cards, System-Font, 14px, responsive (unter 700px single-column), keine externen Frameworks.

### Ausgabe-Struktur pro Case (verbindlich)

**Jeder Case besteht aus zwei Ebenen:**

#### Ebene 1 — Strukturierte Karten (immer sichtbar)

**Kopfzeile:**
- Titel (`botName`), RequestID, JIRA-Link (falls vorhanden), LOB, Service Package, Go-Live-Datum
- Kategorie-Badge groß rechts: **S** (grün) | **M** (gelb) | **L** (rot)

**Karte: Personenbezogene Daten** (mit blauem linken Rand — eigene Hervorhebung)
- Status-Tag: „Verarbeitung personenbezogener Daten" (blau) ODER „Keine direkte Verarbeitung" (grün)
- Bullet-Liste: welche Daten konkret, aus welchen Quellen, wie gespeichert/verarbeitet
- DPIA-Badge: „DPIA: erforderlich" (rot) | „DPIA: zu prüfen" (orange) | „DPIA: nicht erforderlich" (grün)

**Karte: Auswirkungen auf Mitarbeitende**
- Impact-Badge: HOCH (rot) | MITTEL (orange) | GERING (grün)
- Bullet-Liste: konkrete Auswirkungen auf Arbeitsabläufe und betroffene Personengruppen

**Mitigationsmaßnahmen-Block:**
- Abschnitt „✓ Bereits implementiert / geplant" (grün)
- Abschnitt „→ Empfohlen (noch offen)" (orange)
- Abschnitt „↑ Möglicher Weg zu Kategorie S" (blau) — nur bei Kategorie M oder L

**Fehlende KBV-Pflichtpunkte** (roter Block):
- Liste aller laut KBV noch fehlenden Maßnahmen

#### Ebene 2 — Vollständiges Gutachten (aufklappbar)

Button „Vollständiges Gutachten anzeigen" am unteren Rand des Case — klappt auf/zu, Chevron dreht sich.

**Inhalt des Gutachtens — verbindliches Beispiel als Template:**

Das Gutachten folgt exakt dieser Struktur und diesem Stil (angepasst auf den jeweiligen Case):

```
Kategorisierung: Kategorie M
Der KI-Anwendungsfall "AI-Assisted Large Scale Refactoring" fällt in Kategorie M
basierend auf folgender Analyse:

Begründung der Kategorisierung

1. Verarbeitung personenbezogener Daten
Mitarbeiterdaten im Arbeitsprozess: Die Lösung verarbeitet personenbezogene Daten
von Mitarbeitenden im Arbeitsprozess selbst, da:
- Code-Commits und Pull Requests mit Entwickler-Identitäten verknüpft werden
- Die Moderne-Plattform Dashboard-Tracking der Recipe-Ausführung und Fortschritte
  einzelner Entwickler ermöglicht
- Entwickleraktivitäten und -leistungen durch das System erfasst und ausgewertet
  werden können

2. Auswirkungen auf Arbeitsprozesse
Überschaubare bis wenige Auswirkungen auf konkrete Aufgaben:
- Unterstützung und teilweise Übernahme von Coding-Aufgaben durch KI
- Vereinfachung von Refactoring-Tätigkeiten
- Änderung bestehender Entwicklungsprozesse durch Automatisierung
- Jedoch keine vollständige Übernahme kompletter Aufgabenbereiche

Erforderliche Mitigationsmaßnahmen
Folgende Mitigationsmaßnahmen sollten implementiert werden:

1. Bereits geplante/implementierte Maßnahmen:
- Technische Safeguards: Kombination von AI mit AST-basierten Tools zur
  Minimierung von Halluzinationen
- Human-in-the-Loop: Entwickler reviewen alle Änderungen über Pull Requests
  in GitHub
- Schrittweise Einführung: Fokus zunächst auf Moderne-Implementierung,
  AI-Features werden sukzessive eingeführt

2. Empfohlene zusätzliche Mitigationsmaßnahmen:
- Schulungen/Enablement: Umfassendes Training für Entwickler zur Nutzung der
  AI-gestützten Refactoring-Tools
- Datenschutz-Compliance: Bestätigung der Einhaltung datenschutzrechtlicher
  Vorgaben, insbesondere bezüglich der Verarbeitung von Entwickler-Identitäten
- Nutzungsrichtlinien: Klare Guidelines für den Einsatz der AI-Funktionalitäten
- Beschwerdestelle: Etablierung einer Anlaufstelle für Entwickler bei Problemen
  oder Bedenken

3. Mögliche Mitigation zur Kategorie S:
Der Anwendungsfall könnte in Kategorie S eingeordnet werden, wenn:
- Ein Disclaimer implementiert wird, der die AI-Unterstützung als reine
  Beratungs-/Vorschlagsfunktion kennzeichnet
- Umfassendes Enablement (Schulungsangebote) bereitgestellt wird
- Die Verarbeitung von Entwickler-Identitäten auf reine Authentifizierung
  beschränkt wird

Fazit
Die Kategorisierung als Kategorie M ist angemessen, da personenbezogene
Mitarbeiterdaten im Arbeitsprozess verarbeitet werden und überschaubare
Auswirkungen auf Entwicklungsaufgaben bestehen. Die vorgeschlagenen
Mitigationsmaßnahmen können das Risiko weiter reduzieren und bei entsprechender
Umsetzung möglicherweise eine Einstufung in Kategorie S ermöglichen.
```

**Regeln für das Gutachten:**
- Abschnitt 1 beginnt immer mit einer Unterüberschrift die den Kernbefund benennt (z.B. „Mitarbeiterdaten im Arbeitsprozess:" oder „Keine Verarbeitung personenbezogener Daten:")
- Abschnitt 2 beginnt immer mit einer Einschätzung der Eingriffstiefe (z.B. „Überschaubare bis wenige Auswirkungen..." oder „Erhebliche Auswirkungen...")
- Mitigationsmaßnahmen immer dreigeteilt: bereits implementiert → empfohlen → Weg zu S (Abschnitt 3 nur bei Kategorie M oder L)
- Fazit: 2–3 Sätze, direkt, ohne Floskeln — Begründung der Kategorie + Mitigationspotenzial
- **Fazit-Styling:** Kategorie S → grün hervorgehoben | Kategorie M → gelb | Kategorie L → rot

### Kategorisierungslogik

- **Kategorie S:** Keine personenbezogenen Mitarbeiterdaten im Arbeitsprozess ODER reine Authentifizierungsdaten; geringe Auswirkung auf Aufgaben; Disclaimer + Enablement vorhanden oder leicht ergänzbar
- **Kategorie M:** Personenbezogene Mitarbeiterdaten im Arbeitsprozess; überschaubare bis mittlere Auswirkung; keine vollständige Aufgabenübernahme
- **Kategorie L:** Weitreichende personenbezogene Datenverarbeitung; hohe Auswirkung auf Arbeitsabläufe; Entscheidungsersatz durch KI; starke Leistungs-/Verhaltenskontrolle möglich

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
