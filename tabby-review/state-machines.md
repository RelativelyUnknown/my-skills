# Finding implicit state machines

Most state-machine bugs live in code that never says it is one. A status string, a pair of booleans, a nullable timestamp or a call order that must be respected is a state machine whose states, transitions and rules are scattered over the code base. The bugs are the states nobody meant to allow and the transitions nobody wrote. Finding them is a reading task first and a probing task second ([bug-hunt.md](bug-hunt.md)).

## 1. Find them

Search for the usual shapes, then group the hits by the thing that has the state (an order, a job, a connection, a session, a document).

- Names: `status`, `state`, `phase`, `stage`, `step`, `mode`, `kind`, `lifecycle`, `attempt`, `retries`. `git grep -nEi "(status|state|phase|stage|step|mode)\s*(=|==|!=|in\b)"`
- String or enum comparisons in `if`/`elif` chains, a `match` on a state, `Literal["pending", "done"]`, an `Enum` with verbs or adjectives for members, a dict mapping a state to a handler.
- Booleans that travel together: `is_active` and `is_deleted`, `is_paid` and `is_shipped`. Two booleans are four states; usually one or two are not allowed.
- Nullable fields that mean a state: `published_at`, `deleted_at`, `completed_at`, `error`, `locked_by`, `lease_expires_at`. "Is it published?" is `published_at is not None`, and every reader repeats that rule.
- Database columns and migrations with a status; message types on a queue; webhook event types; retry and backoff counters; cache entries (cold, warm, stale, refreshing).
- Objects with a required call order: `open` then `read` then `close`, `connect` before `send`, `start` before `stop`, a builder, a client with `initialize()`, a task that is created, started, cancelled or done.
- Feature flags and settings that switch behaviour at runtime; a global that says "ready".

## 2. Write each one down

For every machine: the states (include the combinations the booleans allow, and "field missing"), the events that change it (a user action, a callback, a timeout, a retry, a restart), and the transitions (`git grep` every place that writes the field, including SQL `UPDATE`s and admin scripts). Put it in a table: state against event, the new state, and the code that does it.

```
state       event           next        where
pending     payment ok      paid        billing.py:88
pending     timeout         cancelled   jobs.py:41
paid        refund          refunded    billing.py:120
paid        payment ok      ???         (webhook delivered twice)
```

## 3. Look for these

- **Illegal states you can reach.** Two booleans that disagree, a `completed_at` with an `error`, a status with no row behind it. Can any path produce it, and what does the next reader do with it?
- **Missing transitions.** An event the table has no row for (the second `payment ok`, a refund of a cancelled order, a cancel while running). Today it does whatever the code happens to do.
- **Stuck states.** A state with no exit if an event never arrives (`pending` forever when the callback is lost, `running` after a crash). Is there a timeout, a lease or a sweeper?
- **No terminal state, or two writers.** Two code paths that both move the same thing, with no lock, compare-and-set (`UPDATE ... WHERE status = 'pending'`) or version column: the later write wins and the earlier one is lost.
- **Transitions that are not idempotent or not atomic.** The same event twice charges twice; a status change and its side effect (email, queue message, refund) are not in one transaction, so a crash between them leaves them disagreeing.
- **A rule repeated.** "Active" meaning three different conditions in three files; a state compared as a string that is spelled two ways.
- **Order dependence.** A method that only works after another was called, with no check, and the failure shows up far from the cause.

Run what you can: build the illegal state in a test and call the next function; send the event twice; stop the process between the status change and the side effect.

## 4. Report

The list of machines found (name, where the state lives, how many states), the table for any that has a finding, and each finding with file and line, the sequence of events that reaches it, and what happens. Draw one with the `tabby-diagrams` skill when the user wants a picture; a state diagram only helps when it shows the missing arrows.

Making a machine explicit (an `Enum`, one function that is the only writer, a transition table, a database `CHECK` or compare-and-set) is the fix when the table shows illegal states or two writers. Where the table shows none, leave the code alone and say so.
