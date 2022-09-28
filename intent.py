class IntentQuestion():
  def __init__(self):
    self.Type = None
    self.Variable = None

class Intent():
  def __init__(self):
    self.Tag = None
    self.Responses = None
    self.Buzzwords = None
    self.Redirect = None
    self.Question = IntentQuestion()