# IUCR KBV-Analyse Tool

Dieses Tool analysiert IUCR Use Cases automatisch auf KBV-Compliance (SAP Interims-Konzernbetriebsvereinbarung über KI, Stand 31.10.2025) und erstellt eine interaktive HTML-Übersicht mit E-Mail-Entwürfen.

---

## Voraussetzungen

- **Claude Code** installiert ([Download](https://claude.ai/download))
- SAP VPN aktiv (bei Remote-Arbeit)
- SAP Jira Account
- Excel-Exportdatei aus dem IUCR-System

---

## Setup

### Schritt 1: Repository klonen

```
git clone https://github.com/ThaubanNasr/IUCR-Analyse.git
```

Dann das Verzeichnis in Claude Code öffnen.

### Schritt 2: Jira MCP einrichten

Einmalig im Terminal ausführen:

```
claude mcp add sap-jira --transport http https://mcp.jira.tools.sap/mcp
```

Beim ersten Aufruf öffnet sich ein Browser-Fenster zur OAuth-Anmeldung mit dem SAP-Jira-Account — einmalig bestätigen, danach läuft die Authentifizierung automatisch.

**Verbindung testen** — in Claude Code eingeben:

```
Zeige mir meine letzten Jira-Tickets
```

Wenn Daten zurückkommen, ist alles korrekt eingerichtet.

> **Hinweis:** Bei „Project not found"-Fehlern muss der Projektadmin den technischen User `jira-mcp` zum Projekt hinzufügen.

### Schritt 3: Excel-Datei ins Verzeichnis legen

Die aktuelle IUCR-Exportdatei ins Projektverzeichnis kopieren. Der Dateiname muss mit `IUCR_` beginnen, z.B. `IUCR_15June.xlsx`.

---

## Nutzung

### Übersicht erstellen

```
übersicht
```

Claude liest automatisch die neueste `IUCR_*.xlsx` ein, analysiert die 15 neuesten Use Cases (gefiltert nach KI-Technologie, Status „In Development", Service Package 1–4) und schreibt die Datei `kbv_uebersicht.html` neu. Dauert ca. 2–3 Minuten.

### HTML-Übersicht öffnen

Die Datei `kbv_uebersicht.html` im Browser öffnen.

- Kompakte Tabelle mit allen Cases (RequestID, Name, LOB, Ampel)
- Klick auf eine Zeile → Detailansicht mit personenbezogenen Daten, Leistungs-/Verhaltenskontrolle und fehlenden KBV-Pflichtpunkten
- **„In Outlook öffnen"** → öffnet fertigen E-Mail-Entwurf in Outlook (nichts wird automatisch versendet)
- **„Kopieren"** → kopiert Betreff + Text in die Zwischenablage

### Einzelanalyse eines JIRA-Tickets

Einfach die Ticketnummer eingeben — mit oder ohne Bindestrich, groß oder klein:

```
INTAI-2481
2481
intai 2481
```

Claude analysiert automatisch Inhalt, personenbezogene Daten, Leistungs-/Verhaltenskontrolle, fehlende KBV-Pflichtpunkte und erstellt einen fertigen E-Mail-Entwurf.

### Neue Excel-Datei verwenden

Neue IUCR-Exportdatei ins Projektverzeichnis legen (Name muss mit `IUCR_` beginnen), dann `übersicht` eingeben — Claude nimmt automatisch die neueste Datei.

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
