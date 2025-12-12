# Piblib

## Implementierung

Mach den Piblib ordner in die gleiche ebene, wie die Datei ist, welche auf diesen zugreiffen soll. Anschliessend kannst du diese folgendermassen verwenden:

```py
import piblib.movements as piblib
import piblib.gesture as piblibGesture
piblib.startup()
piblibGesture.shakeHand()
piblib.shutdown()
```

Was hinter dem `as` ist spielt keine Rolle, da dies dann einfach der Alias ist

## Funktionen

**Die Wichtigsten Funktionen sind `startup()` und `shutdown()` du solltest diese immer am Anfang bzw. am Ende deines Skriptes verwenden.**

`amount` ist immer ein Wert zwischen `-9000` und `9000`

| Funktionsname           | Was sie macht                                                  | Parameter |
| :---------------------- | :------------------------------------------------------------- | :-------- |
| `turnLeftThumb`         | Setzt die Position (Drehung) des linken Daumens.               | `amount`  |
| `curlLeftThumb`         | Setzt die Position (Krümmung) des linken Daumens.              | `amount`  |
| `curlLeftIndex`         | Setzt die Position (Krümmung) des linken Zeigefingers.         | `amount`  |
| `curlLeftMiddle`        | Setzt die Position (Krümmung) des linken Mittelfingers.        | `amount`  |
| `curlLeftRing`          | Setzt die Position (Krümmung) des linken Ringfingers.          | `amount`  |
| `curlLeftPinky`         | Setzt die Position (Krümmung) des linken kleinen Fingers.      | `amount`  |
| `curlLefWrist`          | Setzt die Position (Krümmung) des linken Handgelenks.          | `amount`  |
| `turnRightThumb`        | Setzt die Position (Drehung) des rechten Daumens.              | `amount`  |
| `curlRightThumb`        | Setzt die Position (Krümmung) des rechten Daumens.             | `amount`  |
| `curlRightIndex`        | Setzt die Position (Krümmung) des rechten Zeigefingers.        | `amount`  |
| `curlRightMiddle`       | Setzt die Position (Krümmung) des rechten Mittelfingers.       | `amount`  |
| `curlRightRing`         | Setzt die Position (Krümmung) des rechten Ringfingers.         | `amount`  |
| `curlRightPinky`        | Setzt die Position (Krümmung) des rechten kleinen Fingers.     | `amount`  |
| `curlRightWrist`        | Setzt die Position (Krümmung) des rechten Handgelenks.         | `amount`  |
| `turnLeftUnderarm`      | Setzt die Position (Drehung) des linken Unterarms.             | `amount`  |
| `turnRightUnderarm`     | Setzt die Position (Drehung) des rechten Unterarms.            | `amount`  |
| `curlLeftEllbow`        | Setzt die Position (Beugung/Krümmung) des linken Ellenbogens.  | `amount`  |
| `curlRightEllbow`       | Setzt die Position (Beugung/Krümmung) des rechten Ellenbogens. | `amount`  |
| `turnLeftUperarm`       | Setzt die Position (Drehung) des linken Oberarms.              | `amount`  |
| `turnRightUperarm`      | Setzt die Position (Drehung) des rechten Oberarms.             | `amount`  |
| `turnLeftShoulderHor`   | Setzt die horizontale Position der linken Schulter.            | `amount`  |
| `turnLeftShoulderVert`  | Setzt die vertikale Position der linken Schulter.              | `amount`  |
| `turnRightShoulderHor`  | Setzt die horizontale Position der rechten Schulter.           | `amount`  |
| `turnRightShoulderVert` | Setzt die vertikale Position der rechten Schulter.             | `amount`  |
| `turnHeadHor`           | Setzt die horizontale Drehung des Kopfes.                      | `amount`  |
| `turnHeadVert`          | Setzt die vertikale Neigung des Kopfes.                        | `amount`  |
| `relaxLeftFingers`      | Entspannt alle linken Finger.                                  | Keine     |
| `moveLeftFingers`       | Bewegt alle linken Finger um den Betrag.                       | `amount`  |
| `curlLeftFingers`       | Krümmt alle linken Finger.                                     | Keine     |
| `relaxRightFingers`     | Entspannt alle rechten Finger.                                 | Keine     |
| `moveRightFingers`      | Bewegt alle rechten Finger um den Betrag.                      | `amount`  |
| `curlRightFingers`      | Krümmt alle rechten Finger.                                    | Keine     |
| `relaxLeftArm`          | Entspannt den linken Arm.                                      | Keine     |
| `relaxRightArm`         | Entspannt den rechten Arm.                                     | Keine     |
| `liftLeftArm`           | Hebt den linken Arm.                                           | Keine     |
| `liftRightArm`          | Hebt den rechten Arm.                                          | Keine     |
| `relaxLeftShoulder`     | Entspannt die linke Schulter.                                  | Keine     |
| `relaxRightShoulder`    | Entspannt die rechte Schulter.                                 | Keine     |
| `relaxHead`             | Entspannt den Kopf.                                            | Keine     |
| `relaxFingers`          | Entspannt Finger beider Hände.                                 | Keine     |
| `moveFingers`           | Bewegt Finger beider Hände um den Betrag.                      | `amount`  |
| `curlFingers`           | Krümmt Finger beider Hände.                                    | Keine     |
| `relaxArms`             | Entspannt beide Arme.                                          | Keine     |
| `relaxShoulders`        | Entspannt beide Schultern.                                     | Keine     |
| `relaxPos`              | Stellt eine entspannte Gesamtposition her.                     | Keine     |
| `readyPos`              | Stellt eine "bereite" Position her.                            | Keine     |
