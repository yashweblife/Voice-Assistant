import speech_recognition as sr
import time
from datetime import datetime
import webbrowser
import os
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def talk(val):
    engine.say(val)
    engine.runAndWait()

def run_check(val):
    check = val.lower()
    print(">"+check)
    if(("hey" in check and "ada" in check) or ("hello" in check and "ada" in check)):
        talk("Hello Yash")
        engine.runAndWait()
    elif(("turn" in check and "off" in check) or ("exit" in check) or ("escape" in check)):
        talk("Bye")
        exit()
    elif((("what's" in check) or ("what" in check) and "is" in check and "time" in check)):
        talk("It is " + datetime.now().strftime("%H:%M:%S"))
    elif(("open" in check and ("brave" in check) or("browser") in check)):
        talk("Opening browser")
        webbrowser.get('windows-default').open('https://google.com')
    elif(("clear" in check and "terminal" in check)):
        talk("")
        os.system("clear")

    elif(("test" in check)):
        talk("Testing")
        os.system('echo Hello')
    else:
        talk(val + " Didnt Match")

m=sr.Microphone()
r = sr.Recognizer()

def listen():
    while True:
        with m as source:
            audio = r.listen(source)
        try:
            value = r.recognize_google(audio)
            run_check(value)
        except sr.UnknownValueError:
            print("Didnt catch that")
