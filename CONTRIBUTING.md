# Contributing

Thanks for helping. Three kinds of contribution are especially useful.

## 1. A new hypothesis

1. Read [docs/METHODOLOGY.md](docs/METHODOLOGY.md) and the format in [docs/WORKFLOWS.md](docs/WORKFLOWS.md#hypothesis-format).
2. Copy a file in `hypotheses/` to the next free ID, set `status: draft`, `author:` your GitHub
   handle, and explain in `rationale` **why** the idea should work. Write this before looking at
   any results.
3. `crl registry check` must pass. It rejects unknown rules, wrong parameters and re-worded duplicates.
4. Open a pull request. A maintainer runs `crl registry register H-0NN` to lock it. The weekly
   runner tests it, and the result appears on the dashboard.

Rules of the game: no tuning after seeing results (make a new hypothesis instead), always
include fees, and prefer confirmation on coins that weren't used to design the idea.

Not a coder? Open an issue with the **Hypothesis idea** template.

## 2. Translations

All dashboard text is in [`src/crl/i18n.py`](src/crl/i18n.py). To fix a translation, edit the
string. To add a language, copy the `"en"` block, translate it and add the language to `LANGS`.
`pytest` checks that no key is missing. Engine output (summaries, specs) stays in English on purpose.

## 3. Code

```bash
pip install -e ".[dev]"
pytest -q && crl registry check
```

Keep changes small and tested. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
(`feat:`, `fix:`, `docs:` …). Every timestamp is UTC. A decision made at a day's close may only use
data available at that close.
