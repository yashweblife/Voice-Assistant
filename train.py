import speech_recognition as sr
import pyttsx3
import random
import json
random.seed(123)
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)


def talk(val):
    engine.say(val)
    engine.runAndWait()


m = sr.Microphone()
r = sr.Recognizer()


def get_response():
    while True:
        with m as source:
            audio = r.listen(source)
        try:
            value = r.recognize_google(audio)
            return (value)
        except sr.UnknownValueError:
            print("Didnt catch that")


def addTo(name, location, attr, value):
    fs = open(name)
    data = json.load(fs)
    fs.close()
    data[location][attr].append(value)
    with open(name, "w") as out:
        json.dump(data,out)

def main():
    questions = [
        "how are you",
        "how is your day going",
        "how was your day",
    ]
    choice = random.choice(questions)
    talk(choice)
    val = get_response()
    addTo("./users.json", "questions", choice, val)

for _ in range(0,10):
    main()