"""
KBV-Checker — tickettyp-agnostische Analyse.
Basiert auf KI-KBV (Oktober 2025) + IT-KRBV (November 2018).
"""

PLACEHOLDER = "insert your text here"

# ---------------------------------------------------------------------------
# KBV-Fragen
# Jede Frage hat:
#   question     — was wir den Ticket-Owner fragen (klar, direkt, kein Juristendeutsch)
#   context      — kurze Erklärung WARUM wir das brauchen (1 Satz, verständlich)
#   example      — konkretes Beispiel wie eine gute Antwort aussieht
#   signals_yes  — Keywords die signalisieren: Frage ist beantwortet (ja/nein egal)
#   only_if      — diese Frage nur stellen wenn eine andere Frage auch offen ist
# ---------------------------------------------------------------------------

KBV_QUESTIONS = [
    {
        "id": "affected_employees",
        "question": "Wer nutzt dieses System konkret — SAP-Mitarbeitende in Deutschland, externe Nutzer, oder beides?",
        "context": "Der Betriebsrat muss wissen ob SAP-Beschäftigte in Deutschland direkt betroffen sind — das entscheidet ob und wie das System mitbestimmungspflichtig ist.",
        "example": "z.B. \"Genutzt von ca. 500 SAP-Entwicklern in Deutschland\" oder \"Nur für externe Kunden, keine SAP-Mitarbeitenden betroffen\"",
        "signals_yes": ["employee", "mitarbeiter", "developer", "entwickler", "nutzer", "staff",
                        "user", "customer only", "external only", "keine mitarbeiter", "no employees",
                        "beschäftigte", "belegschaft"],
    },
    {
        "id": "personal_data",
        "question": "Verarbeitet das System personenbezogene Daten von Mitarbeitenden — und wenn ja, welche genau?",
        "context": "Schon eine User-ID oder ein Aktivitätslog gilt als personenbezogen. Die Antwort bestimmt maßgeblich in welche Kategorie (S, M oder L) der Use Case fällt.",
        "example": "z.B. \"Ja, User-ID und Anfrage-Logs werden 30 Tage gespeichert\" oder \"Nein, alle Daten sind anonymisiert bevor sie verarbeitet werden\"",
        "signals_yes": ["personal data", "personenbezogen", "user id", "user activity", "employee data",
                        "no personal data", "keine personenbezogenen", "anonymized", "anonymisiert",
                        "authentication only", "nur authentifizierung", "keine nutzerdaten",
                        "pseudonymisiert", "pseudonymized"],
    },
    {
        "id": "data_purpose",
        "question": "Zu welchem Zweck werden die Mitarbeiterdaten genutzt — und ist sichergestellt dass sie nicht für andere Zwecke verwendet werden?",
        "context": "Daten dürfen laut IT-KRBV nur für den explizit vereinbarten Zweck genutzt werden. Der Zweck muss klar und begrenzt beschrieben sein.",
        "example": "z.B. \"Nur zur Personalisierung der IDE-Vorschläge, keine Weitergabe an Dritte, keine Nutzung für HR-Prozesse\"",
        "signals_yes": ["purpose", "zweck", "used for", "verarbeitet für", "verwendet für",
                        "data is used", "daten werden genutzt", "no data", "keine daten",
                        "only for", "ausschliesslich", "ausschließlich"],
        "only_if": "personal_data",
    },
    {
        "id": "performance_control",
        "question": "Könnte das System theoretisch dazu genutzt werden, die Leistung oder das Verhalten einzelner Mitarbeitender zu beobachten oder zu bewerten — auch wenn das nicht die Absicht ist?",
        "context": "Auch unbeabsichtigte Leistungs- oder Verhaltenskontrolle (LVK) ist mitbestimmungspflichtig. Falls möglich, braucht es einen expliziten Nutzungsausschluss.",
        "example": "z.B. \"Nein, es werden keine individuellen Nutzungsstatistiken erhoben\" oder \"Theoretisch möglich, daher Nutzungsausschluss: Das System darf nicht zur LVK verwendet werden\"",
        "signals_yes": ["no performance", "keine leistungskontrolle", "nutzungsausschluss", "kein monitoring",
                        "not used for performance", "nicht zur leistungskontrolle", "lvk ausgeschlossen",
                        "no individual", "keine individuelle", "aggregated only", "nur aggregiert",
                        "performance control", "leistungskontrolle", "verhaltenskontrolle",
                        "monitoring", "tracking", "überwachung"],
    },
    {
        "id": "logs",
        "question": "Werden Nutzungsdaten oder Logs gespeichert — und wenn ja, für welchen Zweck und wie lange?",
        "context": "Logs die Rückschlüsse auf einzelne Mitarbeitende erlauben dürfen laut IT-KRBV nur für definierte Zwecke (Betrieb, Datensicherung, Audit) genutzt werden — nicht zur Leistungsbewertung.",
        "example": "z.B. \"Technische Logs für 7 Tage zur Fehlerdiagnose, danach automatisch gelöscht\" oder \"Keine nutzerbezogenen Logs\"",
        "signals_yes": ["log", "protokoll", "audit", "trace", "history", "verlauf",
                        "no logs", "keine protokolle", "not logged", "wird nicht gespeichert",
                        "no logging", "kein logging", "deleted after", "gelöscht nach",
                        "retention", "aufbewahrung"],
    },
    {
        "id": "decision_autonomy",
        "question": "Trifft das System automatisch Entscheidungen oder gibt Empfehlungen ab — und hat der Mitarbeitende immer die Möglichkeit, diese zu ignorieren oder zu überschreiben?",
        "context": "KI-Systeme die eigenständig Entscheidungen über Mitarbeitende treffen (z.B. Aufgabenzuweisung, Bewertung) fallen in Kategorie L. Reine Vorschläge bei denen der Mensch entscheidet sind weniger kritisch.",
        "example": "z.B. \"Das System gibt nur Code-Vorschläge, die Entscheidung liegt immer beim Entwickler\" oder \"Das System weist Tickets automatisch zu — hier brauchen wir eine Mitigation\"",
        "signals_yes": ["human in the loop", "human-in-the-loop", "final decision by human",
                        "nur vorschlag", "suggestion only", "nur empfehlung", "recommendation only",
                        "autonomous", "autonom", "automated decision", "automatische entscheidung",
                        "entscheidet selbst", "assigns automatically", "weist zu"],
    },
    {
        "id": "dpia",
        "question": "Wurde bereits eine Datenschutzfolgeabschätzung (DPIA) durchgeführt oder ist eine geplant — und wo ist sie dokumentiert (PET on SPG)?",
        "context": "Bei KI-Systemen die personenbezogene Daten verarbeiten ist eine DPIA verpflichtend. Ohne Verweis auf die DPIA kann das PMO die Einreichung nicht abschließen.",
        "example": "z.B. \"DPIA läuft, Eintrag in PET on SPG unter Referenz XYZ\" oder \"DPIA nicht erforderlich, da keine personenbezogenen Daten verarbeitet werden\"",
        "signals_yes": ["dpia", "datenschutzfolgeabschätzung", "privacy impact", "pet on spg",
                        "procedure enrollment", "datenschutzprüfung", "no dpia", "kein dpia",
                        "not required", "nicht erforderlich", "spg", "privacy governance"],
        "only_if": "personal_data",
    },
    {
        "id": "mitigation",
        "question": "Sind Maßnahmen geplant um Risiken für Mitarbeitende zu reduzieren — z.B. ein Disclaimer, Schulungen, ein zeitlich begrenzter Pilot oder ein Nutzungsausschluss für bestimmte Szenarien?",
        "context": "Solche Mitigationsmaßnahmen können die Einstufung verbessern (z.B. von L auf M) und sind bei risikobehafteten Use Cases oft der entscheidende Faktor für eine schnelle Genehmigung.",
        "example": "z.B. \"Pilot mit 20 Entwicklern für 6 Monate, danach Evaluation\" oder \"Disclaimer: KI-Ergebnisse müssen vom Nutzer geprüft werden\" oder \"Keine Mitigation geplant\"",
        "signals_yes": ["disclaimer", "mitigation", "pilot", "nutzungsausschluss", "enablement",
                        "schulung", "training", "change management", "safeguard", "keine mitigation",
                        "no mitigation", "not applicable", "nicht erforderlich"],
    },
]

TEMPLATE_SECTIONS = [
    {"label": "Business Problem – Ist-Situation (From)",
     "markers": ["from (describe current situation)", "describe the underlying business problem"]},
    {"label": "Business Problem – Ziel-Situation (To)",
     "markers": ["to (describe target situation)", "describe your expected vision"]},
    {"label": "Target Users",
     "markers": ["target users", "list target users"]},
    {"label": "Value Proposition",
     "markers": ["value proposition", "summarize the expected benefits"]},
    {"label": "AI/ML Job to be done",
     "markers": ["job to be done", "describe the objective that the ai"]},
    {"label": "Data Requirements",
     "markers": ["data requirements", "input data:", "output data:"]},
    {"label": "Integration & User Enablement",
     "markers": ["integration & user enablement", "describe where the ai prediction"]},
]


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _uses_intai_template(description: str) -> bool:
    markers = ["insert your text here", "titleBGColor=#0f70f2", "business problem description",
               "value proposition", "ai/ml", "job to be done"]
    desc_lower = description.lower()
    return sum(1 for m in markers if m in desc_lower) >= 2


def _section_filled(description: str, section: dict) -> bool:
    desc_lower = description.lower()
    for marker in section["markers"]:
        idx = desc_lower.find(marker.lower())
        if idx == -1:
            continue
        snippet = desc_lower[idx: idx + 600]
        if PLACEHOLDER.lower() in snippet:
            return False
        lines = [l.strip() for l in snippet.split("\n") if l.strip()]
        content = [l for l in lines
                   if not l.startswith("#")
                   and "instruction:" not in l
                   and len(l) > 25]
        if content:
            return True
    return True


def _is_answered(description: str, question: dict) -> bool:
    desc_lower = description.lower()
    return any(s.lower() in desc_lower for s in question["signals_yes"])


# ---------------------------------------------------------------------------
# Hauptanalyse
# ---------------------------------------------------------------------------

def analyze(issue: dict) -> dict:
    fields = issue.get("fields", {})
    description = fields.get("description") or ""
    issue_type = (fields.get("issuetype") or {}).get("name", "Unknown")

    missing_sections = []
    if _uses_intai_template(description):
        missing_sections = [
            s["label"]
            for s in TEMPLATE_SECTIONS
            if not _section_filled(description, s)
        ]

    open_questions = []
    unanswered_ids = set()
    for q in KBV_QUESTIONS:
        if "only_if" in q and q["only_if"] not in unanswered_ids:
            continue
        if not _is_answered(description, q):
            open_questions.append({
                "id": q["id"],
                "question": q["question"],
                "context": q["context"],
                "example": q["example"],
            })
            unanswered_ids.add(q["id"])

    return {
        "key": issue["key"],
        "summary": fields.get("summary", ""),
        "issue_type": issue_type,
        "missing_sections": missing_sections,
        "open_questions": open_questions,
        "has_issues": bool(missing_sections or open_questions),
    }


# ---------------------------------------------------------------------------
# Mail-Text — variabel je nach Inhalt, verständlich ohne Vorkenntnisse
# ---------------------------------------------------------------------------

def format_mail_body(assignee_name: str, issue_key: str, summary: str,
                     result: dict, jira_base_url: str) -> str:
    issue_type = result.get("issue_type", "Ticket")
    missing = result["missing_sections"]
    questions = result["open_questions"]
    first_name = assignee_name.split(",")[-1].strip() if "," in assignee_name else assignee_name.split()[0]

    lines = [f"Hallo {first_name},", ""]

    # Intro — kontextabhängig
    if missing and questions:
        lines += [
            f"ich schaue gerade den Use Case \"{summary}\" ({issue_key}) durch,",
            "damit wir ihn beim Betriebsrat einreichen können.",
            "",
            "Dabei sind mir zwei Dinge aufgefallen: Ein paar Abschnitte im Ticket",
            "sind noch nicht ausgefüllt, und es gibt Fragen die ich für die",
            "Kategorisierung (S/M/L) noch nicht beantworten kann.",
        ]
    elif missing:
        lines += [
            f"ich schaue gerade den Use Case \"{summary}\" ({issue_key}) durch,",
            "damit wir ihn beim Betriebsrat einreichen können.",
            "",
            "Ein paar Abschnitte im Ticket sind noch nicht ausgefüllt —",
            "ohne diese kann das PMO die Einreichung nicht vorbereiten.",
        ]
    else:
        lines += [
            f"ich schaue gerade den Use Case \"{summary}\" ({issue_key}) durch,",
            "damit wir ihn beim Betriebsrat einreichen können.",
            "",
            "Das Ticket ist inhaltlich gut ausgefüllt, aber für die Kategorisierung",
            "nach KI-KBV fehlen mir noch ein paar Angaben die ich im Ticket",
            "nicht eindeutig beantworten kann.",
        ]

    lines.append("")

    # Fehlende Template-Abschnitte
    if missing:
        if len(missing) == 1:
            lines += [
                "NOCH AUSZUFÜLLEN:",
                f"  - {missing[0]}",
            ]
        else:
            lines += ["NOCH AUSZUFÜLLEN:"]
            for s in missing:
                lines.append(f"  - {s}")
        lines.append("")

    # Offene KBV-Fragen — jede mit Kontext und Beispiel
    if questions:
        lines += [
            "OFFENE FRAGEN:",
            "Könntest du folgende Punkte direkt im Ticket ergänzen",
            "(z.B. unter Data Requirements oder Integration & User Enablement)?",
            "",
        ]
        for i, q in enumerate(questions, 1):
            lines += [
                f"{i}. {q['question']}",
                f"   Warum das wichtig ist: {q['context']}",
                f"   Beispiel: {q['example']}",
                "",
            ]

    lines += [
        f"Ticket: {jira_base_url}/{issue_key}",
        "",
        "Danke und viele Grüße",
    ]

    return "\n".join(lines)
