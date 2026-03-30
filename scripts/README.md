# Scripts

## `autoresearch_idea_runner.py`

Runs repeatable idea approval checks for Fun Builds.

What it does:

- loads ideas from a source file
- runs the approval gate across repeated perturbation rounds
- writes durable artifacts into `autoresearch-runs/`
- produces `results.tsv`, `changelog.md`, `run_config.json`, and a preview queue file

Default behavior:

- `100` iterations per idea
- `95%` per-eval pass threshold
- conservative rejection if an idea is unstable across perturbations

Example:

```bash
python3 scripts/autoresearch_idea_runner.py \
  --source /Users/somepalli/claude/dangerous/fun-builds/100_ideas.txt \
  --iterations 100 \
  --min-pass-rate 0.95
```

Important:

- this script approves or rejects ideas
- it does **not** build apps automatically
- app generation should only happen for ideas that remain stable under the runner
