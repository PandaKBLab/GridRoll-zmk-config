# GridRoll

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · **Deutsch**

ZMK-Firmware für die geteilte PandaKB GridRoll: 47 Tasten, linker Drehgeber, rechter PAW3222-Trackball, USB/Bluetooth, ZMK Studio und DYA Studio.

Die **rechte Hälfte ist die Zentrale** und verbindet sich mit dem Computer. Die linke Hälfte verbindet sich drahtlos mit ihr. Tastatur-, Bluetooth- und USB-Produktname lauten **GridRoll**.

Dieses Repository enthält Firmware, Build-Werkzeuge und Anleitungen. PCB-Projekte, Schaltpläne, Leiterbahndaten, Netzlisten und interne Schaltungsunterlagen werden nicht verteilt. Die notwendigen GPIO-Definitionen bleiben im Board-Quellcode.

## Download und Aktualisierung

1. Öffnen Sie einen erfolgreichen Lauf unter [Build GridRoll firmware](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/workflows/build.yml).
2. Laden Sie nur die ZIP **GridRoll-firmware** herunter. Sie enthält genau drei Dateien: **GridRoll-left.uf2**, **GridRoll-right.uf2** und **GridRoll-settings-reset.uf2**.
3. Starten Sie den Bootloader auf beiden Hälften. Kopieren Sie GridRoll-left.uf2 auf die linke und GridRoll-right.uf2 auf die rechte Hälfte. Die Rücksetz-Firmware ist nicht für den normalen Betrieb gedacht.
4. Ohne installierten GridRoll-Bootloader ist zunächst die [Erstinstallation](docs/first-flash.md) nötig. Das Erstinstallationspaket muss separat gebaut werden und ist nicht in dieser ZIP enthalten.

Artefakte werden 30 Tage gespeichert. Ein erfolgreicher Build bestätigt Softwareprüfungen, aber keine bestandenen Gerätetests.

## Bluetooth und Studio

Koppeln Sie den Computer mit **GridRoll auf der rechten Hälfte**. Wenn die Tastatur unsichtbar ist, wählen Sie ein freies Bluetooth-Profil oder löschen Sie das aktuelle Profil und die alte Kopplung am Computer. Normale Updates erhalten gespeicherte Kopplungen.

Halten Sie **Tab oben links** für System: **Q** oben wählt Profil 0, **Backspace** löscht es, **Y** wählt USB und **U** BLE. Sobald der PC die rechte USB-Hälfte erkennt, wird USB auch bei gespeicherter BLE-Präferenz bevorzugt. Reine Ladeverbindungen erzwingen keinen Wechsel; nach dem Abziehen ist ein verbundener BLE-Host verfügbar. Eine manuelle BLE-Auswahl bleibt bis zur nächsten USB-Verbindung erhalten. Gespeicherte Belegungen können abweichen.

Für [ZMK Studio](https://zmk.studio/) oder [DYA Studio](https://studio.dya.cormoran.works/) verbinden Sie die **rechte Hälfte per USB** und wählen USB-Ausgabe sowie den seriellen Anschluss. **Die Bearbeitung ist standardmäßig entsperrt; eine Entsperrtaste ist nicht nötig. Leerlauf und Trennen sperren sie nicht erneut.** Schließen Sie andere Seiten mit demselben Anschluss und speichern Sie Änderungen. Updates erhalten Studio/DYA-Einstellungen. Entfernen Sie eine zuvor in DYA eingestellte Drehkorrektur: Die feste Montagekorrektur erfolgt vor der Zeiger- und Scrollverarbeitung.

Beide Oberflächen unterstützen die Tastenbelegung; DYA bietet mouse-/scroll-Einstellungen und **Drehgeber-Zuweisungen je Ebene und Drehrichtung**. Auf der Basisebene scrollt der Drehgeber im Uhrzeigersinn nach unten, gegen den Uhrzeigersinn nach oben. CI prüft drei festgeschriebene DYA-Protokolle und die entsperrte Konfiguration. Nicht implementierte Sensorbilder sind nicht enthalten.

## Acht Standardebenen

Sieben LiNEA40-Ebenen dienen als Vorlage für GridRolls 47 Tasten; hinzu kommt System. Alle acht sind aktiviert. [Alle Tastenwerte, Diagramme, Ebenenzugriffe und Drehgeberfunktionen](docs/keymap.md) sind dokumentiert. Die englische Startseite zeigt alle Diagramme, aus dem Quell-Keymap erzeugt und in CI abgeglichen.

Normale Updates behalten Studio-Belegungen. Für neue Standardwerte zuerst exportieren und dann in Studio die Standardbelegung wiederherstellen. settings-reset ist dafür unnötig. Japanische Symbol-Keycodes bleiben erhalten; Zeichen hängen vom PC-Tastaturlayout ab.

## Energiesparen und Aufwachen

- Nach **30 Sekunden** ohne Eingabe beginnt der Leerlauf; Bluetooth bleibt verfügbar.
- Im Akkubetrieb beginnt nach **15 Minuten** ohne Eingabe der Tiefschlaf. Drücken Sie auf jeder schlafenden Hälfte eine Taste und warten Sie auf die Bluetooth-Verbindung. Trackball- oder Drehgeberbewegungen sind keine zugesicherten Weckquellen.
- USB-versorgte Hälften bleiben für USB/Studio wach. Speichern Sie Studio-Änderungen vor dem Schlafmodus, da ungesicherte RAM-Inhalte verloren gehen.
- Der Trackball nutzt MOTION-Interrupts und vorhandene Ruhemodi des Sensors. Stromaufnahme und Aufwachverhalten müssen am Gerät geprüft werden.
- Bei BLE werden Bewegungen unter Erhalt der gesamten Strecke zu Berichten mit mindestens **8 ms** Abstand zusammengefasst. USB bleibt unmittelbar. Die rechte Hälfte fordert **7,5 ms** Verbindungsintervall ohne Peripheral Latency an; die tatsächlichen Werte bestimmt der Host. Der Verbrauch im verbundenen Leerlauf kann steigen. Bewegungsqualität und Stromaufnahme müssen noch am Gerät geprüft werden.

Siehe [Wartung](docs/maintenance.md), [Firmware-Kompatibilität](docs/hardware.md) und [Prüfstatus](docs/validation.md). Abhängigkeiten sind in config/west.yml festgeschrieben. Eigener Code steht unter MIT; Lizenzen der Abhängigkeiten stehen in den [Drittanbieterhinweisen](THIRD_PARTY_NOTICES.md).
