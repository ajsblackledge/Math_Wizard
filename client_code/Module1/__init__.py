from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.server

from ..HomeScreen import HomeScreen
from ..DifficultyScreen import DifficultyScreen
from ..QuizScreen import QuizScreen
from ..EndScreen import EndScreen


class MainForm(MainFormTemplate):
    """
    Root navigation controller — mirrors App.tsx state machine.

    Screen flow (taxonomy):
      home → difficulty → quiz → end → home

    State:
      _screen   : "home" | "difficulty" | "quiz" | "end"
      _topic    : str | None
      _difficulty : str | None
      _result   : dict | None  (score, reason, correct_count, time_left, time_used)
    """

    def __init__(self, **properties):
        self.init_components(**properties)
        self._topic = None
        self._difficulty = None
        self._result = None
        self._go_home()

    # ── Navigation helpers ────────────────────────────────────────────────────

    def _clear_content(self):
        self.content_panel.clear()

    def _go_home(self):
        self._clear_content()
        hs = HomeScreen()
        hs.add_event_handler("topic_selected", self._on_topic_selected)
        self.content_panel.add_component(hs)

    def _go_difficulty(self):
        self._clear_content()
        ds = DifficultyScreen(topic=self._topic)
        ds.add_event_handler("difficulty_selected", self._on_difficulty_selected)
        ds.add_event_handler("back_clicked", self._on_back_to_home)
        self.content_panel.add_component(ds)

    def _go_quiz(self):
        self._clear_content()
        qs = QuizScreen(topic=self._topic, difficulty=self._difficulty)
        qs.add_event_handler("quiz_ended", self._on_quiz_ended)
        qs.add_event_handler("exit_clicked", self._on_exit_quiz)
        self.content_panel.add_component(qs)

    def _go_end(self):
        self._clear_content()
        es = EndScreen(
            topic=self._topic,
            difficulty=self._difficulty,
            score=self._result["score"],
            reason=self._result["reason"],
            correct_count=self._result["correct_count"],
            time_left=self._result["time_left"],
        )
        es.add_event_handler("home_clicked", self._on_back_to_home)
        self.content_panel.add_component(es)

    # ── Event handlers ────────────────────────────────────────────────────────

    def _on_topic_selected(self, topic, **event_args):
        self._topic = topic
        self._difficulty = None
        self._result = None
        self._go_difficulty()

    def _on_difficulty_selected(self, difficulty, **event_args):
        self._difficulty = difficulty
        self._go_quiz()

    def _on_quiz_ended(self, result, **event_args):
        self._result = result
        self._go_end()

    def _on_exit_quiz(self, **event_args):
        """Exit mid-quiz → back to difficulty selection."""
        self._go_difficulty()

    def _on_back_to_home(self, **event_args):
        self._topic = None
        self._difficulty = None
        self._result = None
        self._go_home()
