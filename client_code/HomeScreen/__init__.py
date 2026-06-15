from anvil import *
import anvil.server

class HomeScreen(HomeScreenTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self._build_ui()

  def _build_ui(self):
    topics = [
      ("Differentiation", "📈", "Rates of change & gradients", "blue"),
      ("Integration", "🧮", "Areas & anti-derivatives", "green"),
      ("Graphs", "📖", "Transformations & sketching", "purple"),
      ("Circles", "⭕", "Equations & geometry", "orange"),
    ]
    for name, icon, desc, color in topics:
      btn = Button(text="{} {}\n{}".format(icon, name, desc), full_width_row=True)
      btn.tag = name
      btn.set_event_handler('click', self._topic_clicked)
      self.add_component(btn)

  def _topic_clicked(self, sender, **event_args):
    topic = sender.tag
    open_form('DifficultyScreen', topic=topic)