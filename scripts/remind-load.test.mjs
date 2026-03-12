import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const scriptPath = path.join(__dirname, 'remind-load.mjs');

function runHook(args, input) {
  return spawnSync(process.execPath, [scriptPath, ...args], {
    input,
    encoding: 'utf8'
  });
}

test('用户提示词空输入时静默退出', () => {
  const result = runHook(['user-prompt'], '');
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '');
});

test('用户提示词已包含 explore 命令时跳过提醒', () => {
  const result = runHook(['user-prompt'], JSON.stringify({ prompt: '请先执行 /claude-shadow-context:explore 再说' }));
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '');
});

test('用户提示词已包含 blueprint 路径时跳过提醒，兼容反斜杠', () => {
  const result = runHook(['user-prompt'], JSON.stringify({ prompt: '请查看 .blueprint\\skills\\explore\\SKILL.md' }));
  assert.equal(result.status, 0);
  assert.equal(result.stdout, '');
});

test('普通用户提示词时输出 explore 与 align 提醒', () => {
  const result = runHook(['user-prompt'], JSON.stringify({ prompt: '帮我熟悉这个项目' }));
  assert.equal(result.status, 0);
  const payload = JSON.parse(result.stdout);
  assert.equal(payload.hookSpecificOutput.hookEventName, 'UserPromptSubmit');
  assert.match(payload.hookSpecificOutput.additionalContext, /\/claude-shadow-context:explore/);
  assert.match(payload.hookSpecificOutput.additionalContext, /\/claude-shadow-context:align/);
});

test('子 agent 启动时输出蓝图优先上下文', () => {
  const result = runHook(['subagent-start'], JSON.stringify({ session_id: 'test' }));
  assert.equal(result.status, 0);
  const payload = JSON.parse(result.stdout);
  assert.equal(payload.hookSpecificOutput.hookEventName, 'SubagentStart');
  assert.match(payload.hookSpecificOutput.additionalContext, /子 agent/);
  assert.match(payload.hookSpecificOutput.additionalContext, /\/claude-shadow-context:align/);
});
