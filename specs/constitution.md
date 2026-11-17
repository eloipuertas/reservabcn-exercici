# Constitution

Principles that every spec and every pull request in this repository follows. Humans own this file.

1. **Spec first.** No feature is implemented without an approved spec (`Status: active`). Requirement IDs are stable and never reused.
2. **One test per requirement.** Every requirement ID appears in at least one test. CI checks it.
3. **Small and reviewable.** One task per commit, one feature per pull request, diffs a person can read in ten minutes.
4. **Humans decide.** Agents propose. A person from the code-owner group approves every merge.
5. **Shared contracts have one owner.** Models, database session, auth, clock, entry point and test fixtures change only in their own pull request.
6. **Privacy by default.** A diner can never see or change another diner's data. Unknown and foreign ids look the same (404).
7. **Out of scope stays out.** Each spec lists what it does not cover. Agents do not add it.
