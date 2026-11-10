# Refactoring

Change the structure, not the behaviour. Behaviour here means public interfaces, failure behaviour, ordering, output bytes and compatibility.

1. **Understand before touching.** Before removing or reshaping something, find out why it is there: callers, tests, `git log -S` or `git blame` on the lines. If you cannot say why a check or branch exists, keep it and flag it; do not "fix" a quirk you do not understand.
2. **Pin the behaviour first.** No tests around the code? Write characterization tests from the current behaviour (a few realistic and edge inputs, including the odd ones), run them green, and only then change structure. Without any way to run code, say so and refactor only what you can verify by reading.
3. **Pick the highest safety rung you can reach.** Existing tests green; else characterization tests; else a before-and-after comparison on recorded input; else a read-only plan. Say which rung you stood on.
4. **One ownership boundary at a time.** Extract, move or merge one thing per step, keep the project buildable and the tests green after each step, and keep feature changes out of the refactor.
5. **Moved code keeps its checks.** Code you move, merge or inline keeps its validation and error handling; a check that vanished in the move is a behaviour change.
6. **Fix every smell the request is about**, not just the cheap ones, and nothing outside it ([code/smells.md](../code/smells.md)). Mention what you noticed and left alone.
7. **Prove it.** Run the same checks after as before. Report the rung, what moved, what you kept on purpose, and anything you could not verify.

Not a refactor: a signature change, a new error type, a different output. That is a feature or a break: handle it as one ([api-design.md](../library/shared/api-design.md)).
