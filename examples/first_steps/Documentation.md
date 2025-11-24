# Documentation

## Öffnen & Weiterarbeiten

Die SD-Karte mit Ubuntu hat das Programm "PyCharm" aus dem default Ubuntu Appstore, worauf sich sämtlicher Code befindet. Dieser besteht aus einem "main File" namens "Script" einem sub File für alle Fähigkeiten nahmens "actions" und einem CSV das spezifiziert welcher "Prompt" für welche Fähigkeit aus "actions" steht.

## Ausgangslage

Das Ziel war ein, den PIB-Roboter zusammen zu bauen und zu programmieren. Er soll ggf. sogar mit KI verbunden werden. Das ganze soll dann als Vorzeigeobjekt für Kunden oder als späteres Lernendenprojekt dienen.

## Erste Schritte

Bevor man mit der Software beginnen kann, muss natürlich der Roboter zusammengebaut werden. Das beginnt schon mit dem 3d-Drucken der Einzelteile. Das hat glücklicherweise Dani für uns übernommen.
Wir kamen also erst beim Zusammenbauen ins Spiel. 

Hierzu gibt es eine seperate Anleitung - ich werde nicht ins Detail gehen. Das Zusammenbauen hat allerdings definitiv Spass gemacht, da man immer wieder auf neue Herausforderungen sötsst und diese als Team lösen kann. 

Dabei hat man sogar etwas wirkliches in den Händen - eine Seltenheit in unserem Beruf. Nach einigen Tagen wurde das ganze jedoch auch etwas eintönig, weshalb ich froh war, mit der Entwicklung der Software starten zu dürfen.

## Software

Nach zahlreichen Versuchen, und einigen Nervenzusammenbrüchen, haben wir sämtlichen Glauben an die PIB Software verloren. Die Plattform hatte definitiv ihre Grenzen, Mikrofon und Kamera funktionierten nur sporadisch. Gleichzeitig war die Low-Code Umgebung nicht ideal.

Nach einigen neu aufgesetzten SD-Karten haben wir uns schliesslich entschieden ein ganz normales Ubuntu, ohne die PIB Software, zu installieren und dort mit Python selbst zu starten.
Das ging wesentlich besser, da man in der IDE PyCharm, die man im Ubuntu AppStore herunterladen kann, wirklich gut arbeiten kann. Gleichzeitig löst diese das Problem der `pip install`s. Diese haben im normalen CMD nicht funktioniert - egal wie sehr wir es probiert haben. PyCharm setzt automatische eine Art virtuelle Maschine auf, auf der alles so funktioniert wie geplant.

So konnte es also losgehen mit der Entwicklung.

### Konzept

Das Ziel war es selber einen Lernenden Sprachassistenten zu konzipieren. Da es fast etwas langweilig gewesen wäre, einfach ChatGPT auf dem PIB laufen zu lassen. Entsprechend war der Ansatz der folgende:

Der PIB bekommt einige Funktionen von uns. Diese werden jeweils in einem CSV mit dem entsprechenden Command festgehalten. Nun soll der PIB bei jedem Command durch das CSV durch-loopen und herausfinden, welcher dort vorhandene Command dem jetztigen Command am nächsten kommt. So hat er praktisch immer eine Antwort bereit. 

Weiss er nun nicht was er tun soll, fragt er nach. Die Antwort auf diese Frage wird nun wieder durch das CSV geloopt etc. etc. bis er herausfindet was er hätte machen sollen. Dann werden alle Erklärungsversuche und der anfängliche Command mit der Aktion, die er hätte machen sollen, im CSV verlinkt. So lernt der PIB.

Das ganze haben wir erreicht, in dem wir mit den `Python Libraries pyttsx3, speechrecognition und csv` geschafft. Diese reichen für Speechrecognition, Text to Speech und eben CSV management.

Von dort an konnten wir also beginnen einige Funktionen hinzuzufügen.

### Tokenisation und Stemming

Um der KI noch etwas näher zu kommen haben wir mit der Library `NLTK` das Handling unsere Commands verbessert. Nun werden sämtliche Commands in Tokens umgewandelt - also meistens in Worte unterteilt - und diese unterlaufen dann das Stemming. Stemming heisst, sie werden in ihre Stammform heruntergebrochen. So können wir Commands effizienter einlesen, bzw. der entsprechenden Aktion zuordnen.

### Mode

Ein weiterer Schritt war der Modus. Nun kann via Command "switch to text/speech mode" der Modus gewechselt werden. Das lässt den input / output von PIB entweder zu Audio oder Text werden. Man kann also nun mit ihm schreiben oder sprechen.

### OLLAMA / AI

Neben einigen standard Funktionen, wie auf "Wie geht es dir?" "Mir geht es gut" antworten, haben wir nun einige komplexere Funktionen hinzugefügt. Diese werden übrigens in einem externen Python File gespeichert und diese wird dann mit "`import fileName`" in unser Main Dokument eingebunden. So haben wir alle Funktionen des "Funktiondokuments" in einem aufgeräumten Maindokument. 

Nach etwas Recherche zum Thema AI sind wir auf OLLAMA gestossen. OLLAMA lässt uns hunderte starke KI LLM Models, wie DeepSeek v3, auf unser Gerät herunterladen. Diese laufen dann lokal und offline im Terminal. Nun kann man PIB sagen, dass man KI verwenden will. Er öffnet dann im Hintergrund ein Terminal und führt den KI-Befehl aus. Dann fragt er die KI den Promt, den man will, und gibt einem den Output zurück.

## Quellen

[Weather Tutorial](https://www.instructables.com/Get-Weather-Data-Using-Python-and-Openweather-API/)
[OpenWeather](https://openweathermap.org)
[ChatGPT](https://chatgpt.com)
[Ollama](https://ollama.com)
[Video Ollama](https://www.youtube.com/watch?v=WxYC9-hBM_g)
[pyttsx3](https://pypi.org/project/pyttsx3/)
[Speechrecognition](https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py)
[Sklearn](https://scikit-learn.org/stable/)
[NLTK](https://www.nltk.org/)
[csv](https://www.geeksforgeeks.org/working-csv-files-python/)
[faicial Recognition](https://github.com/ageitgey/face_recognition)
[face Recognition](https://pypi.org/project/face-recognition/)
[OpenCV](https://pypi.org/project/opencv-python/)
[FaceAlgorythm](https://github.com/kipr/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml)