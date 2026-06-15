from ._anvil_designer import DifficultyScreenTemplate
from anvil import *
import anvil.server


class DifficultyScreen(DifficultyScreenTemplate):
    """
    Level 2 – Difficulty Selection
    Shown after the user picks a topic. Displays Easy / Medium / Hard cards
    plus a quiz-info footer (10 questions · 90s · 3 lives · speed bonus).
    Raises 'difficulty_selected' or 'back_clicked' events.
    """

    def __init__(self, topic="", **properties):
        self.topic = topic
        self.init_components(**properties)
        self._setup_ui()

    def _setup_ui(self):
        self.lbl_topic_name.text = self.topic

    # ── Difficulty card handlers ─────────────────────────────────────────────

    def btn_easy_click(self, **event_args):
        self.raise_event("difficulty_selected", difficulty="Easy")

    def btn_medium_click(self, **event_args):
        self.raise_event("difficulty_selected", difficulty="Medium")

    def btn_hard_click(self, **event_args):
        self.raise_event("difficulty_selected", difficulty="Hard")

    def btn_back_click(self, **event_args):
        self.raise_event("back_clicked")
