"""
Automated Pytest Test Suite for Post Quantum Vpn Wireguard Agent.
Domain: Post-Quantum Cryptography & Hardware Security
Standard: NIST FIPS 203/204/205 / ISO/IEC 17825 Standards
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException, AuditTrail
from agents.models import SystemTaskPayload, UrgencyLevel, SystemIntegrityStatus
from agents.workers import InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
from agents.supervisor import SystemSupervisor
from cli import main, _resolve_safe_path


def test_phi_guard_enforcement():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive for Staphylococcus")

    # Clean text passes
    PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")


def test_specialized_workers():
    # Worker 1: QC Invariant
    p1 = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=35.0)
    alerts1 = InvariantQCWorker.evaluate(p1)
    assert len(alerts1) == 1
    assert alerts1[0].urgency == UrgencyLevel.ELEVATED

    # Worker 2: Safety
    p2 = SystemTaskPayload(task_id="T2", target_identifier="KEY-02", primary_metric=10.0, is_critical_flag=True)
    alerts2 = SafetyEscalationWorker.evaluate(p2)
    assert len(alerts2) == 1
    assert alerts2[0].urgency == UrgencyLevel.CRITICAL_STAT

    # Worker 3: Protocol Conformance
    p3 = SystemTaskPayload(task_id="T3", target_identifier="KEY-03", primary_metric=10.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = ProtocolConformanceWorker.evaluate(p3)
    assert len(alerts3) == 1


def test_supervisor_consensus_and_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="TASK-PROD-01",
        target_identifier="KEY-PROD-01",
        primary_metric=12.0,
        secondary_metric=4.0,
        status_descriptor="NOMINAL"
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.ROUTINE
    assert dossier.integrity_status == SystemIntegrityStatus.VALIDATED
    assert dossier.audit_hash != ""

    # Verify cryptographic audit trail
    assert AuditLogger.verify_integrity() is True

    # CLI tests
    assert main(["audit", "--task-id", "CLI-TEST-01"]) == 0
    assert main(["chat", "Explain", "specifications"]) == 0
    assert main(["verify-audit"]) == 0


def test_resolve_safe_path_absolute():
    """Test that _resolve_safe_path returns absolute paths."""
    result = _resolve_safe_path("test.csv")
    assert result.is_absolute()


def test_resolve_safe_path_nonexistent_raises():
    """Test that _resolve_safe_path raises for non-existent files when must_exist=True."""
    with pytest.raises(FileNotFoundError):
        _resolve_safe_path("/nonexistent/path/to/file.csv", must_exist=True)


def test_audit_trail_with_explicit_key():
    """Test that AuditTrail accepts an explicit key."""
    trail = AuditTrail(secret_key="test-secret-key-2026")
    entry = trail.log("test", "test_tier", "TEST_EVENT", {"data": "value"})
    assert entry["current_hash"] != ""
    assert entry["prev_hash"] == "GENESIS_BLOCK_0000000000000000"
    assert trail.verify_integrity() is True


def test_audit_trail_chained_integrity():
    """Test that audit trail maintains chained integrity across multiple entries."""
    trail = AuditTrail(secret_key="chain-test-key")
    trail.log("actor1", "tier1", "EVENT_1", {"seq": 1})
    trail.log("actor2", "tier2", "EVENT_2", {"seq": 2})
    trail.log("actor3", "tier3", "EVENT_3", {"seq": 3})
    assert trail.verify_integrity() is True
    assert len(trail.get_trail()) == 3


def test_batch_missing_file_raises():
    """Test that batch command raises FileNotFoundError for missing input."""
    with pytest.raises(FileNotFoundError):
        main(["batch", "-i", "/nonexistent/input.csv"])
