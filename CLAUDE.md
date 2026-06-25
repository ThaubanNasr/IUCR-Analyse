# CLAUDE.md — Projektregeln

## Sprache
Immer auf Deutsch antworten.

---

## Excel-Filter (Standard)
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

## Cases analysieren / Proto erstellen

Wenn der User **„analysiere"**, **„kategorisierung"**, **„erstelle proto"** oder ähnliches schreibt — oder einfach Cases nennt — immer die KBV-Kategorisierungs-Analyse erstellen und `kbv_kategorisierung_proto.html` neu schreiben.

### Modi — automatisch erkennen

- **Nur Screenshot** → Proto mit genau den im Bild sichtbaren Cases erstellen.
- **Nur „letzte Woche bis IRPA-RXXX"** (oder INTAI-ID) → Delta-Modus: Excel einlesen, Standard-Filter, alle Cases ab der genannten ID aufwärts, Proto erstellen. Keine Begrenzung auf 15.
- **Beides zusammen** (Screenshot + „letzte Woche bis...") → Eine Proto mit zwei Abschnitten: oben „My Action Required" (Cases aus Screenshot), darunter „Neue Cases seit letzter Woche" (Delta aus Excel).
- **Ohne Angabe** → 15 neueste Cases aus Excel (Standard-Filter)
- **Mit IDs** → Nur genannte Cases (IRPA-R... oder INTAI-...), Anzahl unbegrenzt
- **Mit Bild(ern)** → Informationen direkt aus dem Bild extrahieren, ggf. JIRA ergänzend abrufen

### Ablauf
1. Excel aus `data/` einlesen, Standard-Filter anwenden
2. JIRA-Tickets per MCP abrufen falls INTAI-ID vorhanden
3. Jeden Case vollständig analysieren → KBV-Kategorie S / M / L bestimmen
4. `kbv_kategorisierung_proto.html` vollständig neu schreiben

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

---

## JIRA-Einzelticket-Analyse

Wenn der User nur eine Ticketnummer nennt (z.B. „INTAI-1688"), automatisch vollständige KBV-Prüfung + E-Mail-Entwurf durchführen — ohne Rückfrage. Nur das direkt angefragte Ticket analysieren.

**KBV-Prüfung umfasst:**
- Welche personenbezogenen Daten werden verarbeitet? (→ DPIA erforderlich?)
- Ist Leistungs- oder Verhaltenskontrolle möglich? (→ Nutzungsausschluss nötig?)
- Was fehlt laut KBV (DPIA, Nutzungsausschluss, Disclaimer, Mitigationsmaßnahmen)?

KBV-Kategorisierung (S / M / L) nur wenn der User explizit danach fragt.

**E-Mail-Entwürfe:** Nur erstellen, nie ohne Genehmigung abschicken. Direkt mit offenen Punkten beginnen — keine Höflichkeitsfloskeln, keine Platzhalter für Deadlines.
