# Importing the required libraries
import speech_recognition as sr  # For speech recognition
import webbrowser  # To open URLs in the default web browser
import pyttsx3  # For text-to-speech conversion
import time  # For adding delays
import requests  # For making HTTP requests (e.g., fetching news)
import openai

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsApi = "Your_Api_Key"  # Your NewsAPI key

# Class to store and manage the search query
class Search:
    def __init__(self):
        self.query = ""

    @property
    def word(self):  # Getter for query
        return self.query

    @word.setter
    def word(self, value):  # Setter for query
        self.query = value

def openai_process(command):
    client = openai.OpenAI(api_key="Your_Api_Key")  # Replace with your actual key

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "You are a virtual assistant named Sunday"},
            {"role": "user", "content": command}
        ]
    )
    return response.choices[0].message.conten

# Function to convert text to speech
def speak(text):
    engine.setProperty('rate', 130)  # Set speech rate
    engine.setProperty('volume', 1.0)  # Set volume to max
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Use female voice (index may vary)
    engine.say(text)
    engine.runAndWait()

# Print the assistant's reply
# Function to handle user voice commands
def processCommand(c):
    c = c.lower()  # Convert command to lowercase for comparison

    # Google search functionality
    if "open google" in c:
        while True:
            try:
                speak("What do you wish to search on Google?")
                audio = listen_for_command()
                print("Recognizing...")
                s = Search()
                s.word = recognizer.recognize_google(audio)
                speak(f"Searching {s.word} on Google")
                search_url = "https://www.google.com/search?q=" + s.word.replace(" ", "+")
                webbrowser.open(search_url)
                break
            except sr.UnknownValueError:
                speak("Sorry, I could not understand your speech.")
            except sr.RequestError:
                speak("Sorry, my speech service is temporarily unavailable.")
            except Exception as e:
                speak("An error occurred. Please try again later.")
                print(f"Error during Google search: {e}")
                break

    # Open LinkedIn
    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    # Open weather forecast
    elif "today's weather" in c:
        speak("Opening 7 Day Weather Forecast on Google")
        webbrowser.open("https://www.google.com/search?q=today%27s+weather+forecast")

    # Fetch and read news headlines
    elif "news" in c:
        speak("Reading out the top 10 headlines")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=india&apiKey={newsApi}")
        data = r.json()

        articles = data.get("articles", [])
        for i, article in enumerate(articles[:10], 1):  # Read top 10 headlines
            title = article.get('title')
            if title:
                speak(f"Headline {i}: {title}")
        
        speak("Okay, not reading the headlines.")

    # Open ChatGPT
    elif "open chatgpt" in c:
        speak("Opening ChatGPT")
        webbrowser.open("https://chatgpt.com")

    # YouTube search functionality
    elif "open youtube" in c:
        while True:
            try:
                speak("What do you wish to search on YouTube?")
                audio = listen_for_command()
                print("Recognizing...")
                word = recognizer.recognize_google(audio)
                speak(f"Searching {word} on YouTube")
                search = "https://www.youtube.com/results?search_query=" + word.replace(" ", "+")
                webbrowser.open(search)
                break
            except sr.UnknownValueError:
                speak("Sorry, I could not understand your speech.")
            except sr.RequestError:
                speak("Sorry, my speech service is temporarily unavailable.")
            except Exception as e:
                speak("An error occurred. Please try again later.")
                print(f"Error during YouTube search: {e}")
                break

    # Open Facebook
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    # Open Instagram
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")

    # Fallback for unrecognized command
    else:
        output = openai_process(c)
        speak(output)

# Function to capture voice input from the user
def listen_for_command():
    with sr.Microphone() as source:
        print("Sunday is listening...")
        recognizer.adjust_for_ambient_noise(source)  # Calibrate for background noise
        audio = recognizer.listen(source, timeout=7, phrase_time_limit=7)  # Listen with limits
    return audio

# Main loop for the voice assistant
if __name__ == "__main__":
    speak("BOOTING UP SUNDAY......")
    is_listening = False

    while True:
        try:
            if not is_listening:
                is_listening = True
                audio = listen_for_command()
                word = recognizer.recognize_google(audio)
                print(f"Sunday heard you say: {word}")

                # If wake word "sunday" is detected
                if "sunday" in word.lower():
                    speak("Yes, how can I help you?")
                    speak("If you wish me to stop then say break")
                    command_audio = listen_for_command()
                    command = recognizer.recognize_google(command_audio)
                    print(f"Command: {command}")
                    processCommand(command)

                # Exit command
                elif "break" in word.lower():
                    break

                is_listening = False

        # Couldn't understand the input
        except sr.UnknownValueError:
            print("Couldn't understand the audio.")
            continue

        # Recognition service error
        except sr.RequestError as e:
            speak("Speech service is temporarily down. Retrying...")
            print(f"Speech service error: {e}")
            time.sleep(3)
            continue

        # General error handling
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)  # Short delay before next iteration
