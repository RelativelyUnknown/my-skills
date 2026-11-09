# Runbook

A procedure for someone woken at night who did not write the system. Every step is an action they can do without thinking.

```markdown
# Runbook: <situation>

## When to use this
The alert or symptom, by its exact name.

## Before you start
Access, tools and where to run commands.

## Steps
1. <action>
   ```bash
   <exact command>
   ```
   Expected: <what a good result looks like>.
2. <action> ... Expected: ...

## Check it worked
The command and the result that means "fixed".

## If it did not work
The next thing to try, the time limit, and who to escalate to (name, channel) with what to tell them.
```

- One action per step, with the exact command in a code block; no "check the logs" without the command.
- Every check says what a good result looks like ("Expected: 0"), so the reader can tell success from failure.
- Give a time limit for escalation, and the person or channel.
- Last line: the owner and the date the steps were last run.
