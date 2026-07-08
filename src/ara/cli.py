from __future__ import annotations

from pathlib import Path
import click
from rich.console import Console
from rich.table import Table

from .models import Case
from .pipeline import init_case, analyze_stub
from .report import write_report


console = Console()


@click.group()
def main():
    """Android Reverse Agent CLI."""
    pass


@main.command("init-case")
@click.argument("apk_path")
@click.option("--out", default="cases", help="Output case root directory.")
def cmd_init_case(apk_path: str, out: str):
    """Create a case workspace."""
    case = init_case(apk_path, out)
    console.print(f"[green]Created case:[/green] {case.case_id}")
    console.print(f"Case file: {Path(case.workdir) / 'case.json'}")


@main.command("analyze")
@click.argument("apk_path")
@click.option("--out", default="cases", help="Output case root directory.")
def cmd_analyze(apk_path: str, out: str):
    """Run the foundation analysis stub."""
    case = analyze_stub(apk_path, out)
    report = write_report(case)
    console.print(f"[green]Analysis foundation generated:[/green] {case.case_id}")
    console.print(f"Report: {report}")


@main.command("show-plan")
@click.argument("case_json")
def cmd_show_plan(case_json: str):
    """Show next actions from a case.json."""
    case = Case.load(case_json)
    table = Table(title=f"Next Actions: {case.case_id}")
    table.add_column("Status")
    table.add_column("Action")
    table.add_column("Reason")
    for act in case.next_actions:
        table.add_row(str(act.status.value), act.title, act.reason)
    console.print(table)


@main.command("emit-playbook")
@click.argument("topic", required=False)
def cmd_emit_playbook(topic: str | None):
    """Print a built-in topic checklist."""
    plans = {
        "protocol": [
            "Scan OkHttp/Retrofit/HttpURLConnection/WebSocket/Socket/gRPC.",
            "Identify endpoints, methods, headers and payload format.",
            "Trace JSON/Form/Protobuf builders.",
            "Locate sign/token/timestamp/nonce/device fields.",
            "Trace crypto APIs and native sign/encrypt methods.",
        ],
        "native": [
            "Find System.loadLibrary/System.load.",
            "List Java native methods.",
            "Inspect JNI_OnLoad.",
            "Resolve RegisterNatives table.",
            "Map Java signatures to native addresses.",
        ],
        "vmp": [
            "Find dispatcher loop.",
            "Identify opcode fetch and pc update.",
            "Find handler table and VM context.",
            "Trace opcode sequence.",
            "Annotate handler semantics and build solver.",
        ],
    }
    selected = plans.get(topic or "protocol", plans["protocol"])
    for item in selected:
        console.print(f"- {item}")
