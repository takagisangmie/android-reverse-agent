from __future__ import annotations

from pathlib import Path
from .models import Case


def render_markdown_report(case: Case) -> str:
    lines = [
        f"# Android Reverse Report: {case.case_id}",
        "",
        "## Sample",
        "",
        f"- APK: `{case.apk_path}`",
        f"- Workdir: `{case.workdir}`",
        f"- Package: `{case.package_name or 'unknown'}`",
        "",
        "## Findings",
        "",
    ]

    if not case.findings:
        lines.append("- No findings yet.")
    else:
        for item in case.findings:
            lines.extend([
                f"### {item.title}",
                "",
                f"- Category: `{item.category}`",
                f"- Severity: `{item.severity}`",
                f"- Confidence: `{item.confidence}`",
                f"- Summary: {item.summary}",
                "",
            ])

    lines.extend(["## Evidence", ""])
    if not case.evidence:
        lines.append("- No evidence yet.")
    else:
        for ev in case.evidence:
            lines.extend([
                f"### {ev.id}",
                "",
                f"- Kind: `{ev.kind}`",
                f"- Source: `{ev.source}`",
                f"- Location: `{ev.location}`",
                f"- Confidence: `{ev.confidence}`",
                f"- Summary: {ev.summary}",
                "",
            ])

    lines.extend(["## Next Actions", ""])
    if not case.next_actions:
        lines.append("- No next actions.")
    else:
        for act in case.next_actions:
            lines.append(f"- [{act.status}] **{act.title}**: {act.reason}")

    return "\n".join(lines) + "\n"


def write_report(case: Case) -> Path:
    out = Path(case.workdir) / "reports" / "report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown_report(case), encoding="utf-8")
    return out
