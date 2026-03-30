#!/usr/bin/env python3
"""
Autoresearch idea runner for Fun Builds.

This script evaluates candidate ideas against the repo's approval gate,
repeats the evaluation across multiple perturbation rounds to test stability,
and then ranks surviving ideas for build readiness.

It is intentionally conservative:
- it prefers rejecting blurry ideas over approving weak ones
- it writes durable artifacts for every run
- it can update idea_queue.json, but does not build apps itself
- it adds a second-stage build-readiness score for survivor ranking
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path("/Users/somepalli/claude/dangerous/fun-builds")
QUEUE_PATH = ROOT / "idea_queue.json"
APPROVAL_PATH = ROOT / "AUTORESEARCH_APPROVAL.md"
RUNS_DIR = ROOT / "autoresearch-runs"


TWO_HUNDRED_PATTERN = re.compile(
    r"^\s*\d+\.\s+\*\*(.*?)\*\*\s+\|\s+([a-z0-9-]+)\s+\|\s+(.*?)\s+\|\s+([a-z/]+)\s*$",
    re.M,
)

MARKDOWN_IDEA_PATTERN = re.compile(r"^\*\*(.*?)\*\*\s+[—-]\s+(.*)$", re.M)
PIPE_IDEA_PATTERN = re.compile(r"^(?:\*\*(.*?)\*\*|(.*?))\s+\|\s+([a-z0-9-]+)\s+\|\s+(.*?)\s+\|\s+([a-z0-9-]+)\s*$", re.M)


BLACKLIST_FEASIBILITY = {
    "api",
    "account",
    "accounts",
    "payment",
    "payments",
    "login",
    "scrape",
    "scraping",
    "server",
    "backend",
    "realtime social media activity",
    "twilio",
    "raspberry pi",
    "esp32",
    "oled",
    "thermal printer",
    "receipt printer",
    "speaker",
    "webcam",
    "camera module",
    "motion sensor",
    "microphone",
    "bluetooth",
    "servo",
    "led",
    "physical",
    "hardware",
}

BLACKLIST_BUILD_COST = {
    "custom dataset",
    "large dataset",
    "vision api",
    "camera",
    "microphone",
    "sensor",
    "motion",
    "audio processing",
    "real-time audio",
    "real time audio",
    "servo",
    "raspberry pi",
    "esp32",
    "bluetooth",
    "thermal printer",
    "printer",
    "external services",
}

SHAREABLE_HINTS = {
    "score",
    "meter",
    "report",
    "roast",
    "receipt",
    "generator",
    "judge",
    "forecast",
    "calculator",
    "diagnostic",
    "audit",
    "verdict",
    "artifact",
    "bingo",
    "dashboard",
}

BUILD_ARTIFACT_HINTS = {
    "receipt",
    "report",
    "score",
    "meter",
    "verdict",
    "forecast",
    "dashboard",
    "card",
    "judge",
    "calculator",
    "artifact",
}


@dataclass
class Idea:
    title: str
    slug: str
    one_liner: str
    source: str
    category: str = "text"


def normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\s-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def slugify(value: str) -> str:
    value = normalize_text(value)
    return value.replace(" ", "-")


def parse_two_hundred_file(path: Path) -> List[Idea]:
    text = path.read_text()
    ideas: List[Idea] = []
    for title, slug, desc, category in TWO_HUNDRED_PATTERN.findall(text):
        ideas.append(Idea(title=title.strip(), slug=slug.strip(), one_liner=desc.strip(), source=path.name, category=category.strip()))
    return ideas


def parse_markdown_ideas(path: Path) -> List[Idea]:
    text = path.read_text()
    ideas: List[Idea] = []
    seen = set()

    for bold_title, plain_title, slug, desc, category in PIPE_IDEA_PATTERN.findall(text):
        title = (bold_title or plain_title).strip()
        slug = slug.strip()
        if slug in seen:
            continue
        seen.add(slug)
        ideas.append(Idea(title=title, slug=slug, one_liner=desc.strip(), source=path.name, category=category.strip()))

    for title, desc in MARKDOWN_IDEA_PATTERN.findall(text):
        title = title.strip()
        if title.lower() in {"hardware:", "software:", "the magic moment:"}:
            continue
        slug = slugify(title)
        if slug in seen:
            continue
        seen.add(slug)
        ideas.append(Idea(title=title, slug=slug, one_liner=desc.strip(), source=path.name))
    return ideas


def load_built_apps(root: Path) -> Dict[str, str]:
    built = {}
    for child in root.iterdir():
        if child.is_dir() and (child / "index.html").exists():
            built[child.name] = child.name.replace("-", " ")
    return built


def load_known_titles(root: Path) -> Dict[str, str]:
    known: Dict[str, str] = {}
    for path in [root / "100_ideas.txt", root / "200_ideas.txt"]:
        if path.exists():
            for idea in parse_two_hundred_file(path):
                known[idea.slug] = idea.title
    return known


def perturb_text(text: str, rng: random.Random) -> str:
    text = text.strip()
    options = [
        text,
        text.lower(),
        text.upper(),
        text.replace("—", "-"),
        re.sub(r"\s+", " ", text),
        text + "!",
        text + ".",
        text.rstrip(".!?"),
    ]
    choice = rng.choice(options)
    if rng.random() < 0.3:
        choice = choice.replace(" and ", " & ")
    if rng.random() < 0.2:
        choice = re.sub(r"\bvery\b", "", choice, flags=re.I).strip()
    if rng.random() < 0.15:
        choice = choice[: max(20, len(choice) - 8)].strip()
    return re.sub(r"\s+", " ", choice).strip()


def title_similarity(title_a: str, title_b: str) -> float:
    return SequenceMatcher(None, normalize_text(title_a), normalize_text(title_b)).ratio()


def eval_hook(title: str, one_liner: str) -> bool:
    return len(title.split()) <= 6 and len(one_liner.split()) <= 20 and any(ch.isalpha() for ch in title)


def eval_single_file_browser(title: str, one_liner: str) -> bool:
    text = normalize_text(f"{title} {one_liner}")
    return not any(term in text for term in BLACKLIST_FEASIBILITY)


def eval_shareable_output(title: str, one_liner: str) -> bool:
    text = normalize_text(f"{title} {one_liner}")
    return any(term in text for term in SHAREABLE_HINTS) or len(one_liner.split()) <= 18


def eval_low_build_cost(title: str, one_liner: str) -> bool:
    text = normalize_text(f"{title} {one_liner}")
    return not any(term in text for term in BLACKLIST_BUILD_COST)


def eval_distinct(title: str, slug: str, built_titles: Dict[str, str], known_titles: Dict[str, str]) -> bool:
    if slug in built_titles:
        return False

    current = title
    for other_slug, other_title in {**built_titles, **known_titles}.items():
        if other_slug == slug:
            continue
        if title_similarity(current, other_title) >= 0.84:
            return False

    clusters = [
        ("meeting", {"meeting", "sync", "standup"}),
        ("dating", {"crush", "ghost", "flirt", "dating", "friendzone"}),
        ("apology", {"apology", "sorry"}),
        ("resume", {"resume", "linkedin"}),
        ("tone", {"tone", "subtext", "translator", "decoder"}),
    ]
    norm = normalize_text(f"{title} {slug}")
    for _, words in clusters:
        if sum(1 for word in words if word in norm) >= 2:
            # Dense cluster ideas are only allowed if the title is visibly distinct.
            if not any(word in normalize_text(title) for word in {"court", "bingo", "receipt", "forecast", "dashboard", "meter", "prenup"}):
                return False
    return True


def build_readiness_score(idea: Idea) -> Tuple[int, Dict[str, int]]:
    """
    Second-stage scorer after stability approval.

    Scores are intentionally simple and explainable. Higher is better.
    """
    norm_title = normalize_text(idea.title)
    norm_line = normalize_text(idea.one_liner)
    combined = f"{norm_title} {norm_line}"

    score_breakdown = {
        "instant_hook": 25 if len(idea.title.split()) <= 5 else 15 if len(idea.title.split()) <= 7 else 0,
        "artifact_strength": 20 if any(term in combined for term in BUILD_ARTIFACT_HINTS) else 8,
        "brevity": 20 if len(idea.one_liner.split()) <= 14 else 12 if len(idea.one_liner.split()) <= 20 else 0,
        "browser_fit": 20 if eval_single_file_browser(idea.title, idea.one_liner) else 0,
        "build_cost": 15 if eval_low_build_cost(idea.title, idea.one_liner) else 0,
    }
    return sum(score_breakdown.values()), score_breakdown


def evaluate_once(
    idea: Idea,
    title: str,
    one_liner: str,
    built_titles: Dict[str, str],
    known_titles: Dict[str, str],
) -> Dict[str, bool]:
    return {
        "hook_15s": eval_hook(title, one_liner),
        "single_file_browser": eval_single_file_browser(title, one_liner),
        "distinct_from_existing": eval_distinct(title, idea.slug, built_titles, known_titles),
        "shareable_output": eval_shareable_output(title, one_liner),
        "low_build_cost": eval_low_build_cost(title, one_liner),
    }


def stable_passes(iteration_results: List[Dict[str, bool]], minimum_passes: int) -> Tuple[bool, Dict[str, int]]:
    totals = {key: 0 for key in iteration_results[0]}
    for result in iteration_results:
        for key, value in result.items():
            if value:
                totals[key] += 1
    overall = all(total >= minimum_passes for total in totals.values())
    return overall, totals


def run_autoresearch(
    ideas: Iterable[Idea],
    iterations: int,
    min_pass_rate: float,
    seed: int,
    root: Path,
) -> Path:
    built_titles = load_built_apps(root)
    known_titles = load_known_titles(root)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS_DIR / f"idea-approval-{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "SKILL.md.baseline").write_text(APPROVAL_PATH.read_text())

    min_passes = int(iterations * min_pass_rate)
    rng = random.Random(seed)

    summary_rows = []
    shortlist_rows = []
    changelog_lines = ["# Changelog", ""]
    queue = json.loads(QUEUE_PATH.read_text())
    existing_items = {item["slug"]: item for item in queue["items"]}

    for index, idea in enumerate(ideas, start=1):
        iteration_results: List[Dict[str, bool]] = []
        for _ in range(iterations):
            perturbed_title = perturb_text(idea.title, rng)
            perturbed_one_liner = perturb_text(idea.one_liner, rng)
            iteration_results.append(
                evaluate_once(idea, perturbed_title, perturbed_one_liner, built_titles, known_titles)
            )

        approved, totals = stable_passes(iteration_results, min_passes)
        status = "approved" if approved else "rejected"
        score = sum(totals.values())
        max_score = len(totals) * iterations
        pass_rate = (score / max_score) * 100.0
        readiness, breakdown = build_readiness_score(idea)

        notes = []
        for key, total in totals.items():
            if total < min_passes:
                notes.append(f"{key} unstable at {total}/{iterations}")
        if not notes:
            notes.append("Stable across perturbation rounds.")

        summary_rows.append(
            {
                "slug": idea.slug,
                "title": idea.title,
                "score": score,
                "max_score": max_score,
                "pass_rate": f"{pass_rate:.1f}%",
                "status": status,
                "build_readiness": readiness,
                "notes": "; ".join(notes),
            }
        )
        if approved:
            shortlist_rows.append(
                {
                    "slug": idea.slug,
                    "title": idea.title,
                    "build_readiness": readiness,
                    "instant_hook": breakdown["instant_hook"],
                    "artifact_strength": breakdown["artifact_strength"],
                    "brevity": breakdown["brevity"],
                    "browser_fit": breakdown["browser_fit"],
                    "build_cost": breakdown["build_cost"],
                }
            )

        existing_items[idea.slug] = {
            "slug": idea.slug,
            "title": idea.title,
            "one_liner": idea.one_liner,
            "status": "approved" if approved else "rejected",
            "evals": {
                "hook_15s": totals["hook_15s"] >= min_passes,
                "single_file_browser": totals["single_file_browser"] >= min_passes,
                "distinct_from_existing": totals["distinct_from_existing"] >= min_passes,
                "shareable_output": totals["shareable_output"] >= min_passes,
                "low_build_cost": totals["low_build_cost"] >= min_passes,
            },
            "approved_by": "autoresearch-100x",
            "notes": "; ".join(notes),
        }

        changelog_lines.extend(
            [
                f"## Idea {index} - {idea.slug}",
                "",
                f"Status: {status}",
                f"Title: {idea.title}",
                f"Iterations: {iterations}",
                f"Threshold per eval: {min_passes}/{iterations}",
                f"Totals: {json.dumps(totals, sort_keys=True)}",
                f"Notes: {'; '.join(notes)}",
                f"Build readiness: {readiness}/100",
                f"Breakdown: {json.dumps(breakdown, sort_keys=True)}",
                "",
            ]
        )

    queue["items"] = sorted(existing_items.values(), key=lambda item: item["slug"])
    (run_dir / "idea_queue.preview.json").write_text(json.dumps(queue, indent=2) + "\n")

    with (run_dir / "results.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["slug", "title", "score", "max_score", "pass_rate", "status", "build_readiness", "notes"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    shortlist_rows.sort(key=lambda row: (-row["build_readiness"], row["slug"]))
    with (run_dir / "shortlist.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "slug",
                "title",
                "build_readiness",
                "instant_hook",
                "artifact_strength",
                "brevity",
                "browser_fit",
                "build_cost",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(shortlist_rows)

    (run_dir / "changelog.md").write_text("\n".join(changelog_lines))
    (run_dir / "run_config.json").write_text(
        json.dumps(
            {
                "iterations": iterations,
                "min_pass_rate": min_pass_rate,
                "seed": seed,
                "ideas": [idea.__dict__ for idea in ideas],
            },
            indent=2,
        )
        + "\n"
    )

    return run_dir


def load_ideas_from_file(path: Path) -> List[Idea]:
    if path.name in {"100_ideas.txt", "200_ideas.txt"}:
        return parse_two_hundred_file(path)
    return parse_markdown_ideas(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run 100-iteration autoresearch stability checks on fun-build ideas.")
    parser.add_argument("--source", required=True, help="Idea source file path.")
    parser.add_argument("--iterations", type=int, default=100, help="Iterations per idea.")
    parser.add_argument("--min-pass-rate", type=float, default=0.95, help="Per-eval pass threshold.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for perturbations.")
    parser.add_argument("--limit", type=int, default=0, help="Optional max number of ideas to evaluate.")
    args = parser.parse_args()

    source = Path(args.source)
    ideas = load_ideas_from_file(source)
    if args.limit > 0:
        ideas = ideas[: args.limit]

    run_dir = run_autoresearch(
        ideas=ideas,
        iterations=args.iterations,
        min_pass_rate=args.min_pass_rate,
        seed=args.seed,
        root=ROOT,
    )

    print(json.dumps({"run_dir": str(run_dir), "ideas_scanned": len(ideas)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
