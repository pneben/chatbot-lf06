import json
import random
import cdifflib
from intent import Intent

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

# Eingangsmethode des Programms
def start():
    running = True
    intents = load_intents()
    while running:
        loop(intents)

# Liest Eingabe des Nutzers
def read_input():
    print(bcolors.OKGREEN)
    input_tmp = input("Du: ")
    print(bcolors.ENDC)
    return input_tmp

# Gibt die Antwort aus, aus der Sicht des Bots
def print_result(intent: Intent):
    print(bcolors.OKBLUE)
    if intent:
        print("Bot: " + random.choice(intent.Responses))
    else:
        print("Bot: Wir konnten nichts zu ihrer Anfrage finden. Bitte wenden Sie sich an den Support unter +49 0123-456-78")
    return print(bcolors.ENDC)

# Gibt den Intent zur jeweiligen Message zurück
def find_intent(msg: str, intents: list[Intent]):
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
    intents = []
    with open('./intents.json', mode='r', encoding='utf-8') as f:
        intents_raw = json.load(f)
        for intent in intents_raw["intents"]:
            obj = Intent()
            obj.Tag = intent["tag"]
            obj.Responses = intent["responses"]
            obj.Buzzwords = intent["buzzwords"]
            intents.append(obj)
    return intents

# Hauptschleife zum lesen/ausgeben der Nachrichten
def loop(intents):
    msg = read_input()
    intent = find_intent(msg, intents)
    print_result(intent)


if __name__ == "__main__":
    start()