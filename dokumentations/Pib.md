# Pib

- [Pib](#pib)
  - [Basic Servo](#basic-servo)
  - [Brick Viewer](#brick-viewer)
  - [PyCharm](#pycharm)
    - [Einrichten](#einrichten)
    - [Syntax](#syntax)
  - [Speech to text, AI, text to speach](#speech-to-text-ai-text-to-speach)
  - [Truble Shooting](#truble-shooting)
    - [Servo reagiert nicht](#servo-reagiert-nicht)
    - [Pib stürtzt ab nach bewegung](#pib-stürtzt-ab-nach-bewegung)
    - [Gelenk ist leicht verschoben](#gelenk-ist-leicht-verschoben)

Der Pib Roboter ist ein über 3 Bricklet gesteuerter Roboter. Er kann aufgrund der vielen Servos[^2] vieles machen, jedoch hat er wenig Sicherheitsvorkehrungen. (Ja er kann dich schlagen und ja er kann sich selbst einen Finger ausrenken). Es ist wichtig, beim einschalten der Servos eine gewisse distanz zu ihm zu haben. Dazu sollte die Servos sich nicht zu schnell bewegen und auch nich überdehnbar sein.

## Basic Servo

Die Servos sind in 3 haupt Servos aufgeteilt:

| bricklet     | Id   | Funktion           |
| ------------ | ---- | ------------------ |
| `bricklet_1` | 2b7m | Rechter Arm        |
| `bricklet_2` | 2b7W | Schultern und Kopf |
| `bricklet_3` | 2b83 | Linker Arm         |

Bei den beiden Ärm sind die pins dann volgendermassen:

| Pin | Gelenk            |
| --- | ----------------- |
| 0   | Daumen opposition |
| 1   | Daumen Strecken   |
| 2   | Zeigefinger       |
| 3   | Mittelfinger      |
| 4   | Ringfinger        |
| 5   | kleiner Finger    |
| 6   | Handgelenk        |
| 7   | Unterarm rotieren |
| 8   | Ellbogen          |
| 9   | Oberarm rotieren  |

Und bei dem `bricklet_2` so:

| Pin | Gelenk                     |
| --- | -------------------------- |
| 0   | Linke Schulter horizontal  |
| 1   | Linke Schulter vertikal    |
| 2   | -                          |
| 3   | -                          |
| 4   | Kopf drehen                |
| 5   | Kopf nicken                |
| 6   | -                          |
| 7   | -                          |
| 8   | Rechte Schulter horizontal |
| 9   | Rechte Schulter vertikal   |

Genäuere angaben in dieser [Datei](../conf/servo_conf.json).

## Brick Viewer

Es empfielt sich, zuerst im [Brick Viewer](./Brick_Viwer.md) die Funktion der einzelnen Servo an zusehen.

## PyCharm

In PyCharm kann nun mithilfe von pib Syntax und Python der Roboter programmiert werden.

### Einrichten

Erstelle am Anfang eine venv. Siehe [PyCharm](/PyCharm.md/#virtuelle-umgeungen).

Erstelle eine neu Datei (z.B. test.py) in `venv/bin/` und importiere dort die folgenden libs:

```py
from tinkergrog.ip_connection import IPConnection
from tinkerfrog.bricklet_servo_v2 import BrickletServoV2
```

### Syntax

Hier wäre beispielsweise ein kleines Skript

```py
#import time for pause
import time

from tinkergrog.ip_connection import IPConnection
from tinkerfrog.bricklet_servo_v2 import BrickletServoV2

#IP Connection
ipcon = IPConnection()

#Servo as variable
servoLeftHand = BrickletServoV2(2b83, ipcon)

#Connect to pi b
ipcon.connect('localhost',4223)

#Set Servo pulse width
#servoLeftHand.set_pulse_Width(pin,min,max)
servoLeftHand.set_pulse_Width(0,1000,2000)

#Enable Servo
#servoLeftHand.set_enable(pin,True/False)
servoLeftHand.set_enable(0,True)

#Move servo
#servoLeftHand.set_position(pin,position)
#The position is a value between -9000 and 9000
#It has also no context to the pulse width
servoLeftHand.set_position(0,5000)

#Sleep is very important, otherwise the commands aren't made smoothly
time.sleep(3)

#Move back
servoLeftHand.set_position(0,-5000)

#Disable Servo
#Same syntax as enable
servoLeftHand.set_enable(0,False)
```

## Speech to text, AI, text to speach

Es ist möglich, dass er mit hilfe von einigen Modulen mit einem Reden kann, auch mit einer AI. Für das speech to text verwende `speech_recognition`:

```py
import speech_recognition as sr

recognizer = sr.Recognizer()
mircrophone = sr.Microphone()
```

Für das Text to Speech benutze `pyttsx3`:

```py
import pyttsx3

enegine = pyttsx3.init()
enegine.setProperty('rate', 150) #speech speed
enegine.setProperty('volume', 1) #colume 0-1
```

Jedoch ist `gtts` eine bessere lösung, da diese eine angenehmere Stimme hat, welche weniger mechanisch klingt.

Für die AI empfielt es sich, eine API von OpenAI zu benutzen. Dafür benötigst du einen Account. Du findest im internet genügend Anleitunge, wie du diese API bekommst.

Um ein kleines Beispiel zu sehen, siehe auf dem pib unter Erste_Tests

## Truble Shooting

### Servo reagiert nicht

Es kann durchaus vorkommen, dass ein Faden sich 'ausfädelt'. Dazu dann einfach den Pib roboter öffnen und anschliessend herausfinden, welcher servo zu dem Gelenk gehört, welches sich nicht mehr bewegt. Dazu am besten den Servo aktivieren über Brick Viewer und den Regler rauf und runter bewegen. anschliessend wieder die Schnur auf den Servo aufwickeln

### Pib stürtzt ab nach bewegung

Pib kann teilweise nach gewissen Bewegungen abstürtzen. Dann:

- Strom abschalten
- Gelenke in entspannte Position
- Mit sicherheitsabstand Strom wieder einschalten

Das Problem liegt meistens beim Strom: Servos jeweils mit einem Timeout/Sleep dazwischen starten. -> `Piblib.startup()`

### Gelenk ist leicht verschoben

Dies passiert häufig, wenn die Schnur länger wird, in den Finger. Dafür dann einfach bei den Servo hinten die Schnur wieder anziehen (Der Servo kann gedreht werden, es klickt dann so).

[^2]:./Fussnoten/servo.md
