# Active Session State — [project or branch]

<!--
  HOW THIS FILE WORKS. Read this before editing it.

  This file has TWO regions and they are not interchangeable:

    1. The CHECKPOINT region below (STATUS + CHECKPOINT blocks) is the part
       machines read. The Codex SessionStart handler in `.codex/hooks/dispatch.py`
       returns the STATUS and CHECKPOINT payload when that event actually runs, so it is
       BOUNDED BY CONSTRUCTION: keep it under ~25 lines. It is OVERWRITTEN on
       every update, never appended to.

    2. Everything after `<!-- /CHECKPOINT -->` is free-form narrative for humans
       and for a returning agent that wants detail. The handler does not inject it, so
       it may grow — but see Rotation below.

  Why the split exists: one append-only file doing both jobs grows without
  bound, and every consumer then reads a different slice of it: the top, the
  bottom, or a block nothing writes. They disagree because there is no contract
  to agree on. With the named regions, every consumer reads the same part.

  ROTATION. When the narrative below grows past ~200 lines, move it to
  `production/session-logs/` and start it fresh:
      bash .agents/scripts/rotate-session-state.sh
  Nothing is lost — and the commit history already records most of what the
  narrative repeats.
-->

<!-- STATUS -->
Epic:
Feature:
Task:
<!-- /STATUS -->

<!-- CHECKPOINT -->
**Updated:** [YYYY-MM-DD]
**Branch:** `[branch]`
**Current task:** [one line — what is actively being worked on]
**Next step:** [one line — the very next action, concrete enough to resume cold]
**Blocked on:** [one line, or `nothing`]
**Files in progress:** [paths, comma-separated, or `none`]
**Run result:** [`$dev-story` writes its `Run result:` line here, verbatim, for `$story-done` to read; other writers leave this line out]
**Open questions:** [one line each, or `none`]
<!-- /CHECKPOINT -->

---

## Notes

[Free-form. Decisions and their rationale, what was tried and rejected, context
that would be expensive to reconstruct. Not machine-read — write for the person
or agent picking this up cold.]

<!--
  FIELD NOTES

  STATUS block
    Records the current focus (`Combat System > Melee > Hitboxes`) for workflows
    that read it explicitly. The retired client status-line entry is not used.
    All three fields are optional —
    leave a field blank when it does not apply, and blank all three when there is
    no active focus. Keep the markers for `.agents/scripts/session-state.sh`
    and workflows that explicitly read these fields.

  CHECKPOINT block
    The recovery payload. A trusted, actually invoked SessionStart handler reads
    the STATUS and CHECKPOINT regions and returns them as additional context
    when session tracking is on. Keep both bounded.
    Registration does not prove the client emitted or delivered an event.
    PreCompact only reminds the workflow to save; its real client trigger is not
    assessed. Do not assume a post-compaction SessionStart or automatic restore.
    On resume, use an actually received payload or explicitly read this region;
    report unavailable recovery and reconstruct state from current evidence.

    Keep `Branch` current. This file is not committed, so it stays put when you
    switch branches. The resuming agent must run `git branch --show-current`,
    compare it with `Branch`, and resolve any difference before using the saved
    task. `dispatch.py` does not compare branches or add an automatic warning.

    Write it so a cold reader can resume without reading anything else. "Current
    task: fixing the thing" is useless; "Current task: adding wall-jump to
    player_movement.gd" is not.
-->
