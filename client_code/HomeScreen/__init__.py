from ._anvil_designer import HomeScreenTemplate
from anvil import *
import anvil.server


class HomeScreen(HomeScreenTemplate):
    """
    Level 1 – Home Screen
    Displays a 2×2 grid of topic cards: Differentiation, Integration, Graphs, Circles.
    Raises the 'topic_selected' event when the user taps a card.
    """

    def __init__(self, **properties):
        self.init_components(**properties)
        self._load_topics()

    def _load_topics(self):
        """Populate topic cards from the server."""
        topics = anvil.server.call("get_topics")
        # Map topic name → card panel in the form
        card_map = {
            "Differentiation": self.card_differentiation,
            "Integration": self.card_integration,
            "Graphs": self.card_graphs,
            "Circles": self.card_circles,
        }
        # Apply topic metadata to each card
        desc_map = {
            "Differentiation": self.lbl_desc_differentiation,
            "Integration": self.lbl_desc_integration,
            "Graphs": self.lbl_desc_graphs,
            "Circles": self.lbl_desc_circles,
        }
        for topic in topics:
            name = topic["name"]
            if name in desc_map:
                desc_map[name].text = topic["description"]

    # ── Card click handlers ──────────────────────────────────────────────────

    def card_differentiation_click(self, **event_args):
        self.raise_event("topic_selected", topic="Differentiation")

    def card_integration_click(self, **event_args):
        self.raise_event("topic_selected", topic="Integration")

    def card_graphs_click(self, **event_args):
        self.raise_event("topic_selected", topic="Graphs")

    def card_circles_click(self, **event_args):
        self.raise_event("topic_selected", topic="Circles")
