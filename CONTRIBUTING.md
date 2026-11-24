# Contributing

Contributions should improve field decisions, continuity, evidence quality, failure recovery, or technical depth without turning the Skill into a generic security knowledge base.

## Principles

- Preserve the evidence-driven control loop.
- Keep SKILL.md concise and route details through the relevant router.
- Add a card only for a distinct decision, prerequisite set, or return contract.
- Prefer improving an existing domain over adding a top-level domain.
- Keep one shared engagement state and parent attack-path graph.
- Separate observations from inferences and hypotheses.
- Explain success, negative, partial, and ambiguous results.
- Include failure diagnostics and an independent fallback for fragile techniques.
- Classify actions by impact, scale, persistence, reversibility, and business effect.
- Do not add fixed retry limits that cause shallow testing.
- Do not add tool lists without explaining how the capability changes a decision.
- Never submit real client data, credentials, tokens, keys, hostnames, or evidence.

## Where changes belong

- SKILL.md: core operator behavior and top-level routing.
- references/<domain>/router.md: domain entry and card selection.
- references/<domain>/*.md: domain-specific collection, validation, interpretation, and transitions.
- references/<capability>/: cross-cutting capabilities that return to a parent path.
- references/: shared workflow, state, safety, decision, evidence, and reporting contracts.
- scripts/: deterministic reusable helpers.
- agents/openai.yaml: user-facing Codex metadata.
- README files: repository documentation only, never runtime dependencies.

## Card expectations

A practical card should establish the bounded question, prerequisites, decision points, capability choices, expected observations, failure diagnosis, operational impact, evidence to retain, capability changes, affected paths, and return conditions.

Avoid duplicating content owned by another card. Route to the owning domain or capability while preserving the parent path.

## Local checks

~~~powershell
python scripts/session_state.py validate --path references/state-example.json
python -m py_compile scripts/session_state.py
~~~

For frontmatter or packaging changes, run `claude plugin validate .` (add `--strict` to treat
warnings as errors), `python scripts/check_sync.py` to confirm the plugin entry still matches the
root protocol, and `python scripts/check_budget.py` to confirm the always-on protocol stays within
its token budget. The budget check is exact only with `tiktoken` installed (`pip install tiktoken`);
without it the script prints a word-based estimate and stays green unless the text is clearly over,
so install `tiktoken` before trusting a pass. For Codex metadata, use the validator shipped with
Codex skill-creator when available. Review relative references after moving files. Exercise major
behavior changes only on sanitized synthetic scenarios.

## Pull requests

Describe the field problem, why existing behavior is insufficient, changed routing, state or compatibility impact, safety-level impact, checks performed, and remaining assumptions. Keep unrelated reformatting out of the same pull request.