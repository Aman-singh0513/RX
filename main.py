import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from dotenv import load_dotenv
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
import musicLibrary

# Load environment variables
load_dotenv()

newsapi = os.getenv("NEWS_API_KEY")
if newsapi:
    newsapi = newsapi.strip()   # remove any spaces or newlines


def speak(text):
    engine.say(text)
    engine.runAndWait()

# some basic site opening links
def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open insta" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open classroom" in c.lower():
        webbrowser.open("https://classroom.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    # open music from music library
    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "").strip()
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Link not found ")

    # fetch news
    elif "news" in c.lower():
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])[:5]
            if articles:
                for article in articles:
                    title = article.get("title", "No title available")
                    print(title)
                    speak(title)
            else:
                speak("No news articles found.")
        else:
            print("Failed to fetch news:", r.json())
            speak("Sorry, I couldn't fetch the news")

if __name__ == "__main__":
    speak("Intialising Rx")
    speak("what do u want")

    while True:
        # listen for wake word Rx
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print("Listening!!!")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            word = recognizer.recognize_google(audio).lower()
            print("Heard", word)

            if "rx" in word:
                speak("Ya")
                print("Rx Here...")

                # if Rx heard process the command
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    processcommand(command)

        except Exception as e:
            print("Error: ", e)
