# $smoke-check — Phase 4: Run Manual Smoke Checks

> Part of `$smoke-check`. `SKILL.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.

## Phase 4: Run Manual Smoke Checks

**In this file:**

- Checklist source: name it in the report
- Batch 1 — Core stability
- Batch 2 — Sprint changes and regression
- Batch 3 — Data integrity and performance
- Platform batches: PC, console, mobile

Draw the smoke test checklist from, in priority order (and name the one you used in the report):
1. The QA plan's "Smoke Test Scope" section (if QA plan was found in Phase 1)
2. `production/qa/smoke-tests.md` (if it exists)
3. `tests/smoke/` directory contents (if it exists)
4. The standard fallback list below (used only when none of the above exist)

**Name the source you used in the report**, on its own line — *"Checklist source:
`production/qa/smoke-tests.md`"*, or *"Checklist source: standard fallback list —
no QA plan scope, no `production/qa/smoke-tests.md`, no `tests/smoke/`."* The
fallback is a real fallback, so nothing is silently skipped here, but without
that line a report drawn from the generic list reads the same as one drawn from
this project's own smoke definitions. `$gate-check` validates a smoke report's
claims against the repo, and it cannot weigh them without knowing what the
checklist was drawn from.

Tailor batches 2 and 3 to the actual systems identified from the sprint or QA
plan. Replace bracketed placeholders with real mechanic names from the current
sprint's stories.

Use the current question tool only when it is available in this mode, following
its actual schema. Ask one single-select question per check and batch only as many
questions as that tool permits (the synchronous example below allows up to three). There is no total-call limit that could leave required checks unasked.
Without a question tool, list the same check IDs and options in plain text and wait
for an explicit response such as `core_launch=PASS, core_new_game=FAIL,
core_menu=NOT TESTED`. Return all required IDs; a missing ID remains UNANSWERED.

For each check, use these three result options. Replace the example ID/title
and question with the actual check, using the matching adapter below:

Synchronous `request_user_input` example (only where its mode allows it):

```json
{
  "questions": [
    {
      "id": "core_launch",
      "header": "Launch",
      "question": "Did the current build launch without a crash this session?",
      "options": [
        {"label": "PASS", "description": "I tested this check on the current build and it passed."},
        {"label": "FAIL", "description": "I tested this check and observed a failure; I will describe it."},
        {"label": "NOT TESTED", "description": "I did not test this check or could not run it."}
      ]
    }
  ]
}
```

**Choose the adapter from the actual exposed tool and mode.** The synchronous
`request_user_input` example uses `id/header/question` and object options; some
hosts allow it only in Plan mode. Do not call it in Default mode when unavailable.
If the current client exposes `request_user_input_async`, use its declared
`questions[{title, options:[strings]}]` schema instead, as shown below. Do not pass
the synchronous fields to the asynchronous tool. If either tool's current schema
differs, adapt to that schema; these examples are not a universal tool interface.
With neither tool available, ask the same choices in plain text and wait.

**Asynchronous lifecycle:** a successful submission is a delivery receipt, not
the user's answer. Match the later user response to its question title/check ID.
Keep required questions pending until that response arrives. Elapsed time, an
immediate tool return, a dismissal or an empty answer supplies no approval or test
result. Continue only independent work while waiting; do not write an output,
issue a pass or claim completion that depends on an unanswered required question.

| Event | Required state and action |
| --- | --- |
| `ASYNC SUBMITTED` | WAITING; retain the pending question, apply no answer-dependent action. |
| `USER ANSWER RECEIVED` | Apply only the explicit answer to its matching question; preserve unanswered siblings. |
| `NO USER ANSWER` | UNANSWERED; wait, or report the unresolved requirement if the user ends the run. |

Asynchronous `request_user_input_async` example:

```json
{
  "questions": [
    {
      "title": "core_launch: Did the current build launch without a crash this session?",
      "options": [
        "PASS",
        "FAIL",
        "NOT TESTED"
      ]
    }
  ]
}
```

**Response mapping (per required check):**

| Response | Report contribution |
| --- | --- |
| `PASS` | PASS only for the explicitly tested check on the current build. |
| `FAIL` | FAIL; retain the failure description before generating the report. |
| `NOT TESTED` | NOT ASSESSED; record why the check could not run. |
| `UNANSWERED` | NOT ASSESSED; no answer, dismissal, blank or missing check ID never means PASS. |

An explicit free-text N/A needs a reason grounded in the current scope (for example,
save/load is not implemented). Record it verbatim as N/A; it cannot stand for an
unanswered check. Any known FAIL outranks NOT ASSESSED, which outranks a pass.

**Batch 1 — Core stability (always run):**
- `core_launch`: launch the current build without crashing before the main menu.
- `core_new_game`: start a new game / session.
- `core_menu`: main menu responds to inputs.
- `core_navigation`: basic navigation has no crash or hang.

Ask `core_launch` first. If the user has not launched the current build, mark all
unexecuted checks `NOT TESTED — build not launched this session`, explicitly skip
Batches 2 and 3 and platform checks because they need a running build, and return
NOT ASSESSED unless an actual failure was observed. A missing launch answer remains
UNANSWERED: wait for it, or record NOT ASSESSED if the user ends the run.

**Batch 2 — Sprint changes and regression (always run):**
- `sprint_primary`: [primary mechanic this sprint].
- `sprint_secondary`: [second notable change, only when one exists].
- `sprint_regression`: regression check for previous sprint features.
- `sprint_other`: other unexpected breakage observed during the scoped checks.

**Batch 3 — Data integrity and performance (unless `quick` argument):**
- `data_save_load`: save/load preserves data, with explicit N/A if not implemented.
- `performance`: frame rate and hitches on the target device.

**Platform batches** (only when `--platform` was provided):
- **PC** (`pc` or `all`): keyboard controls, mouse/cursor, windowed/fullscreen,
  resolution change — one check ID and result for each.
- **Console** (`console` or `all`): gamepad input, TV safe zone/text clipping,
  correct input prompts, cold start without a prior save — one result for each.
- **Mobile** (`mobile` or `all`): touch controls, orientation change,
  background/foreground transition, performance/thermal throttling — one result for each.

For every FAIL, ask for a brief description. Record each response verbatim for
Phase 5, including NOT TESTED and UNANSWERED. If questions cannot be answered,
report those checks as NOT ASSESSED; never infer a pass from silence.

---
