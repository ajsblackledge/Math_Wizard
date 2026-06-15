from ._anvil_designer import QuizScreenTemplate
from anvil import *
import anvil.server
import time


class QuizScreen(QuizScreenTemplate):
    """
    Level 3 – Quiz Questions
    Manages the full quiz loop:
      • 10 questions per session
      • 90-second countdown timer (anvil.js timer via JavaScript or polling)
      • 3 lives — wrong answer costs one life
      • Speed bonus: max(0, (10 - elapsed_seconds) × 10) added to base 100
      • Ends on: completed (all 10 done) | timeout | no-lives
    Raises 'quiz_ended' with result dict, or 'exit_clicked'.
    """

    TOTAL_TIME = 90
    TOTAL_LIVES = 3
    TOTAL_QUESTIONS = 10
    OPTION_LABELS = ["A", "B", "C", "D"]

    def __init__(self, topic="", difficulty="", **properties):
        self.topic = topic
        self.difficulty = difficulty
        self.init_components(**properties)

        # State
        self._questions = []
        self._current_index = 0
        self._lives = self.TOTAL_LIVES
        self._score = 0
        self._correct_count = 0
        self._time_left = self.TOTAL_TIME
        self._locked = False
        self._ended = False
        self._question_start = None
        self._timer = None

        self._load_questions()

    # ── Setup ────────────────────────────────────────────────────────────────

    def _load_questions(self):
        self._questions = anvil.server.call("get_questions", self.topic, self.difficulty)
        self._show_question()
        self._start_timer()

    def _start_timer(self):
        """Start a 1-second repeating timer."""
        self._timer = anvil.js.call("setInterval", self._tick, 1000) if hasattr(anvil, 'js') else None
        # Anvil built-in timer component (Timer component on form):
        self.timer_component.interval = 1
        self.timer_component.enabled = True

    def timer_component_tick(self, **event_args):
        """Called every second by the Timer component."""
        if self._ended:
            return
        self._time_left -= 1
        self._update_timer_display()
        if self._time_left <= 0:
            self._end_quiz("timeout")

    def _update_timer_display(self):
        t = self._time_left
        self.lbl_timer.text = f"{t}s"
        if t > 30:
            self.lbl_timer.foreground = "#111827"
        elif t > 10:
            self.lbl_timer.foreground = "#f59e0b"
        else:
            self.lbl_timer.foreground = "#ef4444"

    # ── Question display ──────────────────────────────────────────────────────

    def _show_question(self):
        if self._current_index >= len(self._questions):
            return
        q = self._questions[self._current_index]

        # Progress
        progress_pct = int((self._current_index / self.TOTAL_QUESTIONS) * 100)
        self.progress_bar.foreground = f"oklch(0.546 0.245 262.881)"  # primary blue
        self.lbl_progress.text = f"Question {self._current_index + 1} of {self.TOTAL_QUESTIONS}"

        # Lives
        hearts = ("❤️ " * self._lives) + ("🖤 " * (self.TOTAL_LIVES - self._lives))
        self.lbl_lives.text = hearts.strip()

        # Score
        self.lbl_score.text = f"⭐ {self._score}"

        # Header
        self.lbl_topic_header.text = f"{self.topic}  ({self.difficulty})"

        # Question text (LaTeX rendered by MathJax custom component)
        self.lbl_question.text = q["question"]

        # Options
        option_btns = [self.btn_a, self.btn_b, self.btn_c, self.btn_d]
        for i, btn in enumerate(option_btns):
            if i < len(q["options"]):
                btn.text = f"{self.OPTION_LABELS[i]}   {q['options'][i]}"
                btn.visible = True
                btn.background = "#ffffff"
                btn.foreground = "#111827"
                btn.border = "2px solid #e5e7eb"
                btn.enabled = True
            else:
                btn.visible = False

        self._locked = False
        self._question_start = time.time()

    def _reset_option_styles(self):
        for btn in [self.btn_a, self.btn_b, self.btn_c, self.btn_d]:
            btn.background = "#ffffff"
            btn.foreground = "#111827"
            btn.border = "2px solid #e5e7eb"

    # ── Answer handling ───────────────────────────────────────────────────────

    def _handle_answer(self, option_index):
        if self._locked or self._ended:
            return
        self._locked = True

        q = self._questions[self._current_index]
        is_correct = option_index == q["correctIndex"]
        elapsed = time.time() - self._question_start

        option_btns = [self.btn_a, self.btn_b, self.btn_c, self.btn_d]
        # Disable all
        for btn in option_btns:
            btn.enabled = False

        if is_correct:
            speed_bonus = max(0, round((10 - elapsed) * 10))
            points = 100 + speed_bonus
            self._score += points
            self._correct_count += 1
            # Style correct button green
            option_btns[option_index].background = "#d1fae5"
            option_btns[option_index].foreground = "#065f46"
            option_btns[option_index].border = "2px solid #34d399"
        else:
            self._lives -= 1
            # Style selected wrong
            option_btns[option_index].background = "#fee2e2"
            option_btns[option_index].foreground = "#7f1d1d"
            option_btns[option_index].border = "2px solid #f87171"
            # Reveal correct
            option_btns[q["correctIndex"]].background = "#d1fae5"
            option_btns[q["correctIndex"]].foreground = "#065f46"
            option_btns[q["correctIndex"]].border = "2px solid #34d399"

        # Update live display
        hearts = ("❤️ " * self._lives) + ("🖤 " * (self.TOTAL_LIVES - self._lives))
        self.lbl_lives.text = hearts.strip()
        self.lbl_score.text = f"⭐ {self._score}"

        if not is_correct and self._lives <= 0:
            # Short delay then end
            anvil.js.window.setTimeout(lambda: self._end_quiz("no-lives"), 800) if hasattr(anvil, 'js') else self._end_quiz("no-lives")
            return

        # Advance after short pause
        next_index = self._current_index + 1
        if next_index >= self.TOTAL_QUESTIONS:
            anvil.js.window.setTimeout(lambda: self._end_quiz("completed"), 600) if hasattr(anvil, 'js') else self._end_quiz("completed")
        else:
            self._current_index = next_index
            # Brief pause then load next question
            self._schedule_next_question()

    def _schedule_next_question(self):
        """Move to next question. Called after answer feedback delay."""
        self._show_question()

    # Option button click handlers
    def btn_a_click(self, **event_args):
        self._handle_answer(0)

    def btn_b_click(self, **event_args):
        self._handle_answer(1)

    def btn_c_click(self, **event_args):
        self._handle_answer(2)

    def btn_d_click(self, **event_args):
        self._handle_answer(3)

    # ── Exit ─────────────────────────────────────────────────────────────────

    def btn_exit_click(self, **event_args):
        self._ended = True
        self.timer_component.enabled = False
        self.raise_event("exit_clicked")

    # ── End quiz ─────────────────────────────────────────────────────────────

    def _end_quiz(self, reason):
        if self._ended:
            return
        self._ended = True
        self.timer_component.enabled = False

        result = {
            "score": self._score,
            "reason": reason,
            "correct_count": self._correct_count,
            "time_left": self._time_left,
            "time_used": self.TOTAL_TIME - self._time_left,
        }
        # Persist to Data Table (non-blocking on error)
        try:
            anvil.server.call_s(
                "save_quiz_result",
                self.topic,
                self.difficulty,
                self._score,
                self._correct_count,
                reason,
                self.TOTAL_TIME - self._time_left,
            )
        except Exception:
            pass

        self.raise_event("quiz_ended", result=result)
