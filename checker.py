"""
missingJira - KBV-Checker
Prüft INTAI-Tickets auf offene Fragen für die KBV-Einreichung beim Betriebsrat.
Nutzung:
  python checker.py INTAI-2527 INTAI-2528        # einzelne Tickets
  python checker.py --project INTAI --limit 20   # ganzes Projekt
  python checker.py INTAI-2527 --send            # Mail rausschicken
"""

import json
import re
import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path

import kbv_checker

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
JIRA_BASE_URL = "https://jira.tools.sap/browse"


def load_config():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def run_claude(prompt: str) -> str:
    result = subprocess.run(
        ["claude", "--dangerously-skip-permissions", "-p", prompt],
        capture_output=True, text=True, encoding="utf-8",
        cwd=str(SCRIPT_DIR), timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI Fehler: {result.stderr[:500]}")
    return result.stdout.strip()


def fetch_issue(issue_key: str) -> dict:
    prompt = (
        f"Rufe über den sap-jira MCP-Server das Jira-Ticket {issue_key} ab. "
        f"Gib NUR ein JSON-Objekt zurück (kein Markdown, kein Text) mit exakt dieser Struktur: "
        f"{{\"key\":\"INTAI-XXXX\",\"fields\":{{\"summary\":\"...\",\"description\":\"...\","
        f"\"assignee\":{{\"emailAddress\":\"...\",\"displayName\":\"...\"}},"
        f"\"reporter\":{{\"emailAddress\":\"...\",\"displayName\":\"...\"}},"
        f"\"issuetype\":{{\"name\":\"...\"}},"
        f"\"status\":{{\"name\":\"...\"}}}}}}"
    )
    raw = run_claude(prompt)
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise RuntimeError(f"Keine JSON-Antwort für {issue_key}: {raw[:200]}")
    return json.loads(match.group(0))


def fetch_issues_by_project(config: dict) -> list:
    projects = config["projects"]
    issue_types = config.get("issue_types", ["Feature", "Story", "Epic"])
    max_results = config.get("max_issues_per_run", 50)
    projects_jql = ", ".join(f'"{p}"' for p in projects)
    types_jql = ", ".join(f'"{t}"' for t in issue_types)
    jql = (f"project in ({projects_jql}) AND issuetype in ({types_jql}) "
           f"AND statusCategory != Done ORDER BY created DESC")
    prompt = (
        f"Führe über den sap-jira MCP-Server folgende JQL-Abfrage aus (Limit: {max_results}): {jql} "
        f"Gib NUR ein JSON-Array zurück (kein Markdown), jedes Element mit exakt dieser Struktur: "
        f"{{\"key\":\"...\",\"fields\":{{\"summary\":\"...\",\"description\":\"...\","
        f"\"assignee\":{{\"emailAddress\":\"...\",\"displayName\":\"...\"}},"
        f"\"reporter\":{{\"emailAddress\":\"...\",\"displayName\":\"...\"}},"
        f"\"issuetype\":{{\"name\":\"...\"}},"
        f"\"status\":{{\"name\":\"...\"}}}}}}"
    )
    raw = run_claude(prompt)
    match = re.search(r'\[.*\]', raw, re.DOTALL)
    if not match:
        raise RuntimeError(f"Keine JSON-Array-Antwort: {raw[:200]}")
    return json.loads(match.group(0))


def get_owner(issue: dict):
    for person in [issue.get("fields", {}).get("assignee"),
                   issue.get("fields", {}).get("reporter")]:
        if person and person.get("emailAddress"):
            return person["emailAddress"], person.get("displayName", "")
    return None, ""


def send_outlook(sender: str, to: str, subject: str, body: str):
    import win32com.client
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    mail.SentOnBehalfOfName = sender
    mail.To = to
    mail.Subject = subject
    mail.Body = body
    mail.Send()


def print_result(r: dict):
    print(f"\n[{r['key']}] {r['summary']}")
    if r["missing_sections"]:
        print(f"  Unvollstaendige Abschnitte ({len(r['missing_sections'])}):")
        for s in r["missing_sections"]:
            print(f"    - {s}")
    if r["open_questions"]:
        print(f"  Offene KBV-Fragen ({len(r['open_questions'])}):")
        for q in r["open_questions"]:
            print(f"    ? {q['question']}")
    email = r.get("email")
    print(f"  Owner: {r.get('name', '?')} <{email or 'keine Mail'}>")


def main():
    parser = argparse.ArgumentParser(
        description="KBV-Checker: Prüft Jira-Tickets auf offene KBV-Fragen",
        epilog="Beispiele:\n"
               "  python checker.py INTAI-2527\n"
               "  python checker.py INTAI-2527 INTAI-2528 --send\n"
               "  python checker.py --project INTAI --limit 10",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("tickets", nargs="*", help="Ticket-Nummern (z.B. INTAI-2527 INTAI-2528)")
    parser.add_argument("--project", help="Alle offenen Tickets eines Projekts prüfen")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--send", action="store_true", help="Echte Mails verschicken")
    args = parser.parse_args()

    config = load_config()
    if args.project:
        config["projects"] = [args.project]
    if args.limit:
        config["max_issues_per_run"] = args.limit

    dry_run = not args.send
    mode = "DRY-RUN" if dry_run else "LIVE - echte Mails!"
    print(f"\n=== KBV-Checker | {datetime.now().strftime('%Y-%m-%d %H:%M')} | {mode} ===")

    # Tickets laden
    if args.tickets:
        print(f"Lade {len(args.tickets)} Ticket(s): {', '.join(args.tickets)}")
        issues = []
        for key in args.tickets:
            try:
                issues.append(fetch_issue(key.strip()))
            except Exception as e:
                print(f"  FEHLER beim Laden von {key}: {e}")
    elif args.project or config.get("projects"):
        print(f"Lade Tickets aus Projekt(en): {', '.join(config['projects'])}")
        try:
            issues = fetch_issues_by_project(config)
        except Exception as e:
            print(f"  FEHLER: {e}")
            sys.exit(1)
        print(f"  {len(issues)} Tickets geladen.")
    else:
        parser.print_help()
        sys.exit(1)

    # Analysieren — nur konfigurierte Issue-Types
    allowed_types = [t.lower() for t in config.get("issue_types", ["feature", "story", "epic"])]
    results = []
    skipped_types = []
    for issue in issues:
        issue_type = (issue.get("fields", {}).get("issuetype") or {}).get("name", "")
        if issue_type.lower() not in allowed_types:
            skipped_types.append(f"{issue['key']} ({issue_type})")
            continue
        analysis = kbv_checker.analyze(issue)
        if analysis["has_issues"]:
            email, name = get_owner(issue)
            analysis["email"] = email
            analysis["name"] = name or email or "Unbekannt"
            results.append(analysis)

    if skipped_types:
        print(f"Uebersprungen (falscher Typ): {', '.join(skipped_types)}")

    if not results:
        print("\nAlle Tickets vollstaendig — keine offenen KBV-Fragen gefunden.")
        return

    print(f"\n{len(results)} Ticket(s) mit Handlungsbedarf:")
    for r in results:
        print_result(r)

    # Mails
    sender = config["email"]["sender"]
    sent = skipped = 0
    print()
    for r in results:
        if not r.get("email"):
            print(f"SKIP {r['key']}: keine E-Mail-Adresse")
            skipped += 1
            continue

        subject = f"Angaben für KBV-Einreichung fehlen: {r['key']} – {r['summary'][:50]}"
        body = kbv_checker.format_mail_body(
            r["name"], r["key"], r["summary"], r, JIRA_BASE_URL
        )

        if dry_run:
            print(f"[DRY-RUN] {r['key']} -> {r['email']}")
            print(f"  Betreff: {subject}")
            print("  --- Mail-Vorschau ---")
            print("\n".join("  " + l for l in body.splitlines()[:20]))
            if len(body.splitlines()) > 20:
                print(f"  ... ({len(body.splitlines()) - 20} weitere Zeilen)")
            print()
        else:
            try:
                send_outlook(sender, r["email"], subject, body)
                print(f"Mail gesendet: {r['key']} -> {r['email']}")
                sent += 1
            except Exception as e:
                print(f"FEHLER {r['key']}: {e}")
                skipped += 1

    print(f"\nFertig | {len(results)} Findings | {sent} Mails gesendet | {skipped} uebersprungen")

    # Report
    report = SCRIPT_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "checked": len(issues),
            "with_findings": len(results),
            "details": results
        }, f, ensure_ascii=False, indent=2)
    print(f"Report: {report.name}")


if __name__ == "__main__":
    main()
