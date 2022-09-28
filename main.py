import json
import random
import cdifflib
from intent import Intent, IntentQuestion

MAX_MATCH_DELTA = 75
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Nutzerdaten, bspw: OS, Problem
data = {}

intents = []

# Eingangsmethode des Programms
def start():
    running = True
    intents = load_intents()
    while running:
        loop()

# Liest Eingabe des Nutzers
def read_input():
    print(bcolors.OKGREEN)
    input_tmp = input("Du: ")
    print(bcolors.ENDC)
    return input_tmp

# Liest den Input zu einer Frage, und speichert es in "data"
def ask_question(key: str):
    answer = read_input()
    data[key] = answer
    return answer

# Gibt die Antwort aus, aus der Sicht des Bots
def print_result(intent: Intent):
    print(bcolors.OKBLUE)
    if intent:
        if intent.Tag == "close":
            return print(data)

        print("Bot: " + random.choice(intent.Responses))
        if intent.Question and intent.Question.Variable:
            ask_question(intent.Question.Variable)
        if intent.Redirect:
            print_result(get_intent(intent.Redirect))
    else:
        print("Bot: Wir konnten nichts zu ihrer Anfrage finden. Bitte wenden Sie sich an den Support unter +49 123 45 67")
    return print(bcolors.ENDC)

# Gibt ein Intent zurück, abhängig vom tag
def get_intent(tag: str):
    intent = [x for x in intents if x.Tag == tag][0]
    return intent

# Gibt den Intent zur jeweiligen Message zurück
def find_intent(msg: str):
    words = msg.lower().split(" ")
    found = None
    for intent in intents:
        for word in words:
            for buzzword in intent.Buzzwords:
                diff = calculate_diff(word, buzzword)
                if diff > MAX_MATCH_DELTA:
                    found = intent
                    break
    return found

# Berechnet den Unterschied zwischen zwei Wörtern
def calculate_diff(w1: str, w2: str):
    seq = cdifflib.CSequenceMatcher(None, w1, w2)
    diff = seq.ratio()*100
    return diff

# Lädt die Antworten aus der intents.json
def load_intents():
    intents_tmp = []
    with open('./intents.json', mode='r', encoding='utf-8') as f:
        intents_raw = json.load(f)
        for intent in intents_raw["intents"]:
            obj = Intent()
            obj.Tag = intent["tag"]
            obj.Responses = intent["responses"]
            obj.Buzzwords = intent["buzzwords"]
            obj.Redirect = intent.get("redirect")
            obj.Question = IntentQuestion()
            obj.Question.Type = intent.get("question")["type"] if intent.get("question") else None
            obj.Question.Variable = intent.get("question")["variable"] if intent.get("question") else None
            intents.append(obj)
    return intents

# Hauptschleife zum lesen/ausgeben der Nachrichten
def loop():
    msg = read_input()
    intent = find_intent(msg)
    print_result(intent)

if __name__ == "__main__":
    start()