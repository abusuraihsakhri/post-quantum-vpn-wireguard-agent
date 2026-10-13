import { evaluateTask } from './evaluator.mjs';

const form = document.getElementById('audit-form');
const output = document.getElementById('output');
const error = document.getElementById('error');
const exportButton = document.getElementById('export');
const resetButton = document.getElementById('reset');
const countElement = document.getElementById('count');
const alertElement = document.getElementById('alerts');
const stateElement = document.getElementById('status');
let processed = 0;
let totalAlerts = 0;
let latest = null;

form.addEventListener('submit', event => {
  event.preventDefault();
  error.textContent = '';
  const input = {
    task_id: document.getElementById('task-id').value,
    target_identifier: document.getElementById('target-id').value,
    primary_metric: document.getElementById('primary').value,
    secondary_metric: document.getElementById('secondary').value,
    status_descriptor: document.getElementById('descriptor').value,
    is_critical_flag: document.getElementById('critical').checked,
  };
  try {
    const result = evaluateTask(input, processed + 1);
    latest = result;
    processed += 1;
    totalAlerts += result.total_alerts;
    countElement.textContent = String(processed);
    alertElement.textContent = String(totalAlerts);
    stateElement.textContent = result.overall_urgency === 'ROUTINE' ? 'Nominal' :
      result.overall_urgency === 'CRITICAL_STAT_PANIC' ? 'Critical' : 'Elevated';
    stateElement.dataset.level = result.overall_urgency;
    output.textContent = JSON.stringify(result, null, 2);
    exportButton.disabled = false;
  } catch (err) {
    latest = null;
    exportButton.disabled = true;
    error.textContent = err.message || 'Unable to evaluate the input.';
    output.textContent = 'Input was not evaluated.';
  }
});

exportButton.addEventListener('click', () => {
  if (!latest) return;
  const file = new Blob([JSON.stringify(latest, null, 2) + '\n'], { type: 'application/json' });
  const url = URL.createObjectURL(file);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'local-rule-evaluation.json';
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 0);
});

resetButton.addEventListener('click', () => {
  form.reset();
  processed = 0;
  totalAlerts = 0;
  latest = null;
  countElement.textContent = '0';
  alertElement.textContent = '0';
  stateElement.textContent = 'Ready';
  delete stateElement.dataset.level;
  output.textContent = 'Submit an evaluation to see the local rule results.';
  error.textContent = '';
  exportButton.disabled = true;
});
