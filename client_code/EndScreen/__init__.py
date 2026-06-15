from ._anvil_designer import EndScreenTemplate
from anvil import *
import anvil.server


class EndScreen(EndScreenTemplate):
    """
    Level 4 – End Screen
    Displays result for three end-states:
      • completed  → Trophy icon, "Quiz complete!"
      • timeout    → TimerOff icon, "Time's up!"
      • no-lives   → HeartOff icon, "Out of lives!"

    Shows: score (large), lives remaining, correct/10, time used, accuracy bar.
    Raises 'home_clicked' event when the user taps "Back to Home".
    """

    TOTAL_QUESTIONS = 10
    TOTAL_LIVES = 3
    TOTAL_TIME = 90

    REASON_MAP = {
        "completed": {"title": "Quiz complete!", "icon": "🏆", "color": "#f59e0b"},
        "timeout":   {"title": "Time's up!",     "icon": "⏱️", "color": "#3b82f6"},
        "no-lives":  {"title": "Out of lives!",  "icon": "💔", "color": "#ef4444"},
    }

    def __init__(
        self,
        topic="",
        difficulty="",
        score=0,
        reason="completed",
        correct_count=0,
        time_left=0,
        **properties,
    ):
        self.topic = topic
        self.difficulty = difficulty
        self.score = score
        self.reason = reason
        self.correct_count = correct_count
        self.time_left = time_left
        self.init_components(**properties)
        self._render()

    def _render(self):
        meta = self.REASON_MAP.get(self.reason, self.REASON_MAP["completed"])
        time_used = self.TOTAL_TIME - self.time_left
        accuracy = round((self.correct_count / self.TOTAL_QUESTIONS) * 100)
        lives_remaining = 0 if self.reason == "no-lives" else self.TOTAL_LIVES

        # Topic label
        self.lbl_topic.text = f"{self.topic}  ({self.difficulty})"

        # Status
        self.lbl_status_icon.text = meta["icon"]
        self.lbl_status_title.text = meta["title"]
        self.lbl_score_label.text = "You scored"
        self.lbl_score.text = str(self.score)
        self.lbl_points.text = "points"

        # Stats cards
        hearts_full = "❤️ " * lives_remaining
        hearts_empty = "🖤 " * (self.TOTAL_LIVES - lives_remaining)
        self.lbl_stat_lives_val.text = f"{lives_remaining}/{self.TOTAL_LIVES}"
        self.lbl_stat_correct_val.text = f"{self.correct_count}/{self.TOTAL_QUESTIONS}"
        self.lbl_stat_time_val.text = f"{time_used}s"

        # Accuracy bar
        self.lbl_accuracy_pct.text = f"{accuracy}%"
        self.accuracy_bar.value = accuracy
        if accuracy >= 70:
            self.accuracy_bar.foreground = "#10b981"  # emerald
        elif accuracy >= 40:
            self.accuracy_bar.foreground = "#f59e0b"  # amber
        else:
            self.accuracy_bar.foreground = "#ef4444"  # red

    def btn_home_click(self, **event_args):
        self.raise_event("home_clicked")
