import speech_recognition as sr
import pyttsx3
import difflib
import csv
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import sys
import actions  # Import the external actions module


# Download necessary NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

# Global mode variable; can be "talk" (voice) or "text" (chat)
mode = "text"

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# File path for the CSV
CSV_FILE = 'examples.csv'

# Initialize PorterStemmer
stemmer = PorterStemmer()


def speak(text):
    global mode
    if mode == "talk":
        tts_engine.say(text)
        tts_engine.runAndWait()
    else:
        print("Bot:", text)


def listen():
    global mode
    if mode == "text":
        return input("You: ").lower()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, the service is down.")
        return None
    except OSError as e:
        if "FLAC conversion utility not available" in str(e):
            speak("FLAC conversion utility not available. Please install it, for example using 'apt-get install flac'.")
            return None
        else:
            raise e


def load_examples():
    examples = {}
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            examples[row['command'].strip().lower()] = row['code'].strip()
    return examples


def save_example(command, code):
    import os
    newline = ""
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', newline='') as file:
            content = file.read()
        if content and not content.endswith("\n"):
            newline = "\n"
    with open(CSV_FILE, mode='a', newline='') as file:
        file.write(newline)
        writer = csv.DictWriter(file, fieldnames=['command', 'code'])
        writer.writerow({'command': command.strip().lower(), 'code': code.strip()})


def preprocess(text):
    tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)


def get_code(command, examples):
    command_stemmed = preprocess(command)
    examples_stemmed = {preprocess(k): v for k, v in examples.items()}
    matching_commands = difflib.get_close_matches(command_stemmed, list(examples_stemmed.keys()), n=1, cutoff=0.6)
    if matching_commands:
        matched_command = matching_commands[0]
        return examples_stemmed[matched_command]
    else:
        return None


def enhanced_handle_unknown_command(examples):
    while True:
        speak("I did not understand that. What should I have done? (Type 'cancel' to cancel)")
        feedback = listen()
        if feedback is None:
            continue
        if feedback.lower() == "cancel":
            return None
        code = get_code(feedback, examples)
        if code is not None:
            return code
        else:
            speak("I still didn't understand your feedback. Please rephrase or type 'cancel'.")


def execute_code(code, original_command=""):
    global mode

    def set_mode(new_mode):
        global mode
        mode = new_mode

    try:
        if code == '1':
            actions.respond_to_hello(speak)
        elif code == '2':
            actions.respond_to_howareyou(speak)
        elif code == '3':
            actions.respond_to_whoareyou(speak)
        elif code == '5':
            actions.switch_to_text_mode(speak, set_mode)
        elif code == '6':
            actions.switch_to_talk_mode(speak, set_mode)
        elif code == '7':
            actions.ask_ai(speak, listen, original_command)
        elif code == '8':
            actions.get_weather(speak, listen, original_command)
        elif code == '9':
            actions.company_info_query(speak, listen, original_command)
        elif code == '10':
            speak(actions.recognize_faces(speak, listen, original_command))
        elif code == '11':
            actions.handle_nothing(speak, original_command)
        elif code == '12':
            actions.register_faces(speak, listen, original_command)
        elif code == '0':
            actions.respond_to_exit(speak)
        else:
            speak("I didn't understand that command.")
    except Exception as e:
        speak(f"An error occurred: {e}")


def main():
    examples = load_examples()
    unresolved_commands = []
    speak("Hello, how can I assist you today?")
    while True:
        command = listen()
        if command:
            code = get_code(command, examples)
            if code:
                if unresolved_commands:
                    for unknown in unresolved_commands:
                        save_example(unknown, code)
                    unresolved_commands = []
                execute_code(code, command)
                if code == '0':
                    break
            else:
                unresolved_commands.append(command)
                new_code = enhanced_handle_unknown_command(examples)
                if new_code is not None:
                    for unknown in unresolved_commands:
                        save_example(unknown, new_code)
                    unresolved_commands = []
                    execute_code(new_code, command)
                    execute_code(new_code, command)
                else:
                    unresolved_commands = []


if __name__ == "__main__":
    main()
