# camera

## tc.py

tc.py ist die eigenliche funktion. Sie tracked mit einer Kamera die Bewegung einer Person, wandelt diese um und führt sie als Pib aus.

**Wichtig:** Der Piblib Ordener muss in diesen Ordner kopiert werden, ansonsten funktioniert es nicht.

Bis jetzt werden nur die Hände und Ellbogen getracked. Das Kamera Programm macht bei verschiedenen Punkte am Körper ein Punkt und misst dann anschliessend die Distanz zu jeweils zwei Punkten. Z.B. Wenn die Spitze des Zeigefingers näher am Handeglenk ist, dann ist er höchstwahrscheinlich gekrümmt. Dies hat jedoch verschiedene Probleme und kann unpräzise sein.

-> gerne noch verbessern und ausbauen. Evtl. einen neuen Ansatz prüfen.

## camera_stream.py

Dies ist ausschliesslich eine Trubleshooting datei. Sie prüft, ob eine Kamera vorhanden ist und ob eine verbindung hergestellt werden kann. Dieses Sktipt empfielt sich auszuführen, wenn es beim obigen einen Fehler gibt. Meistens ist die Kamera nicht richtig verbunden `;)`.
