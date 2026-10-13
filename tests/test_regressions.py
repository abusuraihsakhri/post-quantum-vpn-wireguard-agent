"""Regression tests for input handling and signed audit-chain integrity."""
import csv
import pytest
from pydantic import ValidationError

from agents.base import AuditTrail
from agents.models import SystemTaskPayload
from cli import main
from pqc_wireguard.models import FrontierPayload


def test_audit_signature_rejects_modified_signed_field():
    trail = AuditTrail(secret_key="test-only-key")
    trail.log("supervisor", "tier", "ACTION", {"count": 1})
    assert trail.verify_integrity()
    trail.logs[0]["actor"] = "attacker"
    assert not trail.verify_integrity()


def test_audit_signature_rejects_rewritten_hash_chain():
    trail = AuditTrail(secret_key="test-only-key")
    trail.log("supervisor", "tier", "EVENT1", {"count": 1})
    trail.log("supervisor", "tier", "EVENT2", {"count": 2})
    trail.logs[0]["current_hash"] = "0" * 64
    trail.logs[1]["prev_hash"] = "0" * 64
    assert not trail.verify_integrity()


def test_audit_trail_snapshots_are_not_live_references():
    trail = AuditTrail(secret_key="test-only-key")
    entry = trail.log("supervisor", "tier", "ACTION", {"count": 1})
    entry["actor"] = "attacker"
    snapshot = trail.get_trail()
    snapshot[0]["actor"] = "attacker"
    snapshot.clear()
    assert trail.verify_integrity()
    assert len(trail.get_trail()) == 1


@pytest.mark.parametrize("value,expected", [
    ("False", "ROUTINE"),
    ("0", "ROUTINE"),
    ("", "ROUTINE"),
    ("True", "CRITICAL_STAT_PANIC"),
    ("1", "CRITICAL_STAT_PANIC"),
])
def test_batch_boolean_parsing(tmp_path, capsys, value, expected):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    with input_file.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "task_id", "target_identifier", "primary_metric", "secondary_metric",
            "status_descriptor", "is_critical_flag",
        ])
        writer.writeheader()
        writer.writerow({
            "task_id": "T1", "target_identifier": "K1", "primary_metric": "10",
            "secondary_metric": "4", "status_descriptor": "NOMINAL",
            "is_critical_flag": value,
        })
    assert main(["batch", "-i", str(input_file), "-o", str(output_file)]) == 0
    with output_file.open(newline="") as handle:
        row = next(csv.DictReader(handle))
    assert row["overall_urgency"] == expected


def test_batch_rejects_invalid_boolean(tmp_path):
    input_file = tmp_path / "input.csv"
    input_file.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag\\n"
        "T1,K1,10,4,perhaps\\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="Invalid is_critical_flag"):
        main(["batch", "-i", str(input_file), "-o", str(tmp_path / "out.csv")])


def test_batch_rejects_overwriting_input(tmp_path):
    path = tmp_path / "input.csv"
    path.write_text("task_id,primary_metric\\nT1,10\\n", encoding="utf-8")
    with pytest.raises(ValueError, match="different files"):
        main(["batch", "-i", str(path), "-o", str(path)])


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_models_reject_nonfinite_metrics(value):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="T1", target_identifier="K1", primary_metric=value)
    with pytest.raises(ValueError):
        FrontierPayload("T1", "K1", value, 4, "NOMINAL")
