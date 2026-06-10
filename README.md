# Stock Selloff Triage

Is your stock weak on its own? Is your sector shifting? Or is the whole market repricing?

This repo documents, end to end, how I built a capital-rotation diagnostic in one evening with Claude Code during the June 2026 tech selloff, using Broadcom (AVGO) as the live case. It accompanies this edition of Alpha with AI: [https://ai.shikshannivesh.com/p/how-claude-mythos-replaced-my-600]

## What is in here

- **process/** — the five instructions I typed, in order, with the full output of each. This is the part that matters. The method transfers to problems this repo has never heard of.
- **outputs/** — the computed stats, the formal classification with every figure, and the returns table. Every number traces to fetched price files.
- **data/** — the sourced news and flows timeline, and the provenance README documenting exactly where every number came from, including the one data patch.
- **skill/** — the reusable skill that was left over after the problem was solved. Not the other way around.

## Install the skill

Copy the `skill/stock-selloff-triage/` folder into `~/.claude/skills/`, or use the packaged `stock-selloff-triage.skill` file. Then, in Claude Code:

    Is my stock weak or is its sector breaking?

That one line is the whole prompt. The skill fetches about 50 price series as CSVs, computes returns, spreads, volume z-scores and breadth in code, applies four written classification rules, and reports with every figure traced to the files.

## The verdict horizon

The skill defaults to a 5-day lens. Short windows and long windows can disagree, and that disagreement is information. Declare your lens before you look at the answer.

## Disclaimer

Educational and research purposes only. Nothing in this repository is investment advice or a recommendation. See 00-disclaimer.md.
