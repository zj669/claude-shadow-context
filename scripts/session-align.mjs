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
  return '';
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
