const reminder = 'Bluefirst 插件提醒：需要熟悉代码上下文时，优先使用 /bluefirst-plugin:explore 探索相关蓝图；若本轮涉及代码改动，结束前请补做 /bluefirst-plugin:sync。';

function shouldSkip(prompt) {
  return /(^|\s)(\/bluefirst-plugin:explore|explore\b)/.test(prompt) || /\.blueprint[\\/]/.test(prompt);
}

function main(rawInput) {
  if (!rawInput || !rawInput.trim()) {
    return '';
  }

  let payload;
  try {
    payload = JSON.parse(rawInput);
  } catch {
    return '';
  }

  const prompt = typeof payload?.prompt === 'string' ? payload.prompt : '';
  if (!prompt || shouldSkip(prompt)) {
    return '';
  }

  return JSON.stringify({
    additionalContext: reminder
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
