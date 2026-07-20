# MISTA — Mitigation & Impact Screening Tool for AI

Analysiert KI-Use-Cases aus dem IUCR anhand der **Interims-Konzernbetriebsvereinbarung über KI (Stand: 31.10.2025)** und erstellt eine interaktive HTML-Auswertung mit Kategorisierung S / M / L.

> **MISTA** = *Mitigation & Impact Screening Tool for AI*

---

## Voraussetzungen

- **Claude Code**
- **JIRA MCP** verbunden
- **IUCR MCP** verbunden

---

## MCP einrichten

Das Tool ruft IUCR und JIRA automatisch per MCP ab. Einmalig im Browser authentifizieren:

- **IUCR:** [iucr-mcp.cfapps.eu10.hana.ondemand.com](https://iucr-mcp.cfapps.eu10.hana.ondemand.com)
- **JIRA:** [mcp.jira.tools.sap/mcp](https://mcp.jira.tools.sap/mcp)

Die `.mcp.json` im Projektverzeichnis liegt bereits vor — kein weiterer Schritt nötig.

---

## Verzeichnisstruktur

```
IUCR-Analyse/
├── data/                        ← Excel-Fallback (falls MCP nicht verfügbar)
├── mista_DDMMYYYY.html          ← Ausgabedatei (wird bei jeder Erstellung ersetzt)
├── CLAUDE.md                    ← Projektregeln (nicht ändern)
└── .mcp.json / .env             ← Konfiguration
```

---

## Cases analysieren

Einfach natürlich formulieren:

| Eingabe | Was passiert |
|---|---|
| `los` | My Action Required Cases (WoCCo-Filter) |
| `los, + 10 neueste` | My Action Required + 10 neueste Cases |
| `analysiere IRPA-R2487` | Genau dieser Case |
| `analysiere INTAI-1688` | Per JIRA-ID |
| Screenshot einfügen | Genau die Cases im Bild analysieren |

---

## Was die HTML-Datei zeigt

**Eingeklappt** (Übersicht):
- Kategorie-Badge **S** (grün) / **M** (gelb) / **L** (rot)
- Case-Titel, Case-ID, JIRA-Link, WoCCo-Status

**Aufgeklappt** (nach Klick auf Header):

| Bereich | Inhalt |
|---|---|
| Personenbezogene Daten (blau) | Welche Daten verarbeitet werden |
| Auswirkungen auf Mitarbeitende (lila) | Eingriffstiefe |
| Mitigationsmaßnahmen | Bereits geplant · Empfohlen · Weg zu S |
| Vollständiges Gutachten | Fließtext im KBV-Format, separat aufklappbar |

**Suche** oben rechts filtert live nach Titel, Case-ID und JIRA-ID.

---

## Kategorisierungslogik

| Kategorie | Personenbezogene Daten | Auswirkungen |
|---|---|---|
| **S** | Keine / nur Authentifizierung | Gering — Assistenzfunktion |
| **M** | Mitarbeiterdaten im Arbeitsprozess | Mittel — Kernaufgaben teilweise betroffen |
| **L** | Weitreichend / sensibel | Hoch — Aufgabenersatz oder Entscheidungsübernahme |

---

## Einzelticket-Analyse

JIRA-Nummer in den Chat schreiben (z.B. `INTAI-1688`) → vollständige KBV-Prüfung + E-Mail-Entwurf, kein HTML.

---

## Hinweise

- HTML-Datei ist vollständig offline nutzbar — kein Server nötig
- Weitergabe: Datei als Anhang per Mail oder Teams
- Gutachten-Texte sind keine Rechtsmeinung — interne Arbeitshilfe auf Basis der Interims-KBV

