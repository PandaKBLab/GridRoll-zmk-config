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

In der Standardbelegung öffnet **Fn + Mouse** die System-Ebene: Die Position **Q** oben wählt Profil 0, **Backspace** löscht dieses Profil und **U** wählt BLE-Ausgabe. In Studio gespeicherte Belegungen können abweichen.

Für [ZMK Studio](https://zmk.studio/) oder [DYA Studio](https://studio.dya.cormoran.works/) verbinden Sie die **rechte Hälfte per USB**, wählen USB-Ausgabe und entsperren die Bearbeitung mit der Taste oben links auf der System-Ebene. Schließen Sie andere Seiten mit demselben seriellen Anschluss und speichern Sie Änderungen. Updates erhalten Studio/DYA-Einstellungen. Entfernen Sie eine zuvor in DYA eingestellte Drehkorrektur des Trackballs: Die neue feste Montagekorrektur erfolgt vor der Zeiger- und Scrollverarbeitung.

## Energiesparen und Aufwachen

- Nach **30 Sekunden** ohne Eingabe beginnt der Leerlauf; Bluetooth bleibt verfügbar.
- Im Akkubetrieb beginnt nach **15 Minuten** ohne Eingabe der Tiefschlaf. Drücken Sie auf jeder schlafenden Hälfte eine Taste und warten Sie auf die Bluetooth-Verbindung. Trackball- oder Drehgeberbewegungen sind keine zugesicherten Weckquellen.
- USB-versorgte Hälften bleiben für USB/Studio wach. Speichern Sie Studio-Änderungen vor dem Schlafmodus, da ungesicherte RAM-Inhalte verloren gehen.
- Der Trackball nutzt MOTION-Interrupts und vorhandene Ruhemodi des Sensors. Stromaufnahme und Aufwachverhalten müssen am Gerät geprüft werden.

Siehe [Wartung](docs/maintenance.md), [Firmware-Kompatibilität](docs/hardware.md) und [Prüfstatus](docs/validation.md). Abhängigkeiten sind in config/west.yml festgeschrieben. Eigener Code steht unter MIT; Lizenzen der Abhängigkeiten stehen in den [Drittanbieterhinweisen](THIRD_PARTY_NOTICES.md).
