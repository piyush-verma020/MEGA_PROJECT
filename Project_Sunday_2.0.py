# Importing the required libraries
import speech_recognition as sr  # For speech recognition
import webbrowser  # To open URLs in the default web browser
import pyttsx3  # For text-to-speech conversion
import time  # For adding delays
import pywhatkit as kit
import openai
import datetime

# Initialize the recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Define a class to store and manage the search query
class Search:
    def __init__(self):
        self.query = ""

    # Getter for query
    @property
    def word(self):
        return self.query

    # Setter for query
    @word.setter
    def word(self, value):
        self.query = value


def ask_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Sunday, an AI assistant. When user speaks, if the command is to play YouTube, open websites, or answer, guide the action. Format: Action: [action here]."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def perform_action(gpt_response):
    if "play" in gpt_response.lower():
        # Example: Action: play [song name]
        video_name = gpt_response.split("play",1)[1].strip()
        speak(f"Playing {video_name} on YouTube.")
        kit.playonyt(video_name)

    elif "open" in gpt_response.lower():
        # Example: Action: open [website name]
        site = gpt_response.split("open",1)[1].strip()
        url = f"https://{site}.com"
        speak(f"Opening {site}.")
        webbrowser.open(url)

    elif "time" in gpt_response.lower():
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}.")

    else:
        # Otherwise, just speak the answer
        speak(gpt_response)



# Function to convert text to speech
def speak(text):
    engine.setProperty('rate', 130)  # Set speed of speech
    engine.setProperty('volume', 1.0)  # Set volume
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Select a voice (change index if needed)
    engine.say(text)
    engine.runAndWait()

# Function to process voice commands
def processCommand(c):
    c = c.lower()

    # If the command was to open Google
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
                speak("An Error occurred. Please try again later.")
                print(f"Error during Google search: {e}")
                break

    # For openning LinkedIn
    elif "open linkedin" in c:
        speak("Opening Linkedin")
        webbrowser.open("https://linkedin.com")

    # For openning weather forecast
    elif "today's weather" in c:
        speak("Opening 7 Day Weather Forecast on Google")
        webbrowser.open("https://www.google.com/search?q=today%27s+weather+forecast")

    # For openning ChatGPT
    elif "use gpt" in c:
        speak("Using Chatgpt")
        while True:
            try:
                audio = listen_for_command()
                print("Recognizing...")
                user_command = recognizer.recognize_google(audio)
                print(f"You said: {user_command}")

                gpt_response = ask_chatgpt(user_command)
                print(f"GPT Response: {gpt_response}")

                perform_action(gpt_response)

            except sr.UnknownValueError:
                speak("Sorry, I could not understand.")
            except sr.RequestError:
                speak("Sorry, network error.")
            except Exception as e:
                speak("An error occurred.")
                print(f"Error: {e}")
                break

    # If the command was to open YouTube
    elif "open youtube" in c:
        while True:
            try:
                speak("What do you wish to play on YouTube?")
                audio = listen_for_command()
                print("Recognizing...")
                word = recognizer.recognize_google(audio)
                speak(f"Playing {word} on YouTube")
                kit.playonyt(word)  # <-- this will automatically play the first video
                break
            except sr.UnknownValueError:
                speak("Sorry, I could not understand your speech.")
            except sr.RequestError:
                speak("Sorry, my speech service is temporarily unavailable.")
            except Exception as e:
                speak("An error occurred. Please try again later.")
                print(f"Error during YouTube play: {e}")
                break

    # For openning Facebook
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    # For openning Instagram
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")

    # Handling unrecognized command
    else:
        speak("Sorry, I didn't understand. Try again.")

# Function to listen for a command using the microphone
def listen_for_command():
    with sr.Microphone() as source:
        print("Sunday is listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust to ambient noise
        audio = recognizer.listen(source)  # Capture audio input
    return audio

# Main program loop
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

                # If activation word "sunday" is detected
                if "sunday" in word.lower():
                    speak("Yes, how can I help you?")
                    command_audio = listen_for_command()
                    command = recognizer.recognize_google(command_audio)
                    print(f"Command: {command}")
                    processCommand(command)

                # Stop the assistant if "break" is spoken
                elif "break" in word.lower():
                    break

                is_listening = False

        # Handling unknown voice input
        except sr.UnknownValueError:
            print("Couldn't understand the audio.")
            continue

        # Handling issues with the recognition service
        except sr.RequestError as e:
            speak("Speech service is temporarily down. Retrying...")
            print(f"Speech service error: {e}")
            time.sleep(3)
            continue

        # General exception handler
        except Exception as e:
            print(f"Error: {e}")
            print("If you wish me to stop then say break")
            continue

        time.sleep(1)  # Brief pause before next listen loop starts
