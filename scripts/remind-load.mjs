const mode = process.argv[2] || 'user-prompt';

const userPromptReminder = [
  'claude-shadow-context 提醒：需要熟悉代码上下文时，优先使用 /claude-shadow-context:explore。',
  '先通过蓝图理解职责、边界和关键方法，再补看少量代码。',
  '若本轮涉及代码改动，结束前请使用 /claude-shadow-context:align 检查蓝图是否仍然对齐。'
].join(' ');

const subagentReminder = [
  'claude-shadow-context 提醒：你是子 agent，优先通过 /claude-shadow-context:explore 的方法收敛上下文。',
  '先读根入口与最相关蓝图，再补看必要代码，不要先全仓散搜。',
  '如果涉及代码变更，请保留足够上下文，供主流程在结束时执行 /claude-shadow-context:align。'
].join(' ');

function safeParse(rawInput) {
  if (!rawInput || !rawInput.trim()) {
    return null;
  }

  try {
    return JSON.parse(rawInput);
  } catch {
    return null;
  }
}

function shouldSkipPrompt(prompt) {
  return /(^|\s)(\/claude-shadow-context:explore|explore\b)/.test(prompt) || /\.blueprint[\\/]/.test(prompt);
}

function wrapAdditionalContext(hookEventName, additionalContext) {
  return JSON.stringify({
    hookSpecificOutput: {
      hookEventName,
      additionalContext
    }
  });
}

function main(rawInput, currentMode = mode) {
  if (currentMode === 'subagent-start') {
    return wrapAdditionalContext('SubagentStart', subagentReminder);
  }

  const payload = safeParse(rawInput);
  const prompt = typeof payload?.prompt === 'string' ? payload.prompt : '';
  if (!prompt || shouldSkipPrompt(prompt)) {
    return '';
  }

  return wrapAdditionalContext('UserPromptSubmit', userPromptReminder);
}

let rawInput = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  rawInput += chunk;
});
process.stdin.on('end', () => {
  const output = main(rawInput);
  if (output) {
    process.stdout.write(output);
  }
});

export { main };
