import speech_recognition as sr
import time
from datetime import datetime
import webbrowser
import os
import requests
import json
import pyttsx3
from dotenv import dotenv_values

va_name = "ava"

envConfig = dotenv_values()
weatherURL = "https://api.openweathermap.org/data/2.5/weather?lat=38.951883&lon=-92.3337366&appid=" + \
    envConfig["TEST"]
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)

m = sr.Microphone()
r = sr.Recognizer()
is_triggered = False


def talk(val):
    engine.say(val)
    engine.runAndWait()


def isQuestion(val):
    if ("what" in val or "when" in val or "how" in val or "where" in val or "which" in val or "who" in val):
        return (True)
    else:
        return (False)


def fetchAnswer(val):
    print(val)
    url = "http://api.wolframalpha.com/v1/spoken?appid="+envConfig["WOLFRAM"]+"&i=" + \
        val+"%3f&units=metric"
    res = requests.get(url)
    if (res.status_code == 200):
        return (res.text)


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
    print("run_check > "+check)
    if ((checkValid("hey", check) and va_name in check) or ("hello" in check and va_name in check)):
        talk("Hello Yash")
        engine.runAndWait()
    elif (("how" in check and "are" in check and "you" in check)):
        talk("I am good!")
    elif (("turn" in check and "off" in check) or ("exit" in check) or ("escape" in check)):
        talk("Good Night Sir")
        exit()
    elif (((("what's" in check) or ("what" in check)) and "time" in check)):
        talk("It is " + datetime.now().strftime("%H:%M:%S"))
    elif (("open" in check and ("brave" in check) or ("browser") in check)):
        talk("Opening browser")
        webbrowser.get('windows-default').open('https://google.com')
    elif (("weather" in check and ("what" in check or "what's" in check))):
        data = getWeather()
        tempVal = checkNegative(ktoc(data["main"]["temp"]))
        temp = str(round(ktoc(data["main"]["temp"])))
        feel = str(round(data["main"]["feels_like"]-273.15))
        city = str(data["name"])
        sky = ""
        if (data["clouds"]["all"] < 50):
            sky = "very little clouds"
        else:
            sky = "very many clouds"
        talk("The temperature is " + tempVal + temp + "degree celcius but it feels like " +
             feel + ". It seems today in"+city+", there will be " + sky)
    elif ("what" in check and "temperature" in check):
        data = getWeather()
        talk("The temperature is " + checkNegative(ktoc(data["main"]["temp"])) + str(round(ktoc(
            data["main"]["temp"]))) + "degree celcius but it feels like " + str(round(data["main"]["feels_like"]-273.15)))
    elif (("test" in check)):
        talk("Testing")
        os.system('echo Hello')
    elif (("led" in check or "LED" in check) and ("toggle" in check)):
        res = requests.get("http://192.168.1.207/led")
        if (res.status_code == 200):
            talk("Done")
        else:
            talk("There was a problem")
    elif ("led" in check and "on" in check):
        res = requests.get("http://192.168.1.207/ledon")
        if (res.status_code == 200):
            talk("Done")
        else:
            talk("There was a problem")
    elif ("led" in check and "off" in check):
        res = requests.get("http://192.168.1.207/ledoff")
        if (res.status_code == 200):
            talk("Done")
        else:
            talk("There was a problem")
    elif (isQuestion(check)):
        output = fetchAnswer(check.replace(" ", "+"))
        talk(output)
    else:
        talk(check + " Didnt Match")


def trigger():
    global is_triggered
    with m as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        value = r.recognize_google(audio).lower()
        print("Trigger>Try>"+value)
        if (is_triggered == False):
            if ("hey"+va_name in value or va_name in value):
                talk("yes?")
                is_triggered = True
                print("Trigger>try>set trigge to " + str(is_triggered))
        else:
            run_check(value)
            is_triggered = False
    except sr.UnknownValueError:
        print("Didnt catch that")

def main():
    while True:
        trigger()

main()