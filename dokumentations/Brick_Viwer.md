# Brick Viwer

- [Brick Viwer](#brick-viwer)

Der Brick Viwer ist ein Tool, mitwelchem ganz einfach die Servo bewegt werden können.

**Wichtig:** Brickviwer funktioniert erst, sobald das folgende Modul installiert wird: [BrickD und BrickV](https://www.tinkerforge.com/de/doc/Embedded/Raspberry_Pi.html)

Sobald auf connect gelickt wird, öffnen sich mehrer 'Fenster'. Die wichtigsten sind die, bei welchen *Servo Bricklet 2.0 steht*. Bei diesen steht jeweils, sobald sie geöffnet sind, die Bricklet ID und darunter, welcher Servo ausgewählt ist. Die beiden Zahlen direkt darunter, Pulse Width min/max, (wahrscheinlich 1000 und 2000), sind wie weit sich der Servo bewegen kann. Bitte nur so weit einstellen, wie es maximal/minimal sein darf (siehe [Servo Conf](../conf/servo_conf.json)). Von den 5 Reglern ist der erste der Wichtigste: Mit ihm kann der Servo dann effektiv bewegt werden, indem man diesen runter bzw. rauf bewegt.

Damit dieser jedoch was macht, muss neben dem Dropdown für die Servo auswahl *enabel* aktiviert werden (Checkbox). **Achtung: Vorsicht er kann nun ausschlagen** (*"Ich kann aus erfahrung sagen, dass dies unangenehm ist"* ~ Nicola Bianchini)

Nun kann mit dem Regeler der Servo live gesteuert werden.
