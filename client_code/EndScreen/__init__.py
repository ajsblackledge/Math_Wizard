from anvil import *
import anvil.server

class EndScreen(EndScreenTemplate):
  def __init__(self, topic="", difficulty="", score=0, 
               reason="completed", correct=0, time_left=0, **properties):
    self.topic = topic
    self.difficulty = difficulty
    self.score = score
    self.reason = reason
    self.correct = correct
    self.time_left = time_left
    self.init_components(**properties)
    self._build_ui()

  def _build_ui(self):
    icons = {
      "completed": "🏆",
      "timeout": "⏱️",
      "no-lives": "💔"
    }
    titles = {
      "completed": "Quiz complete!",
      "timeout": "Time's up!",
      "no-lives": "Out of lives!"
    }
    time_used = 90 - self.time_left
    accuracy = round((self.correct / 10) * 100)
    lives_left = 0 if self.reason == "no-lives" else 3

    self.add_component(Label(text=f"{self.topic} ({self.difficulty})", 
                             foreground="#6b7280", align="right"))
    self.add_component(Label(text=icons.get(self.reason, "🏆"), 
                             font_size=40, align="center"))
    self.add_component(Label(text=titles.get(self.reason, "Done!"), 
                             foreground="#6b7280", align="center"))
    self.add_component(Label(text="You scored", font_size=18, 
                             bold=True, align="center"))
    self.add_component(Label(text=str(self.score), font_size=56, 
                             bold=True, align="center"))
    self.add_component(Label(text="points", foreground="#6b7280", 
                             align="center"))
    self.add_component(Label(text=f"❤️ Lives: {lives_left}/3"))
    self.add_component(Label(text=f"✅ Correct: {self.correct}/10"))
    self.add_component(Label(text=f"🕐 Time used: {time_used}s"))
    self.add_component(Label(text=f"Accuracy: {accuracy}%", bold=True))

    home_btn = Button(text="Back to home", full_width_row=True)
    home_btn.set_event_handler('click', self._home_clicked)
    self.add_component(home_btn)

  def _home_clicked(self, sender, **event_args):
    open_form('HomeScreen')