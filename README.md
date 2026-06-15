# Maths Wizard Quiz — Anvil Application

Converted from the React/Figma Make prototype into a full Anvil application.

---

## Architecture Overview

```
MathsWizardQuiz/
├── anvil.yaml                         ← App manifest & service declarations
├── theme/
│   └── theme.css                      ← Design tokens (ported from Tailwind/theme.css)
├── client_code/
│   ├── Module1/                       ← Root navigation controller (MainForm)
│   │   ├── __init__.py                ← Python: screen state machine
│   │   └── MainForm.yaml              ← Layout: phone-frame card + content_panel
│   ├── HomeScreen/                    ← Level 1 – Home (topic picker)
│   │   ├── __init__.py
│   │   └── HomeScreen.yaml
│   ├── DifficultyScreen/              ← Level 2 – Difficulty picker
│   │   ├── __init__.py
│   │   └── DifficultyScreen.yaml
│   ├── QuizScreen/                    ← Level 3 – Active quiz
│   │   ├── __init__.py                ← Timer, lives, scoring, answer logic
│   │   └── QuizScreen.yaml
│   ├── EndScreen/                     ← Level 4 – Results (3 variants)
│   │   ├── __init__.py
│   │   └── EndScreen.yaml
│   └── MathsLabel/                    ← Custom component: LaTeX via MathJax 3
│       └── __init__.py
└── server_code/
    ├── ServerModule1.py               ← All 120 questions, server callables, DB writes
    └── data_tables_schema.yaml        ← Data Table: quiz_results
```

---

## Navigation Flow (from Taxonomy doc)

```
Home Screen
 └─ [select topic]
     └─ Difficulty Selection  (Easy | Medium | Hard)
          └─ [select difficulty]
               └─ Quiz Questions  (10 questions, 90s timer, 3 lives)
                    ├─ completed  ──┐
                    ├─ timeout    ──┤─→ End Screen ──→ Home Screen
                    └─ no-lives  ──┘
```

---

## Forms

### MainForm (Module1)
Root layout. Holds a `content_panel` into which child screens are swapped.  
Mirrors `App.tsx` — manages `_topic`, `_difficulty`, `_result` state and
responds to events raised by child forms.

### HomeScreen
- 2×2 grid of topic cards: Differentiation (📈 blue), Integration (🧮 emerald),
  Graphs (📖 violet), Circles (⭕ orange).
- Raises `topic_selected(topic)`.

### DifficultyScreen
- Back button → raises `back_clicked`.
- Three difficulty cards: Easy (⚡ green), Medium (⭐ amber), Hard (🔥 red).
- Footer: "10 questions · 90 second timer · 3 lives · Points for speed"
- Raises `difficulty_selected(difficulty)`.

### QuizScreen
- **Timer**: Anvil `Timer` component fires every second; colour shifts
  green → amber (≤30s) → red (≤10s).
- **Lives**: 3 hearts; wrong answer removes one. Zero lives → `no-lives` end.
- **Score**: 100 base + speed bonus `max(0, round((10 − elapsed_seconds) × 10))`
  per correct answer.
- **Progress bar**: advances per question.
- **Answer feedback**: correct = green highlight; wrong = red on selected +
  green on correct.
- Raises `quiz_ended(result)` or `exit_clicked`.

### EndScreen
Three end-state variants driven by `reason` parameter:

| reason      | Icon | Colour  |
|-------------|------|---------|
| completed   | 🏆   | amber   |
| timeout     | ⏱️   | blue    |
| no-lives    | 💔   | red     |

Displays: score (large), lives remaining / 3, correct / 10, time used,
accuracy percentage bar (green ≥ 70%, amber ≥ 40%, red < 40%).

---

## Custom Component: MathsLabel

Renders LaTeX strings using **MathJax 3** (loaded from CDN).  
Supports inline `$…$` and display `$$…$$` delimiters, exactly matching the
React `<Latex>` component from the original codebase.

```python
from ..MathsLabel import MathsLabel

widget = MathsLabel(
    text=r"What is $\frac{d}{dx}(x^2)$?",
    font_size=20,
    bold=True,
)
self.content_panel.add_component(widget)
```

---

## Server Module (ServerModule1.py)

### Callable functions

| Function | Arguments | Returns |
|----------|-----------|---------|
| `get_topics()` | — | `list[dict]` — topic metadata |
| `get_difficulties()` | — | `list[dict]` — difficulty metadata |
| `get_questions(topic, difficulty)` | `str, str` | `list[dict]` — 10 question dicts |
| `get_quiz_config()` | — | `dict` — TOTAL_TIME/LIVES/QUESTIONS |
| `calculate_score(correct_answers, time_per_question_seconds)` | `list[bool], list[float]` | `int` |
| `save_quiz_result(topic, difficulty, score, correct_count, reason, time_used)` | — | `bool` |
| `get_leaderboard(topic, difficulty, limit)` | optional filters | `list[dict]` |

---

## Data Table: quiz_results

| Column | Type | Description |
|--------|------|-------------|
| `topic` | string | Differentiation / Integration / Graphs / Circles |
| `difficulty` | string | Easy / Medium / Hard |
| `score` | number | Final score |
| `correct_count` | number | Correct answers (0–10) |
| `reason` | string | completed / timeout / no-lives |
| `time_used` | number | Seconds elapsed |
| `completed_at` | datetime | Timestamp |

Create this table in the Anvil editor: **Data → Add Table → quiz_results**,
then add the columns above.

---

## Setup Instructions

1. **Create a new Anvil app** at [anvil.works](https://anvil.works).
2. **Enable the Data Tables service** (App → Services → Data Tables).
3. **Create the `quiz_results` table** using the schema above.
4. Copy each file from this package into the corresponding Anvil editor location:
   - `server_code/ServerModule1.py` → Server Module
   - `client_code/*/` → Forms (create each Form with the matching name)
   - `theme/theme.css` → Theme → Custom CSS
5. Set **MainForm** (Module1) as the startup form.
6. The **MathJax CDN** is loaded automatically by the `MathsLabel` component —
   no additional dependency needed.

---

## Quiz Content

**120 questions** across 4 topics × 3 difficulties × 10 questions each:

- **Differentiation**: Power rule, chain/product/quotient rules, implicit
  differentiation, inverse trig, hyperbolic functions.
- **Integration**: Standard integrals, substitution, integration by parts,
  partial fractions, definite integrals.
- **Graphs**: Parabolas, transformations (translations/stretches/reflections),
  asymptotes, inverse functions, parametric curves.
- **Circles**: Standard/general form, tangents/normals, intersection with lines,
  circle theorems, concentric circles.

All questions use **LaTeX** notation for mathematical expressions, rendered
client-side by MathJax 3.
