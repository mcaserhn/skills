# English document template (copy-paste)

> `de-ai-flavor` asset. Pipeline: `references/04-doc-pipeline-and-faq.md`; parameters: same file, "tunable options".

## Full template (with persona / audience)

```
Persona: [e.g., "a staff engineer with 10 years' experience, writing an internal postmortem for the team"]
Audience: [e.g., "frontline engineers who know Kubernetes"]
Style rules:
- Get to the point. No openers like "In today's fast-paced world" or "It is important to note".
- No hedge filler: might, perhaps, to some extent, arguably, it could be said that.
- No buzzwords: leverage, seamless, robust, delve, navigate, empower, unlock, game-changer, synergy, ecosystem, streamline, holistic, cutting-edge.
- Make definitive statements. If unsure, say "unverified / TBD" — don't blur it.
- Order by logic, not by a forced "First / Second / Finally".
- First person and honest judgment are allowed, but judgment must be backed by evidence.
Material (must be cited, do not generalize from nothing):
[paste real data / quotes / cases / logs]
Output: [e.g., "a 400-word postmortem with root cause, impact, next steps"]
After generating, do one self-de-AI pass: cut every removable modifier, replace each abstraction with a concrete action or number.
```

## Minimal template (no persona / audience; essentials only)

```
Write like a real human expert, not an AI assistant. Assume the reader is a practitioner in the field; skip beginner explainers.
Forbid the following: [paste the English banned list]
Every claim needs evidence (number / name / action). No generalizations from nothing.
Material: [paste real data / quotes / cases]
Output: [specific deliverable]
Do one self-de-AI pass after generating.
```
