import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateTask } from '../web/evaluator.mjs';

const base = {
  task_id: 'T1', target_identifier: 'K1', primary_metric: 10,
  secondary_metric: 4, status_descriptor: 'NOMINAL', is_critical_flag: false,
};
test('nominal task has no alerts', () => {
  const report = evaluateTask(base);
  assert.equal(report.overall_urgency, 'ROUTINE');
  assert.equal(report.total_alerts, 0);
  assert.equal('audit_hash' in report, false);
});
test('primary, secondary and keyword checks mirror Python worker thresholds', () => {
  const report = evaluateTask({
    ...base, primary_metric: 25.01, secondary_metric: 12.01,
    status_descriptor: 'DISCORDANT',
  });
  assert.equal(report.total_alerts, 3);
  assert.equal(report.overall_urgency, 'ELEVATED_RISK');
});
test('explicit critical flag dominates overall urgency', () => {
  const report = evaluateTask({ ...base, is_critical_flag: true });
  assert.equal(report.overall_urgency, 'CRITICAL_STAT_PANIC');
  assert.equal(report.critical_alerts_count, 1);
});
test('rejects nonfinite and incomplete metrics', () => {
  assert.throws(() => evaluateTask({ ...base, primary_metric: 'NaN' }));
  assert.throws(() => evaluateTask({ ...base, secondary_metric: '' }));
});
test('does not interpret the string false as a false boolean', () => {
  assert.throws(() => evaluateTask({ ...base, is_critical_flag: 'False' }));
});
