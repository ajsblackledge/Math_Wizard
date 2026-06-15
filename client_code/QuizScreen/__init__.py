from anvil import *
import anvil.server
import time

class QuizScreen(QuizScreenTemplate):
  def __init__(self, topic="", difficulty="", **properties):
    self.topic = topic
    self.difficulty = difficulty
    self.init_components(**properties)
    self._questions = anvil.server.call('get_questions', topic, difficulty)
    self._index = 0
    self._lives = 3
    self._score = 0
    self._correct = 0
    self._time_left = 90
    self._locked = False
    self._start = time.time()
    self._build_ui()
    self._timer = Timer(interval=1)
    self._timer.set_event_handler('tick', self._tick)
    self.add_component(self._timer)

  def _build_ui(self):
    self._lbl_info = Label(text=f"{self.topic} ({self.difficulty})", align="center")
    self._lbl_lives = Label(text="❤️ ❤️ ❤️", font_size=18)
    self._lbl_score = Label(text="⭐ 0", bold=True)
    self._lbl_timer = Label(text="90s", bold=True)
    self._lbl_progress = Label(text="Question 1 of 10", foreground="#6b7280")
    self._lbl_question = Label(text="", bold=True, font_size=18)
    self._option_btns = []
    for i in range(4):
      btn = Button(text="", full_width_row=True)
      btn.tag = i
      btn.set_event_handler('click', self._answer_clicked)
      self._option_btns.append(btn)
    for c in [self._lbl_info, self._lbl_lives, self._lbl_score,
              self._lbl_timer, self._lbl_progress, self._lbl_question]:
      self.add_component(c)
    for btn in self._option_btns:
      self.add_component(btn)
    self._show_question()

  def _tick(self, **event_args):
    self._time_left -= 1
    self._lbl_timer.text = f"{self._time_left}s"
    if self._time_left <= 30:
      self._lbl_timer.foreground = "#f59e0b"
    if self._time_left <= 10:
      self._lbl_timer.foreground = "#ef4444"
    if self._time_left <= 0:
      self._end("timeout")

  def _show_question(self):
    q = self._questions[self._index]
    self._lbl_progress.text = f"Question {self._index + 1} of 10"
    self._lbl_question.text = q['question']
    labels = ["A", "B", "C", "D"]
    for i, btn in enumerate(self._option_btns):
      btn.text = f"{labels[i]}   {q['options'][i]}"
      btn.enabled = True
      btn.background = "#ffffff"
    self._locked = False
    self._start = time.time()

  def _answer_clicked(self, sender, **event_args):
    if self._locked:
      return
    self._locked = True
    q = self._questions[self._index]
    chosen = sender.tag
    elapsed = time.time() - self._start
    for btn in self._option_btns:
      btn.enabled = False
    if chosen == q['correctIndex']:
      bonus = max(0, round((10 - elapsed) * 10))
      self._score += 100 + bonus
      self._correct += 1
      self._lbl_score.text = f"⭐ {self._score}"
      sender.background = "#d1fae5"
    else:
      self._lives -= 1
      hearts = "❤️ " * self._lives + "🖤 " * (3 - self._lives)
      self._lbl_lives.text = hearts.strip()
      sender.background = "#fee2e2"
      self._option_btns[q['correctIndex']].background = "#d1fae5"
      if self._lives <= 0:
        self._end("no-lives")
        return
    self._index += 1
    if self._index >= 10:
      self._end("completed")
    else:
      self._show_question()

  def _end(self, reason):
    self._timer.interval = 0
    anvil.server.call('save_quiz_result', self.topic, self.difficulty,
                      self._score, self._correct, reason, 90 - self._time_left)
    open_form('EndScreen', topic=self.topic, difficulty=self.difficulty,
              score=self._score, reason=reason, correct=self._correct,
              time_left=self._time_left)