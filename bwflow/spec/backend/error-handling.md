# Error Handling

> **To be filled by the team**: Document your project's error handling patterns and conventions.

---

## Overview

**To be filled by the team**: Describe your project's overall error handling philosophy.

Questions to answer:
- What is the general error handling strategy? (fail-fast, graceful degradation, etc.)
- How are errors logged and monitored?
- What error types are used in the codebase?

---

## Error Handling Patterns

**To be filled by the team**: Document common error handling patterns used in your project.

Questions to answer:
- How should errors be caught and handled at different layers?
- When should errors be re-thrown vs. handled locally?
- How should validation errors be handled?
- How should external API errors be handled?

---

## Error Messages

**To be filled by the team**: Document conventions for error messages.

Questions to answer:
- What information should error messages include?
- How should error messages be formatted?
- Should error messages be user-facing or developer-facing?

---

## Examples

**To be filled by the team**: Provide examples of good error handling from your project.

```python
# Example: To be filled by the team
    if result.returncode == 0:
        print("[OK] Auto-committed", file=sys.stderr)
    else:
        print(f"[WARN] Auto-commit failed", file=sys.stderr)
except Exception as e:
    print(f"[WARN] Hook error: {e}", file=sys.stderr)
```

### Return-Based Error Signaling

```python
def check_package_json(cwd: str) -> dict[str, bool]:
    if not fs.existsSync(packageJsonPath):
        return {"hasFrontend": False, "hasBackend": False}
    try:
        content = fs.readFileSync(packageJsonPath, "utf-8")
        pkg = JSON.parse(content)
        return {"hasFrontend": bool(pkg.dependencies), "hasBackend": bool(pkg.scripts)}
    except:
        return {"hasFrontend": False, "hasBackend": False}
```

### Type Guard for Errors

```python
# Correct: Type guard for error.message
except Exception as e:
    message = e.message if isinstance(e, Exception) else str(e)
    print(f"Error: {message}", file=sys.stderr)
```

---

## JavaScript: Hook Error Handling

### SessionEnd Hook: Fail Closed (Silent)

The SessionEnd hook must **never** disrupt Claude shutdown. Use try-catch with silent failure:

```javascript
// session-align.mjs
process.stdin.on('end', () => {
  try {
    const output = main(rawInput);
    if (output) {
      process.stdout.write(output);
    }
  } catch {
    // SessionEnd hook should fail closed to avoid disrupting Claude shutdown.
  }
});
```

### PreToolUse Hook: Allow/Deny Pattern

PreToolUse hooks return structured output for Claude's permission system:

```javascript
const output = {
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "allow",
    updatedInput: { ...tool_input, prompt: new_prompt },
  }
};
print(json.dumps(output, ensure_ascii=False));
process.exit(0);
```

### SessionStart Hook: Context Injection

SessionStart hooks return structured context via `additionalContext`:

```javascript
const result = {
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: output.getvalue(),
  }
};
print(json.dumps(result, ensure_ascii=False));
```

---

## Exit Codes

### Python Scripts

| Code | Meaning | Usage |
|------|---------|-------|
| `0` | Success | Normal completion |
| `1` | Error | Any error condition |
| `2` | Usage error | Wrong arguments |

### Claude Hooks

Hooks do not use exit codes directly — they return structured JSON to the Claude runtime. Non-zero exits may terminate the hook process without affecting Claude's main loop.

---

## DO / DON'T

### DO (Python)

- Catch errors at the top level (command handlers)
- Use `isinstance(e, Exception)` for type guards
- Exit with code 1 on errors for scripting
- Use empty catch for truly optional operations
- Show user-friendly messages, not stack traces
- Print errors to stderr with context

### DON'T (Python)

- Don't catch errors in utility functions unless you can handle them
- Don't assume `error` is an `Error` type
- Don't log full stack traces to users
- Don't use exit code 0 for error conditions

### DO (JavaScript Hooks)

- Fail closed for SessionEnd hooks (swallow errors silently)
- Return structured output with `hookSpecificOutput` key
- Use `permissionDecision: "allow"` for PreToolUse when continuing
- Use `process.exit(0)` after successful hook output

### DON'T (JavaScript Hooks)

- Don't throw unhandled errors in hook entry points
- Don't write to stderr in SessionEnd hooks (may disrupt shutdown)
- Don't return non-JSON output from hooks

---

## Common Mistakes

### Mistake 1: Not using type guard in Python

```python
# Bad
except Exception as error:
    print(error.message)  # error is unknown type

# Good
except Exception as e:
    message = e.message if isinstance(e, Exception) else str(e)
```

### Mistake 2: Silent failure without comment (Python)

```python
# Bad: Why is this ignored?
try:
    doSomething();
except:
    pass

# Good: Explain why it's safe to ignore
try:
    doSomething();
except:
    # Optional operation - safe to ignore if it fails
    pass
```

### Mistake 3: Throwing in SessionEnd hook

```javascript
// Bad: Will disrupt Claude shutdown
process.stdin.on('end', () => {
  main(rawInput);  // No try-catch!
});

// Good: Fail closed
process.stdin.on('end', () => {
  try {
    main(rawInput);
  } catch {
    // Silently fail
  }
});
```
