const readline = require('node:readline');
const test = require('node:test');
const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const scriptPath = path.join(__dirname, '..', 'bridge', 'mcp-server.cjs');

function runServer(inputLines) {
  return spawnSync(process.execPath, [scriptPath], {
    input: inputLines.join('\n') + '\n',
    encoding: 'utf8'
  });
}

test('initialize 返回 claude-shadow-context serverInfo 名称', () => {
  const result = runServer([
    JSON.stringify({ jsonrpc: '2.0', id: '1', method: 'initialize', params: {} })
  ]);

  assert.equal(result.status, 0);
  const lines = result.stdout.trim().split(/\r?\n/).filter(Boolean);
  assert.equal(lines.length, 1);
  const payload = JSON.parse(lines[0]);
  assert.equal(payload.result.serverInfo.name, 'claude-shadow-context');
  assert.equal(payload.result.serverInfo.version, '0.1.0');
});

test('notifications/initialized 不应产生响应', () => {
  const result = runServer([
    JSON.stringify({ jsonrpc: '2.0', id: '1', method: 'initialize', params: {} }),
    JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized', params: {} })
  ]);

  assert.equal(result.status, 0);
  const lines = result.stdout.trim().split(/\r?\n/).filter(Boolean);
  assert.equal(lines.length, 1);
  const payload = JSON.parse(lines[0]);
  assert.equal(payload.result.serverInfo.name, 'claude-shadow-context');
});

test('未知 request 仍返回 -32601', () => {
  const result = runServer([
    JSON.stringify({ jsonrpc: '2.0', id: '1', method: 'unknown/method', params: {} })
  ]);

  assert.equal(result.status, 0);
  const lines = result.stdout.trim().split(/\r?\n/).filter(Boolean);
  assert.equal(lines.length, 1);
  const payload = JSON.parse(lines[0]);
  assert.equal(payload.id, '1');
  assert.equal(payload.error.code, -32601);
  assert.equal(payload.error.message, 'Method not found');
});
