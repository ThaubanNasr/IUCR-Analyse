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

Das Tool ruft IUCR und JIRA automatisch per MCP ab. Die `.mcp.json` liegt bereits vor.

**MCP-Server hinzufügen (einmalig, im Claude Code Terminal):**

```bash
# IUCR
claude mcp add --transport http iucr-mcp-prod https://iucr-mcp.cfapps.eu10.hana.ondemand.com/mcp

# JIRA
claude mcp add --transport http sap-jira https://mcp.jira.tools.sap/mcp
```

Beim ersten Aufruf öffnet sich ein Browser-Fenster zur SAP SSO-Authentifizierung — einmalig bestätigen, danach läuft es automatisch.

---

## Cases analysieren

Einfach natürlich formulieren — kein festes Schlüsselwort nötig. Claude erkennt aus dem Kontext was gemeint ist und fragt bei Unklarheit nach.

| Eingabe | Was passiert |
|---|---|
| `los` / `mach` / `erstell` | My Action Required Cases (WoCCo-Filter) |
| `+ 10 neueste` | My Action Required + 10 neueste Cases |
| `IRPA-R2487` | Genau dieser Case |
| `INTAI-1688` | Per JIRA-ID |
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

## Hinweise

- HTML-Datei ist vollständig offline nutzbar — kein Server nötig
- Weitergabe: Datei als Anhang per Mail oder Teams
- Gutachten-Texte sind keine Rechtsmeinung — interne Arbeitshilfe auf Basis der Interims-KBV

---

## Fallback — wenn IUCR MCP nicht verfügbar ist

1. Excel-Export aus dem IUCR herunterladen und in den Ordner `data/` legen
2. Claude entweder einen Screenshot der gewünschten Cases geben oder die Case-IDs / JIRA-IDs direkt nennen
3. Claude liest die Excel aus und erstellt die MISTA wie gewohnt

