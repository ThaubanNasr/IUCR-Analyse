# MISTA — Mitigation & Impact Screening Tool for AI

Analysiert KI-Use-Cases aus dem IUCR anhand der **Interims-Konzernbetriebsvereinbarung über KI (Stand: 31.10.2025)** und erstellt eine interaktive HTML-Auswertung mit Kategorisierung S / M / L.

> **MISTA** = *Mitigation & Impact Screening Tool for AI*

---

## Voraussetzungen

- **Claude Code**
- **JIRA MCP** verbunden (Einrichtung siehe unten)
- Excel-Export aus dem IUCR im Ordner `data/`

---

## JIRA MCP einrichten

Das Tool ruft JIRA-Tickets automatisch ab. Dafür muss der MCP-Server einmalig konfiguriert sein.

Die Datei `.mcp.json` im Projektverzeichnis muss folgendes enthalten:

```json
{
  "mcpServers": {
    "sap-jira": {
      "type": "http",
      "url": "https://mcp.jira.tools.sap/mcp"
    }
  }
}
```

**Einrichtung in Claude Code:**
1. Claude Code öffnen
2. In das Projektverzeichnis navigieren (`C:\Users\...\IUCR-Analyse`)
3. Die `.mcp.json` liegt bereits vor — kein weiterer Schritt nötig
4. Beim ersten JIRA-Abruf ggf. einmalig im Browser authentifizieren (SAP SSO)

> Falls JIRA nicht erreichbar ist, werden nur die Excel-Daten für die Analyse verwendet — die Kategorisierung funktioniert trotzdem, ist aber weniger präzise.

---

## Verzeichnisstruktur

```
IUCR-Analyse/
├── data/                        ← Excel hier ablegen
│   └── <beliebiger-name>.xlsx   ← neueste Datei wird automatisch verwendet
├── mista_DDMMYYYY.html          ← Ausgabedatei (Datum im Namen, z.B. mista_02072026.html)
├── CLAUDE.md                    ← Projektregeln (nicht ändern)
└── .mcp.json / .env             ← Konfiguration
```

---

## Cases analysieren

Einfach natürlich formulieren — kein festes Schlüsselwort nötig:

| Eingabe | Was passiert |
|---|---|
| `analysiere die 5 neuesten` | 5 neueste Cases aus Excel — Zahl frei wählbar |
| `analysiere IRPA-R2487` | Genau dieser Case |
| `analysiere IRPA-R2487 IRPA-R2312` | Mehrere Cases auf einmal |
| `analysiere INTAI-1688` | Per JIRA-ID (auch mehrere) |
| Screenshot einfügen | Genau die Cases im Bild analysieren |
| `letzte Woche bis IRPA-R2492` | Delta-Modus: alle neuen Cases ab dieser ID aufwärts |
| Screenshot + `letzte Woche bis IRPA-R2492` | Eine HTML mit zwei Abschnitten: My Action Required + neue Cases |

---

## Wöchentlicher Workflow

1. Neue Excel aus dem IUCR exportieren → in `data/` ablegen
2. Screenshot der „My Action Required"-Liste machen
3. Eingabe: Screenshot + `letzte Woche bis IRPA-RXXXX`
4. Claude erstellt eine HTML mit zwei Abschnitten:
   - **My Action Required** — Cases wo du handeln musst
   - **Neue Cases seit letzter Woche** — alle neuen seit der letzten Bearbeitung
5. `mista_DDMMYYYY.html` im Browser öffnen

---

## Was die HTML-Datei zeigt

**Eingeklappt** (Übersicht):
- Kategorie-Badge **S** (grün) / **M** (gelb) / **L** (rot)
- Case-Titel, Case-ID, JIRA-Link
- LOB, Service Package, Go-Live-Datum, WoCCo-Status

**Aufgeklappt** (nach Klick auf Header):

| Bereich | Inhalt |
|---|---|
| Personenbezogene Daten (blau) | Welche Daten, DPIA-Badge |
| Auswirkungen auf Mitarbeitende (lila) | Eingriffstiefe, Impact-Badge |
| Mitigationsmaßnahmen | ✓ Bereits geplant · → Offen · ↑ Weg zu S |
| Vollständiges Gutachten | Fließtext im KBV-Format, separat aufklappbar |

**Suche** oben rechts filtert live nach Titel, Case-ID und JIRA-ID.

---

## Kategorisierungslogik

| Kategorie | Personenbezogene Daten | Auswirkungen |
|---|---|---|
| **S** | Keine / nur Authentifizierung | Gering — Nebenaufgaben, Assistenzfunktion |
| **M** | Mitarbeiterdaten im Arbeitsprozess | Mittel — Kernaufgaben teilweise betroffen |
| **L** | Weitreichend / sensibel | Hoch — Aufgabenersatz oder Entscheidungsübernahme |

---

## Excel-Datenquelle

- Neueste `*.xlsx` im Ordner `data/` wird automatisch verwendet
- Dateiname egal — neue Excel einfach reinlegen
- Sheet muss „SAPUI5 Export" heißen

**Automatische Filter:** Status `In Development` · Service Package 1–4 · Technologie `Artificial Intelligence` oder `Joule Studio Agent`

---

## Einzelticket-Analyse

JIRA-Nummer in den Chat schreiben (z.B. `INTAI-1688`) → vollständige KBV-Prüfung + E-Mail-Entwurf, kein HTML.

---

## Hinweise

- HTML-Datei ist vollständig offline nutzbar — kein Server nötig
- Weitergabe: Datei als Anhang per Mail oder Teams
- Gutachten-Texte sind keine Rechtsmeinung — interne Arbeitshilfe auf Basis der Interims-KBV
