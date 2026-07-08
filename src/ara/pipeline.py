from __future__ import annotations

import hashlib
from pathlib import Path

from .models import Case, Artifact, Evidence, EvidenceKind, Finding, NextAction, TaskStatus
from .evidence import stable_id


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def init_case(apk_path: str, out_root: str = "cases") -> Case:
    apk = Path(apk_path)
    digest = sha256_file(apk) if apk.exists() else hashlib.sha256(str(apk).encode()).hexdigest()
    case_id = f"apk_{digest[:12]}"
    workdir = Path(out_root) / case_id
    for sub in ["artifacts", "evidence", "reports", "scripts", "workspace"]:
        (workdir / sub).mkdir(parents=True, exist_ok=True)

    case = Case(case_id=case_id, apk_path=str(apk), workdir=str(workdir), status=TaskStatus.pending)
    case.artifacts.append(Artifact(name="input_apk", path=str(apk), kind="apk", description="Input APK sample"))
    case.evidence.append(Evidence(
        id=stable_id("ev", case_id, "sha256"),
        kind=EvidenceKind.unknown,
        source="init_case",
        location=str(apk),
        summary=f"APK SHA256: {digest}",
        confidence=1.0,
        tags=["hash", "sample"],
    ))

    case.next_actions.extend([
        NextAction(id=stable_id("act", case_id, "run_apktool"), title="Run apktool decode", action_type="run_apktool", reason="Decode manifest, resources and smali for static analysis"),
        NextAction(id=stable_id("act", case_id, "run_jadx"), title="Run jadx decompile", action_type="run_jadx", reason="Recover Java/Kotlin source for field and protocol analysis"),
        NextAction(id=stable_id("act", case_id, "scan_protocol"), title="Scan protocol-related code", action_type="scan_protocol", reason="Locate network endpoints, payload builders and key fields"),
        NextAction(id=stable_id("act", case_id, "scan_native"), title="Scan native libraries and JNI", action_type="scan_native", reason="Locate native methods, JNI_OnLoad and RegisterNatives candidates"),
    ])

    case.save(workdir / "case.json")
    return case


def build_initial_plan(case: Case) -> list[str]:
    return [
        "Decode APK with apktool and extract AndroidManifest.xml.",
        "Decompile Java/Kotlin with jadx.",
        "Scan network libraries, endpoints and payload builders.",
        "Build field trace for sign/token/device/fingerprint/timestamp/nonce.",
        "Locate native declarations and System.loadLibrary calls.",
        "Analyze JNI_OnLoad and RegisterNatives in native libraries.",
        "Prepare Frida trace scripts for protocol, crypto and JNI observation.",
        "If VMP evidence exists, trace dispatcher/opcode/handler table.",
        "Generate solver or reproduction script only after evidence is verified.",
        "Emit report.md and writeup.md.",
    ]


def analyze_stub(apk_path: str, out: str) -> Case:
    case = init_case(apk_path, out)
    case.status = TaskStatus.success
    report_dir = Path(case.workdir) / "reports"
    report = report_dir / "initial_plan.md"
    report.write_text("# Initial Analysis Plan\n\n" + "\n".join(f"- {x}" for x in build_initial_plan(case)), encoding="utf-8")
    case.artifacts.append(Artifact(name="initial_plan", path=str(report), kind="markdown", description="Initial reverse analysis plan"))
    case.findings.append(Finding(
        id=stable_id("finding", case.case_id, "foundation"),
        title="Case initialized",
        category="workflow",
        summary="The case workspace and initial Android reverse workflow plan were generated.",
        confidence=1.0,
        severity="info",
    ))
    case.save(Path(case.workdir) / "case.json")
    return case
