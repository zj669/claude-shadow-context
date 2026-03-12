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

function main(rawInput) {
  safeParse(rawInput);
  
  const reminder = [
    'claude-shadow-context 提醒：会话即将结束。',
    '如果本轮涉及代码改动，建议使用 /claude-shadow-context:align 检查蓝图是否仍然对齐。'
  ].join(' ');
  
  return JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'SessionEnd',
      additionalContext: reminder
    }
  });
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
