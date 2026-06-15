from anvil import *
import anvil.server

class DifficultyScreen(DifficultyScreenTemplate):
  def __init__(self, topic="", **properties):
    self.topic = topic
    self.init_components(**properties)
    self._build_ui()

  def _build_ui(self):
    self.add_component(Label(text="Maths Wizard", foreground="#6b7280"))
    self.add_component(Label(text=self.topic, bold=True, font_size=28))
    self.add_component(Label(text="Select a difficulty", foreground="#6b7280"))

    difficulties = [
      ("Easy", "⚡", "Fundamental concepts & definitions"),
      ("Medium", "⭐", "Applied techniques & problem solving"),
      ("Hard", "🔥", "Complex proofs & challenging problems"),
    ]
    for name, icon, desc in difficulties:
      btn = Button(text=f"{icon}  {name} — {desc}", full_width_row=True)
      btn.tag = name
      btn.set_event_handler('click', self._difficulty_clicked)
      self.add_component(btn)

    self.add_component(Label(
      text="10 questions  ·  90 second timer  ·  3 lives  ·  Points for speed",
      foreground="#9ca3af", font_size=11, align="center"
    ))

    back_btn = Button(text="← Back")
    back_btn.set_event_handler('click', self._back_clicked)
    self.add_component(back_btn)

  def _difficulty_clicked(self, sender, **event_args):
    open_form('QuizScreen', topic=self.topic, difficulty=sender.tag)

  def _back_clicked(self, sender, **event_args):
    open_form('HomeScreen')