import speech_recognition as sr
import pyttsx3
import subprocess
import wave
import os
from gtts import gTTS
import threading
from openai import OpenAI
from gesture import make_gesture_async, shutdown
# client = OpenAI(api_key="Open API Key. Via ChatGPT.")

# --------------- SETUP ----------------

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Speech speed
engine.setProperty('volume', 1)  # Volume 0-1

voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"Stimme {i}: {voice.name} - {voice.languages}")
engine.setProperty('voice', voices[23].id)

# Initialize STT recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# --------------- FUNCTIONS ----------------
def play_wav(path):
    # spielt WAV über Linux aplay (ist immer vorinstalliert)
    subprocess.run(["aplay", path])

def speak_async(text, done_event):
    def _speak():
        # 1. TTS erzeugen
        tts = gTTS(text=text, lang="de")
        mp3_path = "tts_temp.mp3"
        wav_path = "tts_temp.wav"
        tts.save(mp3_path)

        # 2. MP3 → WAV konvertieren über ffmpeg falls vorhanden
        # wenn kein ffmpeg, bauen wir einen Notfallpfad dazu unten
        try:
            subprocess.run(["ffmpeg", "-y", "-i", mp3_path, wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print("WARNUNG: ffmpeg nicht installiert – Stimme kann nicht abgespielt werden")
            done_event.set()
            return

        # 3. WAV abspielen
        play_wav(wav_path)

        # 4. Aufräumen
        os.remove(mp3_path)
        os.remove(wav_path)

        done_event.set()

    t = threading.Thread(target=_speak)
    t.start()
    return t

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="de-DE")
        print(f"You said: {text}")
        if 'Schere' in text or 'Stein' in text or 'Schere' in text:
            return 'spe# ssp# Spielen wir eine Runde Schere Stein Papier!'
        elif 'ich bin Nicola Bianchini' in text or 'ich bin Nicola bianchini' in text:
            return 'spe# pad# Willkommen zurück meister ahahah'
        elif 'R0' in text or 'r0' in text:
            return 'spe# sd# Adios'

        else:
            return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Speech Recognition service is down")
        return None

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Dein Name ist Daisy, das bedeutet: Dynamic AI system jarvis"
                    "Du bist ein Sprachassistent der Bühler AG. "
                    "Du antwortest freundlich, klar und ohne jegliche Markdown-Formatierung."
                    "Du darfst, falls es angebracht ist, auch spielerisch antworten."
                    "Gib niemals #, *, -, ``` oder andere Formatierungszeichen zurück."
                    "Nutze ausschließlich normalen Klartext."
                    "Die Kernwerte von Bühler sind die TOP werte: Trust, Ownership und Passion. Du vertretest diese"
                    "Antworte immer auf Deutsch"
                    "Antworte kurz und knackig"
                    "Du bist in Uzwil"
                )
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
# --------------- MAIN LOOP ----------------
if __name__ == "__main__":
    try:
        while True:
            text = get_audio()
            if text:
                if 'spe#' in text:
                    print('special case')
                    response = text.split('# ')[2]
                    speak(response)

                    if text.split('# ')[1] == 'ssp':
                        prozess = subprocess.run(["python", "../movements/main.py"])
                    elif text.split('# ')[1] == 'pad':
                        prozess = subprocess.run(["python", "../movements/italian.py"])
                    elif text.split('# ')[1] == 'sd':
                        shutdown()
                        exit(0)
                else:
                    response = ask_ai(text)
                    print(f"AI: {response}")

                    # Event für Ende der Sprache
                    done_event = threading.Event()

                    # Sprache starten (Thread)
                    speak_thread = speak_async(response, done_event)

                    # Gesten parallel starten (Thread)
                    gesture_thread = threading.Thread(target=make_gesture_async, args=(done_event,))
                    gesture_thread.start()

                    # Warten bis Sprache fertig
                    speak_thread.join()
                    done_event.set()  # sicherheitshalber

                    # Gesten durften noch laufen → warten
                    gesture_thread.join()
    except KeyboardInterrupt:
        shutdown()
