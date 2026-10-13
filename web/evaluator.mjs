/**
 * Deterministic local demonstration of the repository's three rule workers.
 * It performs no WireGuard, Noise, ML-KEM, or other cryptographic operations.
 */
export function evaluateTask(data, sequence = 1) {
  const taskId = String(data.task_id ?? '').trim();
  const target = String(data.target_identifier ?? '').trim();
  const descriptor = String(data.status_descriptor ?? '').trim();
  const primary = Number(data.primary_metric);
  const secondary = Number(data.secondary_metric);

  if (!taskId || !target) throw new Error('Task and target identifiers are required.');
  if (taskId.length > 256 || target.length > 256 || descriptor.length > 256) {
    throw new Error('Identifiers and descriptor must be at most 256 characters.');
  }
  if (data.primary_metric === '' || data.secondary_metric === '' ||
      !Number.isFinite(primary) || !Number.isFinite(secondary)) {
    throw new Error('Metrics must be finite numbers.');
  }
  if (typeof data.is_critical_flag !== 'boolean') {
    throw new Error('Critical flag must be a boolean.');
  }

  const alerts = [];
  function add(origin, urgency, summary, details, remediation) {
    alerts.push({
      alert_id: 'LOCAL-' + String(sequence).padStart(4, '0') + '-' + (alerts.length + 1),
      origin_worker: origin,
      urgency,
      summary,
      technical_details: details,
      actionable_remediation: remediation,
    });
  }
  if (primary > 25) {
    add('InvariantQCWorker', 'ELEVATED_RISK', 'Primary Metric Threshold Exceeded',
        'Primary measurement ' + primary.toFixed(2) + ' exceeds demonstration limit 25.00.',
        'Review the primary measurement and its configured threshold.');
  }
  if (data.is_critical_flag || secondary > 12) {
    add('SafetyEscalationWorker', data.is_critical_flag ? 'CRITICAL_STAT_PANIC' : 'ELEVATED_RISK',
        'Safety Interlock Triggered',
        'CriticalFlag=' + data.is_critical_flag + '; secondary metric=' + secondary.toFixed(2) + '.',
        'Review the critical flag and secondary metric.');
  }
  if (['DISCORDANT', 'ANOMALY', 'MUTANT', 'VIOLATION', 'FAIL', 'REJECT']
      .some(term => descriptor.toUpperCase().includes(term))) {
    add('ProtocolConformanceWorker', 'ELEVATED_RISK',
        'Status Descriptor Flag Detected',
        'Descriptor matches a demonstration anomaly keyword.',
        'Inspect the descriptor and confirm whether the flag is meaningful.');
  }

  const criticalCount = alerts.filter(a => a.urgency === 'CRITICAL_STAT_PANIC').length;
  const overall = criticalCount ? 'CRITICAL_STAT_PANIC' :
    alerts.length ? 'ELEVATED_RISK' : 'ROUTINE';
  const integrity = criticalCount ? 'RECALIBRATION_REQUIRED' :
    alerts.length ? 'DISCORDANT_ANOMALY' : 'VALIDATED_OPTIMAL';
  return {
    mode: 'LOCAL_RULE_DEMONSTRATION',
    dossier_id: 'LOCAL-' + String(sequence).padStart(4, '0'),
    task_id: taskId,
    target_identifier: target,
    overall_urgency: overall,
    integrity_status: integrity,
    total_alerts: alerts.length,
    critical_alerts_count: criticalCount,
    alerts,
    consensus_summary: 'Local evaluation of three deterministic threshold/keyword rules.',
    security_note: 'No cryptographic key exchange, WireGuard tunnel, ratchet rotation, or audit signature is performed.',
  };
}
