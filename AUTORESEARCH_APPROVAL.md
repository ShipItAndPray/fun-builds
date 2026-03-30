# Autoresearch Approval Gate

This repo should not bulk-build raw ideas anymore.

Every new app idea must pass an explicit approval step before implementation.

## Status Flow

Use this lifecycle for every idea:

`proposed -> approved -> built`

Optional failure states:

`rejected`

`parked`

## Approval Rule

An idea is only `approved` if it passes at least `4/5` binary evals below.

If it fails `2` or more evals, do not build it.

The binary gate is only a prefilter.

Final approval must come from an LLM review pass that tries to reject weak ideas on semantic grounds:

- Is the premise still strong when read by a model without the repo context?
- Does it feel genuinely distinct, not just mechanically different?
- Would the finished app feel worth clicking in the gallery?
- Does the output artifact feel screenshotable, funny, or useful enough to share?

If the LLM review disagrees with the binary gate, the LLM review wins.

## Binary Evals

EVAL 1: Hook In 15 Seconds
Question: Can a new user understand the joke or utility almost immediately?
Pass: The app concept is obvious from the title plus one sentence.
Fail: The premise needs explanation or setup.

EVAL 2: Single-File Browser Feasibility
Question: Can this be shipped as a standalone client-side HTML app with no backend?
Pass: The core loop works with local JS, text input, timers, camera, audio, or simple browser APIs.
Fail: The concept depends on server state, accounts, payments, scraping, or external services.

EVAL 3: Distinct From Existing Builds
Question: Is it meaningfully different from what already exists in this repo?
Pass: The mechanic or emotional hook is clearly different.
Fail: It is just a renamed variant of an existing app.

EVAL 4: Shareable Output
Question: Does it produce a result that is easy to screenshot, read aloud, or repost?
Pass: The output has a clear punchline, score, or artifact.
Fail: The output is too generic or not visibly interesting.

EVAL 5: Build Cost Fits The Repo
Question: Can it be built fast without introducing heavy maintenance cost?
Pass: The app is small, self-contained, and easy to reason about.
Fail: The concept requires complex assets, large datasets, or lots of custom logic.

## Approval Record Format

Each idea should be recorded in `idea_queue.json` with:

- `slug`
- `title`
- `one_liner`
- `status`
- `evals`
- `approved_by`
- `notes`

Example:

```json
{
  "slug": "bad-idea-vc",
  "title": "Bad Idea VC",
  "one_liner": "Pitch a terrible startup and get a serious investor memo.",
  "status": "approved",
  "evals": {
    "hook_15s": true,
    "single_file_browser": true,
    "distinct_from_existing": true,
    "shareable_output": true,
    "low_build_cost": true
  },
  "approved_by": "autoresearch",
  "notes": "Strong hook, easy output artifact, low implementation cost."
}
```

## Build Policy

- Do not build directly from brainstorm files.
- First move ideas into `idea_queue.json` as `proposed`.
- Only build entries marked `approved`.
- When an app is shipped, change `status` to `built`.

## Review Policy

When running an autoresearch pass over ideas:

1. Score each idea against the 5 binary evals.
2. Keep only ideas that pass at least 4 as the candidate pool.
3. Run an LLM red-team pass over the survivor pool before building anything.
4. Prefer ideas with:
   - instant premise
   - clear visual artifact
   - low code surface area
   - no backend dependency
5. Reject duplicate or blurry concepts even if they are funny.

## Practical Rule

If an idea cannot survive a hard yes/no approval pass, it should not consume build time.
