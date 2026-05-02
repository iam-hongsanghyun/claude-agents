# HANDBOOK: Team Standards for Scientific Modelling Projects

**Scope:** Data science, energy modelling, finance, and economic modelling.
**Python:** 3.11+
**Audience:** Team members and contributors. (Claude reads `CLAUDE.md` — a slim version of this — for in-session context.)

This handbook is the human-facing source of truth. The slim `CLAUDE.md` at the repo root is a derivative for Claude's context window.

---

## 1. Tooling Choices (2024+)

We use a deliberately minimal modern stack:

| Concern | Tool | Replaces |
|---|---|---|
| Package manager | `uv` | pip + virtualenv + pip-tools |
| Build / config | `pyproject.toml` (hatchling) | `setup.py`, `requirements.txt` |
| Lint + format + sort imports | `ruff` | flake8 + black + isort |
| Type checker | `mypy` (strict) | — |
| Test runner | `pytest` + `pytest-cov` | unittest |
| Pre-commit | `pre-commit` | manual |
| Units | `pint` | bare floats |
| Tracking (optional) | `mlflow` or `wandb` | spreadsheets |
| Data versioning (optional) | `DVC` | ad-hoc S3 paths |

**Don't** introduce `setup.py`, `requirements.txt`, `flake8`, `black`, or `isort` to a new project. Everything goes through `pyproject.toml`.

---

## 2. Python Conventions

### Style
- Line length: **100**
- Formatter / linter: **ruff** (config in `pyproject.toml`)
- Import order: handled by ruff (isort rules)

### Type hints
Mandatory on public functions and class methods. Use `from __future__ import annotations` for forward refs in 3.11. mypy runs in strict mode; CI fails on errors.

### Naming

- Functions / variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- **Math variables (single letters)**: ALLOWED in `core/` modules and tests when they mirror published equations. Configured per-file in `[tool.ruff.lint.per-file-ignores]`. Don't write `temperature_kelvin` when the paper says `T`.

### Imports
Absolute imports for project code. Relative imports only within sibling modules of the same package.

---

## 3. Directory Layout

```
project_name/
├── .github/workflows/ci.yml
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── __version__.py
│       ├── core/                # ALGORITHMS — no I/O, no global state
│       │   ├── __init__.py
│       │   ├── model.py
│       │   └── solver.py
│       ├── data/                # I/O — loaders, validators, transforms
│       │   ├── __init__.py
│       │   ├── loaders.py
│       │   └── validators.py
│       ├── config.py            # .env → typed config
│       ├── logger.py            # centralized logging
│       └── cli.py               # CLI entry point (optional)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_core.py
│   ├── test_data.py
│   ├── test_integration.py
│   └── fixtures/
├── docs/
│   ├── README.md                # short user-facing intro
│   ├── ALGORITHM.md             # math / theory
│   ├── HANDBOOK.md              # this file
│   └── API.md                   # auto-generated from docstrings
├── notebooks/                   # OPTIONAL, gitignored exploration
├── .env, .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock                      # COMMIT this
└── CLAUDE.md                    # slim Claude context
```

**Why `src/` layout?** Forces you to install the package; you can't accidentally import from the working directory. Catches packaging bugs.

**Why split `core/` and `data/`?** So algorithms can be tested without filesystem or network. Data loading evolves on a different cadence than the math.

---

## 4. Configuration & Environment

### `.env` / `.env.example`

Every environment-specific value lives in `.env` (gitignored). Mirror the keys (without secret values) into `.env.example` (committed).

### `src/<pkg>/config.py` template

```python
"""Typed configuration loaded from .env."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # safe no-op if .env is missing


@dataclass(frozen=True)
class ModelConfig:
    alpha: float
    beta: float
    max_iterations: int


@dataclass(frozen=True)
class DataConfig:
    input_path: Path
    output_path: Path


@dataclass(frozen=True)
class Config:
    environment: str
    random_seed: int
    log_level: str
    log_file: Path
    model: ModelConfig
    data: DataConfig

    @classmethod
    def from_env(cls) -> "Config":
        env = os.getenv("ENVIRONMENT", "development").lower()
        if env not in ("development", "staging", "production"):
            raise ValueError(f"Invalid ENVIRONMENT: {env}")

        return cls(
            environment=env,
            random_seed=int(os.getenv("RANDOM_SEED", "42")),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            log_file=Path(os.getenv("LOG_FILE", "logs/app.log")),
            model=ModelConfig(
                alpha=float(os.getenv("MODEL_ALPHA", "0.3")),
                beta=float(os.getenv("MODEL_BETA", "0.5")),
                max_iterations=int(os.getenv("MAX_ITERATIONS", "1000")),
            ),
            data=DataConfig(
                input_path=Path(os.getenv("DATA_INPUT_PATH", "data/raw/")),
                output_path=Path(os.getenv("DATA_OUTPUT_PATH", "data/processed/")),
            ),
        )


CONFIG = Config.from_env()
```

`@dataclass(frozen=True)` ensures config is immutable after load.

---

## 5. Logging

### `src/<pkg>/logger.py` template

```python
"""Centralized logging."""
from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

from .config import CONFIG

_FMT = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, CONFIG.log_level))
    formatter = logging.Formatter(_FMT, _DATEFMT)

    # Console
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Rotating file
    log_file = Path(CONFIG.log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
```

### Usage
```python
from .logger import get_logger
log = get_logger(__name__)

log.info("Loaded %d rows from %s", len(df), path)
log.debug("Array shape=%s dtype=%s", arr.shape, arr.dtype)  # NEVER log arr itself
```

### Don't log
Secrets, PII, full arrays/dataframes, raw data rows. Log shape, dtype, or a hash if you need to confirm content.

---

## 6. Reproducibility (CRITICAL for scientific work)

This is non-negotiable for modelling work that gets shown to stakeholders.

### Random seeds
Always use the new generator API and accept a seed parameter:

```python
import numpy as np

def simulate(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.standard_normal(n)
```

Don't use the legacy global `np.random.seed()` — it leaks across modules.

### Lockfiles
Commit `uv.lock`. This is what makes "it works on my machine" actually transfer.

### Environment hash
Log Python version, key library versions, and (if relevant) git SHA at the start of long runs:

```python
import sys, numpy as np, scipy, pandas as pd
log.info("python=%s numpy=%s scipy=%s pandas=%s", sys.version.split()[0], np.__version__, scipy.__version__, pd.__version__)
```

### Determinism
For nondeterministic operations (multi-threaded BLAS, GPU), document it in the docstring. If determinism matters, set thread counts explicitly.

---

## 7. Units (use `pint`)

Currency, energy, power, time-of-day, temperature — all of these have caused real bugs in modelling work because someone passed `kWh` to a function expecting `MWh`. Use `pint` at module boundaries:

```python
import pint
ureg = pint.UnitRegistry()

energy = 100 * ureg.kilowatt_hour
power = energy / (1 * ureg.hour)
print(power.to(ureg.megawatt))  # 0.1 megawatt
```

Internal hot loops can use bare floats; convert at the boundary.

---

## 8. Documentation

### Docstring template

Google-style with an `Algorithm:` section for any function doing math:

```python
def solve_diffusion(
    initial_state: np.ndarray,
    diffusivity: float,
    dt: float,
    n_steps: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Solve 1D heat diffusion using forward-Euler finite differences.

    Algorithm:
        LaTeX:  $$u_t = D \\nabla^2 u$$
        ASCII:  u_t = D * laplacian(u)

        Discretization (interior, periodic BC):
            u[n+1, i] = u[n, i] + (D*dt/dx²) * (u[n, i+1] - 2*u[n, i] + u[n, i-1])

        Stability: CFL = D*dt/dx² ≤ 0.5

    Args:
        initial_state: Temperature profile, shape (n_grid,), units: K.
        diffusivity: D in m²/s. Must be > 0.
        dt: Time step in seconds. Must satisfy CFL.
        n_steps: Number of steps to integrate.

    Returns:
        history: shape (n_steps, n_grid), temperature trace.
        final: shape (n_grid,), temperature at last step.

    Raises:
        ValueError: if CFL violated or shape wrong.

    References:
        Strikwerda (2004), Finite Difference Schemes and PDEs, 2nd ed., §3.
    """
```

### `docs/ALGORITHM.md`
The full mathematical foundation of the project. Equations in LaTeX (with ASCII alongside for grep/diff), assumptions, validation methods, references.

### `docs/API.md`
Auto-generated from docstrings via `pdoc` or `sphinx`. Don't hand-maintain.

```bash
pdoc --output-dir docs/api/ src/project_name/
```

---

## 9. Testing

### What to test (priority order)
1. **Math correctness** against analytical solutions or captured baselines
2. **Edge cases** (empty input, single element, NaN, ±inf)
3. **Invariants** (conservation of energy, positivity, monotonicity where expected)
4. **Type/shape contracts** at module boundaries
5. Line coverage (least important — coverage is necessary not sufficient)

### Numerical comparison
Always specify tolerances explicitly:

```python
import numpy as np
np.testing.assert_allclose(result, expected, rtol=1e-7, atol=1e-12)
```

`assert result == expected` for floats is a bug.

### Markers
```python
@pytest.mark.slow      # skip with -m "not slow"
@pytest.mark.regression  # captured baselines
@pytest.mark.integration  # touches filesystem / network
```

### Fixtures (`tests/conftest.py`)
Share fixtures across test files. Prefer factory fixtures (functions that return objects) over module-level constants.

---

## 10. Code Review

### PR description template
```markdown
## Summary
What changed and why (one paragraph).

## Math (if applicable)
Before:  $$y = f(x)$$
After:   $$y = g(x)$$
Justification: ...

## Testing
- [ ] Unit tests added/updated
- [ ] Regression test against [analytical solution / baseline]
- [ ] Coverage of new code: __%

## Reproducibility
- [ ] Random seeds pinned where applicable
- [ ] No new hardcoded paths or magic numbers
- [ ] `.env.example` updated if new env vars added

## Breaking changes
None / [describe]
```

### Reviewer checklist
- Is the math correct? (re-derive on paper if non-trivial)
- Are tolerances justified? (`rtol=1e-7` not just `rtol=0.1`)
- Are units consistent at module boundaries?
- Are random seeds threaded through to where they're needed?
- Is the new code in `core/` or `data/`? (don't put I/O in `core/`)
- Any hardcoded paths or magic numbers?
- Tests for edge cases?

### Self-merge policy
For solo work, self-merging on green CI is acceptable IF you've done the self-review above. **CI passing is necessary but not sufficient** — numerical bugs routinely pass tests written by the same person who wrote the bug. Sleep on math changes when you can.

---

## 11. Git Workflow

### Branches
- Trunk: `main`
- Feature branches off `main`, no naming convention required (be readable)
- Delete branch after merge

### Commit messages (Conventional Commits)
```
feat: add radiative forcing parameterization
fix: handle zero-variance columns in normalize()
refactor: extract solver from monolithic train()
docs: clarify CFL condition in solve_diffusion docstring
test: regression test for Hansen 1988 baseline
chore: bump scipy to 1.13
```

### Merge strategy
- Squash-merge feature branches (clean history)
- Never `--force` push to `main`
- Use `git revert` to undo merged commits — not `reset --hard`

### Pre-commit
Optional but recommended:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
```

---

## 12. Modularity & Upgrades

### Stable vs experimental
Mark experimental APIs in docstrings:

```python
def stable_solve(...):
    """STABLE — public API, semantic versioning applies."""

def experimental_solve(...):
    """EXPERIMENTAL — interface may change without major version bump."""
```

### Deprecation
```python
import warnings

def old_function():
    warnings.warn(
        "old_function() is deprecated; use new_function()",
        DeprecationWarning,
        stacklevel=2,
    )
```

Keep deprecated functions for at least 2 minor releases.

### Major math changes
For breaking model changes, create a new module (`core/model_v2.py`) and let users opt in. Removing the old version is a major version bump.

---

## 13. Experiment Tracking (data science / ML)

For projects with many runs, use **MLflow** (self-hosted, free) or **W&B** (hosted, free for academic):

```python
import mlflow

with mlflow.start_run():
    mlflow.log_params({"alpha": alpha, "beta": beta, "seed": seed})
    result = train(data, alpha, beta, seed)
    mlflow.log_metric("rmse", result.rmse)
    mlflow.log_artifact("model.pkl")
```

`mlruns/` is gitignored by default. Track with `mlflow ui` locally, or push to a shared tracking server.

For data versioning, use **DVC** (`.dvc/` tracked, `data/` gitignored).

---

## 14. CI

See `.github/workflows/ci.yml` in this template. It runs ruff, mypy, and pytest with coverage on Python 3.11 and 3.12.

PRs cannot merge with red CI. Self-merge OK on green.

---

## 15. New Project Checklist

```bash
# from your projects root:
git init my-project && cd my-project

# Copy templates (or use scaffold script: ~/.claude/scripts/claude-scaffold.sh)
cp ~/.claude/templates/CLAUDE.md .
cp ~/.claude/templates/.gitignore .
cp ~/.claude/templates/.env.example .
cp ~/.claude/templates/pyproject.toml .
mkdir -p docs && cp ~/.claude/templates/docs/HANDBOOK.md docs/
mkdir -p .github/workflows && cp ~/.claude/templates/.github/workflows/ci.yml .github/workflows/

# Customize
# - rename "project_name" in pyproject.toml
# - create src/<pkg>/{__init__.py,config.py,logger.py,core/,data/}
# - create tests/conftest.py
# - write docs/ALGORITHM.md

# Initialize
uv venv && uv sync --all-extras
git add . && git commit -m "chore: initial commit from team template"
```

---

Last updated: 2026-05-02
