import sys
import pexpect
import time


def respond_to_hello(speak):
    speak("Hello! How can I assist you today?")


def respond_to_howareyou(speak):
    speak("I'm good, thanks for asking.")


def respond_to_whoareyou(speak):
    speak("I'm your voice assistant!")


def switch_to_text_mode(speak, set_mode):
    set_mode("text")
    speak("Switched to text mode.")


def switch_to_talk_mode(speak, set_mode):
    set_mode("talk")
    speak("Switched to talk mode.")


def respond_to_exit(speak):
    speak("Goodbye!")
    sys.exit()


def ask_ai(speak, listen):
    speak("Starting AI session. Please wait while the AI loads.")
    try:
        # Spawn the interactive process with a pseudo-terminal.
        child = pexpect.spawn("ollama run qwen:0.5b", encoding="utf-8", timeout=30)
    except Exception as e:
        speak("Failed to start AI session: " + str(e))
        return

    # Wait a fixed time for the AI to load.
    time.sleep(20)

    # Optionally, try to read any initial output:
    try:
        child.expect(r".*[>]", timeout=2)
    except pexpect.TIMEOUT:
        pass

    speak("AI session is ready. You can now ask your questions. Type 'quit AI' to end the session.")

    while True:
        question = listen()
        if not question:
            speak("No question provided. Please try again or type 'quit AI' to end the session.")
            continue
        if "quit ai" in question.lower():
            child.sendline("/bye")
            speak("AI session terminated.")
            break

        # Send the question to the AI.
        child.sendline(question)
        time.sleep(5)  # Allow time for the AI to process the question.

        # Collect any available output non-blockingly.
        response = ""
        end_time = time.time() + 10  # Wait up to 10 seconds for output.
        while time.time() < end_time:
            try:
                chunk = child.read_nonblocking(size=1024, timeout=1)
                response += chunk
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break

        if response.strip():
            speak("The AI says: " + response.strip())
        else:
            speak("No response from AI for that question.")

        speak("Do you have another question for the AI? (Type 'quit AI' to end the session.)")
    child.terminate()
