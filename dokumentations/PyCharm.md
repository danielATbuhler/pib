# PyCharm

- [PyCharm](#pycharm)
  - [Virtuelle Umgeungen](#virtuelle-umgeungen)
  - [Programmieren](#programmieren)
  - [packages installation](#packages-installation)
  - [Truble Shooting](#truble-shooting)
    - [Interpreter error](#interpreter-error)

PyCharm ist eine sehr schlanke aber doch brauchbare IDE. Es empfielt sich, die Dateien einfach rein zu ziehen, anstelle einen Projektordner zu öffnetn, da dies **sehr** lange dauern kann.

## Virtuelle Umgeungen

Es können relativ einfach mithilfe von PyCharm virtuelle Umgebungen gemacht werden. Diese können dann auch geöffnet werden:

- Oben rechts auf das Zahnrad
- Dann Settings
- Interpreter -> Add Interpreter
- Ich empfehle immer Generate new, auch wenn bereits einer existiert
- Entweder Pfad zur existierenden venv[^1] oder ansonsten Pfad, wo die venv hin soll.
- Falls eine existierende venv angegeben erscheint: *Select existing interpreter* -> auswählen
- Bei beiden wegen nun OK

**Es ist wichtig zu beachten, dass bei der erstellung die richtige Python version genommen wird. Z.B hat Python 3.11 und 3.12 mehr packages als 3.13.**

## Programmieren

Es kann in PyCharm ähnlich wie in VS Code programmiert werden. Oben rechts befindet sich ein *run* symbol, mitwelchem der Code dann ausgeführt werden kann.

Für den Anfang kann mit meiner [Piblib](./Piblib.md) programmiert werden. Wichtig ist dort die `startup()` und `shutdown()` funktion. Verwende diese **immer**. Um mehr über Pib Syntax herauszufinden, kannst du auch in die Bibliotheke reinschauen, und ein verständniss aufbauen.

## packages installation

Um Packete zu installiern, öffne Bash und wechsle in dei env:

```bash
cd env/bin
source ./activate
```

anschliessend haben die meisten packages eines der folgenden pattern:

```bash
python -m pip install [packagename]
```

oder

```bash
sudo apt install python3-[packagename]
```

Wobei jeweils `[packagename]` durch den Paketnamen ersetzt wird.

**Es gibt nicht jedes Package auf jeder Python version!**

## Truble Shooting

### Interpreter error

Sollte der Interpreter der venv nicht starten oder sogar nicht hinzufügbar sein, dann ist es wahrscheinlich ein Problem mit den Rechten. Schau, dass der ganze venv ordner ausführbar ist.

<!--## Fussnoten-->

[^1]: ./Fussnoten/venv[^1].md
