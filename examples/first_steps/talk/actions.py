import sys
from time import process_time_ns

import pexpect
import time
import requests
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from glob import glob
import cv2
import depthai as dai
import re

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


def ask_ai(speak, listen, command_text=""):
    # [Your previously working ask_ai code goes here]
    speak("Starting AI session. Please wait while the AI loads.")
    try:
        child = pexpect.spawn("ollama run qwen:0.5b", encoding="utf-8", timeout=30)
    except Exception as e:
        speak("Failed to start AI session: " + str(e))
        return

    time.sleep(20)
    try:
        child.expect(r".*[>]", timeout=2)
    except pexpect.TIMEOUT:
        pass

    # Check if extra context exists in the command.
    lowered = command_text.lower()
    if "ask the ai" in lowered:
        parts = lowered.split("ask the ai", 1)
        question = parts[1].strip()
    else:
        question = ""
    if not question:
        speak("AI session is ready. What do you want to ask the AI?")
        question = listen()
        if not question:
            speak("No question was provided. Terminating AI session.")
            child.sendline("/bye")
            child.terminate()
            return
    else:
        speak("I understood your question as: " + question)

    child.sendline(question)
    time.sleep(5)
    response = ""
    end_time = time.time() + 10
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
        speak("No response from AI.")
    speak("Do you have another question for the AI? Type 'quit AI' to end the session, or ask your question now.")
    while True:
        next_question = listen()
        if not next_question:
            speak("Please say your question or type 'quit AI' to exit.")
            continue
        if "quit ai" in next_question.lower():
            child.sendline("/bye")
            speak("AI session terminated.")
            break
        child.sendline(next_question)
        time.sleep(5)
        response = ""
        end_time = time.time() + 10
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
        speak("Ask another question or type 'quit AI' to end the session.")
    child.terminate()


def get_weather(speak, listen, command_text=""):
    # Always use Uzwil as the city.
    city = "Uzwil"
    api_key = "7167e0453c92af67f7a6cfd081c47751"  # your API key
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(city, api_key)

    try:
        res = requests.get(url)
        data = res.json()
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        speak("It is " + str(temp) + " degrees Celsius in " + city + ".")
        speak("The wind speed is " + str(wind) + ".")
        speak("The pressure is " + str(pressure) + ".")
        speak("The humidity is " + str(humidity) + ".")
        speak("Overall, the weather is " + description + ".")
    except Exception as e:
        speak("Failed to get weather data: " + str(e))


def company_info_query(speak, listen, command_text=""):
    # This function searches through local company documents.
    docs_folder = "company_docs"  # Folder containing text files about the company
    # Get all .txt files in the folder.
    files = glob(os.path.join(docs_folder, "*.txt"))
    documents = []
    doc_names = []
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(content)
                doc_names.append(os.path.basename(file))
        except Exception as e:
            continue
    if not documents:
        speak("No company documents found in the folder.")
        return

    # Use TF-IDF to vectorize the documents.
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Use the command text as the query. If it’s empty, ask the user.
    query = command_text
    if not query or query.strip() == "":
        speak("What is your company-related question?")
        query = listen()
        if not query:
            speak("No question provided.")
            return

    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix)
    best_index = similarity.argmax()
    best_score = similarity[0, best_index]

    # You can adjust the threshold as needed.
    if best_score < 0.1:
        speak("I couldn't find relevant information about your question.")
    else:
        answer = documents[best_index]
        snippet = answer[:500] + ("..." if len(answer) > 500 else "")
        speak("Here's what I found from our company documents: " + snippet)

# test

def recognize_faces(speak, listen, command_text=""):
    """
    Captures a frame from the Oak-D Light camera using DepthAI,
    detects faces, and then performs simple recognition by comparing
    grayscale histograms with known faces stored in the "known_faces" folder.
    """
    # Load Haar cascade for face detection.
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Load known faces from the folder and compute their histograms.
    known_faces_folder = os.path.join(os.getcwd(), "known_faces")
    if not os.path.isdir(known_faces_folder):
        speak("The known faces folder does not exist.")
        return

    # Load known face images and compute histograms.
    known_histograms = {}
    for image_path in glob(os.path.join(known_faces_folder, "*.*")):
        img = cv2.imread(image_path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            continue
        # Assume the first detected face is the person.
        (x, y, w, h) = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        cv2.normalize(hist, hist)
        # Instead of using the entire filename, extract the name before any underscore.
        full_name = os.path.splitext(os.path.basename(image_path))[0]
        name = full_name.split('_')[0]
        known_histograms[name] = hist


    if not known_histograms:
        speak("No known faces were found in the folder.")
        return

    # Create a DepthAI pipeline to capture a frame from the Oak-D Light camera.
    pipeline = dai.Pipeline()
    camRgb = pipeline.create(dai.node.ColorCamera)
    camRgb.setPreviewSize(640, 480)  # Adjust as needed
    camRgb.setInterleaved(False)
    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("rgb")
    camRgb.preview.link(xoutRgb.input)

    # Connect to the Oak-D device and capture a frame.
    try:
        with dai.Device(pipeline) as device:
            qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=True)
            frame = qRgb.get().getCvFrame()
    except Exception as e:
        speak("Error accessing the Oak-D camera: " + str(e))
        return

    if frame is None:
        speak("I couldn't capture a frame from the camera.")
        return

    # Convert the captured frame to grayscale.
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        speak("I didn't detect any faces in the frame.")
        return

    for (x, y, w, h) in faces:
        face_roi = gray_frame[y:y + h, x:x + w]
        hist_roi = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        cv2.normalize(hist_roi, hist_roi)
        best_name = "Unknown"
        best_score = 0
        # Compare this face's histogram with each known face using correlation.
        for name, known_hist in known_histograms.items():
            score = cv2.compareHist(known_hist, hist_roi, cv2.HISTCMP_CORREL)
            if score > best_score:
                best_score = score
                best_name = name
        # If the best match score is below a threshold, mark as Unknown.
        if best_score < 0.1:
            best_name = "Unknown"
        best_score_string = str(best_score)
        return("I see " + best_name + "." + " With a score of " + best_score_string)

def register_faces(speak, listen, command_text=""):
    name = ""
    match = re.search(r"as\s+(\w+)", command_text.lower())
    if match:
        name = match.group(1)

    # If no name was extracted, ask the user.
    if not name:
        speak("Can you repeat the name for me?")
        name = listen()
        if not name:
            speak("No name provided. Cancelling registration.")
            return
        name = name.strip().lower()

    # Ensure the known_faces folder exists.
    known_faces_folder = os.path.join(os.getcwd(), "known_faces")
    if not os.path.exists(known_faces_folder):
        os.makedirs(known_faces_folder)

    speak("I am now capturing your face. Please look at the camera.")

    # Create a DepthAI pipeline to capture a single frame from the Oak-D.
    pipeline = dai.Pipeline()
    camRgb = pipeline.create(dai.node.ColorCamera)
    camRgb.setPreviewSize(640, 480)
    camRgb.setInterleaved(False)
    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("rgb")
    camRgb.preview.link(xoutRgb.input)

    try:
        with dai.Device(pipeline) as device:
            qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=True)
            frame = qRgb.get().getCvFrame()
    except Exception as e:
        speak("Error capturing image from the Oak-D camera: " + str(e))
        return

    # Use OpenCV to detect the face.
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        speak("No face was detected. Please try again.")
        return

    # Use the first detected face.
    (x, y, w, h) = faces[0]
    face_roi = frame[y:y + h, x:x + w]

    # Save the face image as name.png in the known_faces folder.
    base_name = name
    save_path = os.path.join(known_faces_folder, base_name + ".png")
    counter = 1
    while os.path.exists(save_path):
        save_path = os.path.join(known_faces_folder, f"{base_name}_{counter}.png")
        counter += 1
    success = cv2.imwrite(save_path, face_roi)
    if success:
        speak("I saved the face as " + os.path.basename(save_path))
    else:
        speak("I encountered an error while saving the face.")


def handle_nothing(speak, original_command):
    if "okey" in original_command:
        speak("No Problem!")
    elif "thank you" in original_command:
        speak("You're welcome!")
    elif "no thanks" in original_command:
        speak("Alright, you're welcome!")
    else:
        speak("Is there another thing I can help you with?")
