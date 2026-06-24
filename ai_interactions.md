# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
review @app.py  and  @logic_utils.py  for PEP 8 style compliance and generate suggestions to resolve any formatting or naming issues you identify
```

**Linting output before:**
I didn't realize it skipped using linting tools because they weren't installed and instead decided to do it programmatically. I've pasted the results of that run below.
```
### 1. Line too long — E501 (app.py:8, 82 > 79 chars)
### 2. Missing blank line between import groups — E305/PEP 8 import grouping (app.py:1-2)
### 3. Naming — module-level constant should be UPPER_CASE (app.py:27)
### 4. Consistency — missing type hints (logic_utils.py:106, 153) [optional, style]
```

**Changes applied:**

```
app.py:
Added a blank line between the standard-library import (random) and the third-party import (streamlit).
Moved the # FIX: comment onto its own line above should_reset_for_difficulty_change, so the import line is no longer over 79 characters.
Renamed the constant dictionary attempt_limit_map to ATTEMPT_LIMIT_MAP (uppercase, since it's a module-level constant), updating both where it's defined and where it's used.

logic_utils.py:
Added type hints for consistency with the other functions: parse_guess(raw: str | None) and a -> tuple[str, str] return annotation on check_guess.
```
---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
