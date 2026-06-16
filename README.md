# IUCR KBV-Analyse Tool

Dieses Tool analysiert IUCR Use Cases automatisch auf KBV-Compliance (SAP Interims-Konzernbetriebsvereinbarung über KI, Stand 31.10.2025) und erstellt eine interaktive HTML-Übersicht mit E-Mail-Entwürfen.

---

## Voraussetzungen

- **Claude Code** installiert und gestartet
- **Jira MCP-Server** konfiguriert (für JIRA-Ticket-Abruf)
- Excel-Exportdatei aus dem IUCR-System im Projektverzeichnis

---

## Setup

1. Repository klonen:
   ```
   git clone https://github.com/ThaubanNasr/IUCR-Analyse.git
   ```
2. Verzeichnis in Claude Code öffnen
3. Neue IUCR-Excel-Datei ins Verzeichnis legen (Dateiname muss mit `IUCR_` beginnen, z.B. `IUCR_15June.xlsx`)

---

## Nutzung

### Einzelanalyse eines JIRA-Tickets

Einfach die Ticketnummer eingeben — mit oder ohne Bindestrich, groß oder klein:

```
INTAI-2481
2481
intai 2481
```

Claude analysiert automatisch:
- Inhalt des Tickets
- Personenbezogene Daten (→ DPIA erforderlich?)
- Leistungs- und Verhaltenskontrolle (→ Nutzungsausschluss nötig?)
- Fehlende KBV-Pflichtpunkte
- Fertiger E-Mail-Entwurf an den Assignee

---

### Übersicht erstellen

```
übersicht
```

Claude:
1. Liest automatisch die **neueste IUCR_*.xlsx** im Verzeichnis ein
2. Filtert nach: Status = In Development, Service Package 1–4, Technologie = Artificial Intelligence oder Joule Studio Agent
3. Nimmt die 15 neuesten Einträge
4. Ruft verlinkte JIRA-Tickets ab (falls in `botName` enthalten)
5. Analysiert alle 15 Cases **parallel** (dauert ca. 2–3 Minuten)
6. Schreibt `kbv_uebersicht.html` neu

---

### HTML-Übersicht öffnen

Die Datei `kbv_uebersicht.html` im Browser öffnen.

**Funktionen:**
- Kompakte Tabelle mit allen Cases (RequestID, Name, LOB, Ampel)
- Klick auf eine Zeile → Detailansicht mit:
  - Personenbezogene Daten + DPIA-Status
  - Leistungs-/Verhaltenskontrolle (HOCH / MITTEL / GERING)
  - Fehlende KBV-Pflichtpunkte
  - E-Mail-Entwurf
- **„In Outlook öffnen"** → öffnet fertigen Entwurf in Outlook (nichts wird automatisch versendet)
- **„Kopieren"** → kopiert Betreff + Text in die Zwischenablage

---

## Neue Excel-Datei verwenden

1. Neue IUCR-Excel-Exportdatei ins Projektverzeichnis legen (Name muss mit `IUCR_` beginnen)
2. `übersicht` eingeben → Claude nimmt automatisch die neueste Datei

---

## Ampel-Logik

| Ampel | Bedeutung |
|---|---|
| 🔴 ROT | Kritische KBV-Lücken — sofortiger Handlungsbedarf |
| 🟡 GELB | Kleinere Lücken — Nachbesserung nötig |
| 🟢 OK | Keine wesentlichen offenen Pflichtpunkte |

---

## Was wird geprüft (KBV-Pflichtpunkte)

- DPIA (Datenschutzfolgeabschätzung) beantragt?
- Nutzungsausschluss für Leistungs- und Verhaltenskontrolle dokumentiert?
- Personenbezogene Daten vollständig beschrieben?
- IUCR-Eintrag vollständig?
- Disclaimer für Endnutzer vorhanden?
- Mitigationsmaßnahmen beschrieben?

---

## Regeln & Konfiguration

Alle Regeln sind in `CLAUDE.md` im Projektverzeichnis dokumentiert — Filter, HTML-Layout, E-Mail-Stil, KBV-Prüflogik.
