# Contributing to KB Agents

Thanks for your interest in contributing!

## Branch Conventions

- `main` — stable releases only, protected
- `develop` — default working branch, all PRs target here
- `feature/<name>` — new features
- `fix/<name>` — bug fixes

## Workflow

1. Fork the repo and create your branch from `develop`
2. Make your changes
3. Ensure tests pass: `pip install pytest && pytest -v`
4. Open a Pull Request against `develop`

## Tests

All Python scripts in `_bmad-output/*/scripts/` have corresponding tests in `scripts/tests/`. When modifying a script, update or add tests accordingly.

Run the full test suite:

```bash
pip install pytest
pytest -v
```

## Release Process

Releases are created by merging `develop` into `main` via a Pull Request with a title containing the version (e.g., "Release v0.2.0"). The GitHub Actions workflow automatically creates a release.

## Code Style

- Python scripts use stdlib only (no external dependencies)
- Shell scripts should pass `shellcheck`
- Keep agent capability prompts in Markdown with YAML frontmatter

## Questions?

Open an issue — we're happy to help.
