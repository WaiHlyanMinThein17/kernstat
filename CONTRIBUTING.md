# Contributing to kernstat

kernstat welcomes contributions from everyone. Contributing is an opportunity
to improve your technical skills, develop professionally, and participate in
open source Linux tooling.

## Before you start

Review the [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

kernstat is licensed under GPL-3.0. By contributing, you agree that your
changes will be distributed under the same license.

## Reporting issues

If you find a bug or have a feature request, search the
[GitHub issues](https://github.com/WaiHlyanMinThein17/kernstat/issues) first.
If no existing issue covers your case, open a new one with a clear description
and steps to reproduce.

## Setting up for development

kernstat uses a forking, feature-based workflow.

Start by creating a personal fork of the repository on GitHub, then clone
your fork:

```bash
git clone git@github.com:/kernstat.git
cd kernstat
git remote add upstream git@github.com:WaiHlyanMinThein17/kernstat.git
git fetch upstream
```

Set up the development environment:

```bash
uv sync
```

Verify everything is working:

```bash
uv run pytest
uvx ruff check src tests
```

## Making a change

Create a branch for your work:

```bash
git checkout -b feat/your-feature-name
```

Branch names should be brief and follow the format
`<type>/<short-description>`. For example, `feat/add-process-monitoring`
or `fix/cpu-division-by-zero`.

## Commit style

Format commit messages using
[Conventional Commits](https://www.conventionalcommits.org):
feat(cpu): add per-core CPU breakdown
fix(net): handle interface counter rollover
docs(readme): add installation instructions

## Testing

All non-trivial changes should include tests. Run the test suite with:

```bash
uv run pytest
```

Run formatting and linting:

```bash
uvx ruff format src tests
uvx ruff check src tests
```

All pull requests must pass CI before merging.

## Opening a pull request

Push your branch and open a pull request on GitHub. Title the PR after the
most significant change. Describe what the change does and why. Reference
any related issues.

Maintainers aim to review pull requests within a week.