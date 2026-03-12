import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const scriptPath = path.join(__dirname, 'session-align.mjs');

function runHook(input) {
  return spawnSync(process.execPath, [scriptPath], {
    input,
    encoding: 'utf8'
  });
}

test('SessionEnd 脚本在空输入时静默退出', () => {
  const result = runHook('');
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '');
});

test('SessionEnd 脚本在合法 JSON 输入时保持静默', () => {
  const result = runHook(JSON.stringify({ source: 'SessionEnd', session_id: 'abc' }));
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '');
});
