import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import requests
import time 


engine = pyttsx3.init()
engine.setProperty('rate', 150)


def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, there was a problem with the service.")
        return ""


def get_weather(city="Delhi"):
    api_key = "9047817ce5b678bbe59d5df936bcc8ce"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        print(data) 

        if data["cod"] != 200:
            speak("Sorry, I couldn't fetch the weather.")
            return

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The weather in {city} is {desc} with a temperature of {temp} degrees Celsius.")
    except Exception as e:
        print("Error:", e)
        speak("Unable to get weather right now.")

def run_assistant():
    command = listen()

    if "hello" in command:
        speak("Hello! How can I help you today?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "day" in command:
        current_day = datetime.datetime.now().strftime("%A")
        speak(f"Today is {current_day}")
    elif "weather in" in command:
        city = command.split("weather in")[-1].strip()
        if city:
            get_weather(city)
        else:
            speak("Please say the city name.")
    elif "weather" in command:
        speak("Which city do you want the weather for?")
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            speak(f"Searching for {query}")
            pywhatkit.search(query)
        else:
            speak("What should I search for?")

    elif "exit" in command or "stop" in command:
        speak("Alright, wrapping up...")
        time.sleep(2)  
        speak("Goodbye! Have a nice day!")
        exit()
    elif command:
        speak("Sorry, I can't do that yet.")


if __name__ == "__main__":
    speak("Voice assistant is now active.")
    while True:
        run_assistant()

