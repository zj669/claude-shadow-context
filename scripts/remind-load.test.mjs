import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const scriptPath = path.join(__dirname, 'remind-load.mjs');

function runHook(input) {
  return spawnSync(process.execPath, [scriptPath], {
    input,
    encoding: 'utf8'
  });
}

test('空输入时静默退出', () => {
  const result = runHook('');
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '');
});

test('已包含 explore 命令时跳过提醒', () => {
  const result = runHook(JSON.stringify({ prompt: '请先执行 /claude-shadow-context:explore 再说' }));
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '');
});

test('已包含 blueprint 路径时跳过提醒，兼容反斜杠', () => {
  const result = runHook(JSON.stringify({ prompt: '请查看 .blueprint\\skills\\explore\\SKILL.md' }));
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '');
});

test('普通提示词时输出额外上下文', () => {
  const result = runHook(JSON.stringify({ prompt: '帮我熟悉这个项目' }));
  assert.equal(result.status, 0);
  const payload = JSON.parse(result.stdout);
  assert.equal(
    payload.additionalContext,
    'claude-shadow-context 提醒：需要熟悉代码上下文时，优先使用 /claude-shadow-context:explore 探索相关蓝图；若本轮涉及代码改动，结束前请补做 /claude-shadow-context:sync。'
  );
});
