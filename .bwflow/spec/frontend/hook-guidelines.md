# Hook Guidelines

> How hooks (Claude Code hooks and script hooks) are used in this project.

---

## Overview

This project uses two types of hooks:
1. **Claude Code hooks** (Python): Runtime events injected by Claude
2. **Plugin hooks** (JavaScript): Session lifecycle managed by the plugin

---

## Claude Code Hook Architecture

### Hook Types

| Hook | Trigger | Script | Purpose |
|------|---------|--------|---------|
| `SessionStart` | startup / clear / compact | `session-start.py` | Inject full workflow context |
| `PreToolUse` | Before `Task` tool | `inject-subagent-context.py` | Inject agent-specific specs |
| `PreToolUse` | Before `Agent` tool | `inject-subagent-context.py` | Inject agent-specific specs |
| `SubagentStop` | When check agent stops | `ralph-loop.py` | Quality gate loop control |

### Hook Output Format

All Python hooks return structured JSON to the Claude runtime:

```python
import json

# SessionStart / PreToolUse output
result = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",  # or "PreToolUse"
        "additionalContext": "...",       # SessionStart only
        # PreToolUse only:
        "permissionDecision": "allow",
        "updatedInput": { "prompt": "..." }
    }
}
print(json.dumps(result, ensure_ascii=False))
```

### Hook: SessionStart

Injects structured workflow context at session start:

```python
# .claude/hooks/session-start.py
output.write("<session-context>...</session-context>\n")
output.write("<current-state>...\n</current-state>\n")
output.write("<workflow>...\n</workflow>\n")
output.write("<guidelines>...\n</guidelines>\n")
output.write("<instructions>...\n</instructions>\n")
output.write("<task-status>...\n</task-status>\n")
output.write("<ready>...</ready>")
```

Key injection points:
1. **session-context**: Introduction to bwflow workflow
2. **current-state**: Developer, git status, current task
3. **workflow**: Full `workflow.md` contents
4. **guidelines**: Spec index files
5. **instructions**: The start command content
6. **task-status**: Structured task readiness check

### Hook: PreToolUse (Task/Agent)

Intercepts `Task` and `Agent` tool calls to inject agent-specific context:

```python
# .claude/hooks/inject-subagent-context.py
tool_input = input_data.get("tool_input", {})
subagent_type = tool_input.get("subagent_type", "")

if subagent_type == "implement":
    context = get_implement_context(repo_root, task_dir)
    new_prompt = build_implement_prompt(original_prompt, context)
elif subagent_type == "check":
    context = get_check_context(repo_root, task_dir)
    new_prompt = build_check_prompt(original_prompt, context)
# ...

output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": {**tool_input, "prompt": new_prompt},
    }
}
```

Context is sourced from JSONL files in the task directory:
- `implement.jsonl` → Implement agent context
- `check.jsonl` → Check agent context
- `debug.jsonl` → Debug agent context

### Hook: SubagentStop

Controls the check agent loop (Ralph Wiggum pattern):

```python
# .claude/hooks/ralph-loop.py
# Blocks check agent from stopping until:
# 1. verify: commands pass, OR
# 2. Marker mode: all completion markers appear in output
# Safety: Max 5 iterations before forced stop
```

---

## Plugin Hook (SessionEnd)

The legacy plugin hook uses a different pattern:

```json
// hooks/hooks.json
{
  "description": "claude-shadow-context hooks",
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node \"${CLAUDE_PLUGIN_ROOT}/scripts/session-align.mjs\"",
            "timeout": 30,
            "statusMessage": "claude-shadow-context: 执行蓝图对齐收尾"
          }
        ]
      }
    ]
  }
}
```

The JavaScript handler uses stdin/stdout for JSON communication:

```javascript
// scripts/session-align.mjs
let rawInput = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => { rawInput += chunk; });
process.stdin.on('end', () => {
  try {
    const output = main(rawInput);
    if (output) process.stdout.write(output);
  } catch {
    // Fail closed — never disrupt Claude shutdown
  }
});
```

---

## Hook Design Principles

### 1. Context Injection, Not Modification

Hooks should inject context into agent prompts, not modify the agent's behavior. The agent remains autonomous.

### 2. Fail Closed for SessionEnd

The SessionEnd hook must never disrupt Claude shutdown. Always use try-catch with silent failure.

### 3. Return Structured JSON

All Claude Code hooks must return valid JSON to stdout. Any text printed to stdout corrupts the JSON response.

### 4. Cross-Platform Encoding

Python hooks must handle Windows stdio encoding. See `common/__init__.py` for the centralized fix.

---

## DO / DON'T

### DO

- Return valid JSON from all Claude Code hooks
- Use fail-closed pattern for SessionEnd hooks
- Inject context via `additionalContext` or `updatedInput`
- Centralize Windows encoding fix in `common/__init__.py`

### DON'T

- Don't print debug text to stdout in Claude Code hooks
- Don't modify agent behavior directly
- Don't use exit codes for Claude Code hook communication
- Don't throw unhandled errors in hook entry points
