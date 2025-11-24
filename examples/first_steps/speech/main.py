import speech_recognition as sr
import pyttsx3
import difflib
import csv
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import sys

# Download necessary NLTK data
nltk.download('punkt')

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# File path for the CSV
CSV_FILE = 'examples.csv'

# Initialize PorterStemmer
stemmer = PorterStemmer()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
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

def load_examples():
    examples = {}
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            examples[row['command'].strip().lower()] = row['code'].strip()
    return examples

def save_example(command, code):
    with open(CSV_FILE, mode='a', newline='') as file:
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

def handle_unknown_command(command):
    speak("I did not understand that. What should I have done?")
    code = listen()
    
    if code:
        save_example(command, code)
        speak("Thank you! I'll remember that.")
        return code
    else:
        speak("Failed to save the new command.")
        return None


def respond_to_hello():
    speak("Hello! How can I assist you today?")

def respond_to_howareyou():

    speak("I'm good, thank's for asking.")

def respond_to_whoareyou():
    speak("I'm your voice assistant!")
    
def respond_to_exit():
    speak("Goodbye!")
    sys.exit()
    
def execute_code(code):
    try:
        if code == '1':
            respond_to_hello()
        elif code == '2':
            respond_to_howareyou()
        elif code == '3':
            respond_to_whoareyou()
        else:
            speak("I didn't understand that command.")
    except Exception as e:
        speak(f"An error occurred: {e}")

def main():
    examples = load_examples()
    speak("Hello, how can I assist you today?")
    
    while True:
        command = listen()
        
        if command:
            code = get_code(command, examples)
            
            if code:
                execute_code(code)
                if code == '4':  
                    break
            else:
                code = handle_unknown_command(command)
                if code:
                    execute_code(code)
                    examples = load_examples()

if __name__ == "__main__":
    main()
