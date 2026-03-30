# Fun Builds

Free, open-source browser toys built as single-file apps.

No accounts, no backend, no tracking, and no install step. Each build is intended to be fast to understand, fast to try, and easy to share.

## Live Site

- Main gallery: `https://shipitandpray.github.io/fun-builds/`

## What This Repo Contains

- `index.html`
  - The main gallery page for all published builds.
- `manifest.json`
  - PWA metadata for the site shell.
- `<app-slug>/index.html`
  - Each app lives in its own folder and is designed to run standalone in the browser.
- `100_ideas.txt`, `200_ideas.txt`, and other idea files
  - Raw brainstorm inputs. These are not automatic build sources.
- `AUTORESEARCH_APPROVAL.md`
  - The approval gate for deciding which ideas are allowed to become apps.
- `idea_queue.json`
  - The tracked queue of `proposed`, `approved`, and `built` ideas.

## Live Links

### Recently Added

- Bad Idea VC: `https://shipitandpray.github.io/fun-builds/bad-idea-vc/`
- Apology Generator: `https://shipitandpray.github.io/fun-builds/apology-generator/`
- Excuse Printer: `https://shipitandpray.github.io/fun-builds/excuse-printer/`
- Petty Translator: `https://shipitandpray.github.io/fun-builds/petty-translator/`
- Ghosted Response Simulator: `https://shipitandpray.github.io/fun-builds/ghosted-response-simulator/`

### New Batch

- Overexplainer Bot: `https://shipitandpray.github.io/fun-builds/overexplainer-bot/`
- Blame Wheel: `https://shipitandpray.github.io/fun-builds/blame-wheel/`
- Vibe Last Seen: `https://shipitandpray.github.io/fun-builds/vibe-last-seen/`
- Excuse Escalator: `https://shipitandpray.github.io/fun-builds/excuse-escalator/`
- Out of Office Drama: `https://shipitandpray.github.io/fun-builds/out-of-office-drama/`
- Niche Hater: `https://shipitandpray.github.io/fun-builds/niche-hater/`
- Groupchat Peacemaker: `https://shipitandpray.github.io/fun-builds/groupchat-peacemaker/`
- Overthink Optimizer: `https://shipitandpray.github.io/fun-builds/overthink-optimizer/`
- Flex Decoder: `https://shipitandpray.github.io/fun-builds/flex-decoder/`
- Flake Forecast: `https://shipitandpray.github.io/fun-builds/flake-forecast/`
- Awkward Exit Script: `https://shipitandpray.github.io/fun-builds/awkward-exit-script/`
- Doomscroll Bingo: `https://shipitandpray.github.io/fun-builds/doomscroll-bingo/`
- Deadline Dice: `https://shipitandpray.github.io/fun-builds/deadline-dice/`
- Complaint Remix Studio: `https://shipitandpray.github.io/fun-builds/complaint-remix-studio/`
- Unhinged LinkedIn Post: `https://shipitandpray.github.io/fun-builds/unhinged-linkedin-post/`
- Text Tone Autopsy: `https://shipitandpray.github.io/fun-builds/text-tone-autopsy/`
- Crisis Rebrand: `https://shipitandpray.github.io/fun-builds/crisis-rebrand/`
- Meeting Hostage Negotiator: `https://shipitandpray.github.io/fun-builds/meeting-hostage-negotiator/`
- Answer Later Simulator: `https://shipitandpray.github.io/fun-builds/answer-later-simulator/`
- Moral Support Hotline: `https://shipitandpray.github.io/fun-builds/moral-support-hotline/`

## Build Principles

The repo favors ideas that are:

- understandable in under 15 seconds
- browser-only and single-file friendly
- visually or socially shareable
- small enough to ship quickly
- distinct from existing builds

This is intentionally not a heavy app framework repo. The goal is momentum, novelty, and low maintenance cost.

## Idea Workflow

Ideas should not go straight from brainstorm to implementation.

Use this flow:

`proposed -> approved -> built`

Definitions:

- `proposed`
  - The idea exists but has not cleared the approval gate.
- `approved`
  - The idea passed the binary autoresearch criteria and is allowed to be built.
- `built`
  - The app has been implemented and added to the gallery.
- `rejected`
  - The idea failed the gate and should not consume build time.
- `parked`
  - The idea may be useful later but should not be built now.

## Autoresearch Approval Gate

The build gate is documented in [AUTORESEARCH_APPROVAL.md](/Users/somepalli/claude/dangerous/fun-builds/AUTORESEARCH_APPROVAL.md).

An idea must pass at least `4/5` of these binary checks:

1. `Hook In 15 Seconds`
2. `Single-File Browser Feasibility`
3. `Distinct From Existing Builds`
4. `Shareable Output`
5. `Build Cost Fits The Repo`

If it fails two or more, it should not be built.

## Queue File

Tracked ideas live in [idea_queue.json](/Users/somepalli/claude/dangerous/fun-builds/idea_queue.json).

Each entry records:

- `slug`
- `title`
- `one_liner`
- `status`
- `evals`
- `approved_by`
- `notes`

This is the durable record that lets Claude or Codex pick up where the last approval pass left off.

## How To Add A New App

1. Add the idea to `idea_queue.json` as `proposed`.
2. Score it against the approval gate in `AUTORESEARCH_APPROVAL.md`.
3. Only move it to `approved` if it passes at least `4/5`.
4. Build it as `<slug>/index.html`.
5. Add a card to `index.html`.
6. Change its queue status to `built`.

## Deployment

This repo is published via GitHub Pages from:

- GitHub repo: `https://github.com/ShipItAndPray/fun-builds`
- Pages base URL: `https://shipitandpray.github.io/fun-builds/`

When `main` is pushed, GitHub Pages may take a short time to refresh.

## Current Note

There are unrelated local changes in this repo that are not part of the approved build flow. New work should continue to avoid touching unrelated dirty files unless explicitly requested.
