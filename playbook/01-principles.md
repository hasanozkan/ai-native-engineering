# 1. Principles

AI coding agents are fast, tireless and confidently wrong in ways a human
teammate rarely is. The answer is not to supervise every keystroke; it is to
put agents inside the same structure that keeps humans honest — and to make
that structure mechanical.

1. **The spec leads.** An agent implements numbered rules someone wrote down,
   not a paraphrase of a chat. If the rule is not written, the first task is
   writing it.
2. **Every rule has one owner.** A convention lives in exactly one file;
   everything else points at it. Copies drift, and an agent will faithfully
   follow whichever copy it read.
3. **Gates, not guidelines.** Anything that matters is checked by the build.
   A reviewer — human or agent — then reads intent instead of policing style.
4. **A gate is trusted only after it has failed.** Break it on purpose once
   and watch it turn red. A green check that has never been red proves nothing.
5. **Measure, don't assume.** Before stating a fact about the system, look.
   "The API doesn't support that" is a claim; the discovery document is
   evidence.
6. **Report outcomes as they are.** Red tests are reported red, skipped steps
   are reported skipped. An agent that rounds "mostly works" up to "done"
   costs more than one that stops.
7. **Humans hold the irreversible buttons.** Merging code, deploying,
   deleting, spending money and speaking for the team stay behind explicit
   approval (see [approval boundaries](05-approval-boundaries.md)).
8. **Lessons are written down where the next session will read them.**
   An agent's memory is a versioned repository, not a chat history.
