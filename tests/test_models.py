from ara.models import Case, Evidence, EvidenceKind


def test_case_roundtrip(tmp_path):
    c = Case(case_id="demo", apk_path="demo.apk", workdir=str(tmp_path))
    c.evidence.append(Evidence(
        id="ev1",
        kind=EvidenceKind.java,
        source="test",
        summary="demo evidence",
    ))
    p = tmp_path / "case.json"
    c.save(p)
    loaded = Case.load(p)
    assert loaded.case_id == "demo"
    assert loaded.evidence[0].summary == "demo evidence"
