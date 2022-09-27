import json
from intent import Intent

# Eingangsmethode des Programms
def start():
    running = True
    intents = load_intents()
    print(intents)
    while running:
        loop()

# Liest Eingabe des Nutzers
def read_input():
    return input("Du: ")

# Gibt die Antwort aus, aus der Sicht des Bots
def print_result():
    return print("Bot: Answer!\n")

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
def loop():
    msg = read_input()
    print_result()


if __name__ == "__main__":
	start()