import speech_recognition as sr
import time
from datetime import datetime
import webbrowser
import os
import requests
import json
import pyttsx3
from dotenv import dotenv_values
envConfig = dotenv_values()
weatherURL = "https://api.openweathermap.org/data/2.5/weather?lat=38.951883&lon=-92.3337366&appid=" + \
    envConfig["TEST"]
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)


def talk(val):
    engine.say(val)
    engine.runAndWait()


def getWeather():
    res = requests.get(weatherURL)
    if (res.status_code == 200):
        data = res.json()
        return (data)


def checkValid(val, test):
    if (val in test):
        return (True)
    else:
        return (False)


def checkNegative(val):
    if (val < 0):
        return ("negative")
    else:
        return ("")


def ktoc(val):
    return (val-273.15)


def run_check(val):
    check = val.lower()
    print(">"+check)
    if ((checkValid("hey", check) and "ada" in check) or ("hello" in check and "ada" in check)):
        talk("Hello Yash")
        engine.runAndWait()
    elif (("how" in check and "are" in check and "you" in check)):
        talk("I am good!")
    elif (("turn" in check and "off" in check) or ("exit" in check) or ("escape" in check)):
        talk("Bye")
        exit()
    elif (((("what's" in check) or ("what" in check)) and "is" in check and "time" in check)):
        talk("It is " + datetime.now().strftime("%H:%M:%S"))
    elif (("open" in check and ("brave" in check) or ("browser") in check)):
        talk("Opening browser")
        webbrowser.get('windows-default').open('https://google.com')
    elif (("weather" in check and ("what" in check or "what's" in check))):
        data = getWeather()
        talk("The temperature is " + checkNegative(ktoc(data["main"]["temp"])) + str(round(ktoc(
            data["main"]["temp"]))) + "degree celcius but it feels like " + str(round(data["main"]["feels_like"]-273.15)))
    elif (("test" in check)):
        talk("Testing")
        os.system('echo Hello')
    else:
        talk(val + " Didnt Match")


m = sr.Microphone()
r = sr.Recognizer()


def listen():
    with m as source:
        audio = r.listen(source)
    try:
        value = r.recognize_google(audio)
        run_check(value)
    except sr.UnknownValueError:
        print("Didnt catch that")


def main():
    while True:
        listen()

main()