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

In der Planck-Standardbelegung öffnet **Lower + Raise** die System-Ebene: Q wählt Profil 0, Backspace löscht es, Y wählt USB und U BLE. Sobald der PC die rechte Hälfte erkennt, wird USB bevorzugt. Nach dem Abziehen wird ein verbundener BLE-Host verwendet. Reines Laden erzwingt keinen Wechsel; manuelle BLE-Auswahl bleibt möglich. Gespeicherte Belegungen können abweichen.

Für [ZMK Studio](https://zmk.studio/) oder [DYA Studio](https://studio.dya.cormoran.works/) verbinden Sie die **rechte Hälfte per USB** und wählen USB-Ausgabe sowie den seriellen Anschluss. **Die Bearbeitung ist standardmäßig entsperrt; eine Entsperrtaste ist nicht nötig. Leerlauf und Trennen sperren sie nicht erneut.** Schließen Sie andere Seiten mit demselben Anschluss und speichern Sie Änderungen. Updates erhalten Studio/DYA-Einstellungen. Entfernen Sie eine zuvor in DYA eingestellte Drehkorrektur: Die feste Montagekorrektur erfolgt vor der Zeiger- und Scrollverarbeitung.

Beide Oberflächen unterstützen die Tastenbelegung; DYA bietet mouse-/scroll-Einstellungen und **Drehgeber-Zuweisungen je Ebene und Drehrichtung**. Auf der Basisebene scrollt der Drehgeber im Uhrzeigersinn nach oben, gegen den Uhrzeigersinn nach unten. CI prüft drei festgeschriebene DYA-Protokolle und die entsperrte Konfiguration. Nicht implementierte Sensorbilder sind nicht enthalten.

## Acht Standardebenen

Die Standardbelegung verwendet **Planck QWERTY / Lower / Raise** für 47 Tasten, ergänzt um Mouse, Navigation, Scroll, Wireless und System: acht aktive Ebenen. Tab/Esc/Shift/Satzzeichen/Enter sind normale Tasten; Lower + Raise öffnet System. Alte LiNEA40-Tippkombinationen entfallen. [Alle Tastenwerte und Diagramme](docs/keymap.md) werden aus dem Quelltext erzeugt und in CI geprüft.

## Automatische Maus-Ebene und Rad

Die erste gültige Ballbewegung aktiviert Mouse sofort, sofern in den letzten **200 ms** keine Taste gedrückt wurde. Diese Zeit schützt beim Tippen. **1200 ms** nach Bewegung, Radschritt oder Loslassen einer Maus-/Modifikatortaste endet Mouse. Gehaltene Tasten schützen das Ziehen; normale transparente Buchstabentasten oder Esc beenden die Ebene sofort.

**J=Linksklick, K=Rechtsklick, H=Mittelklick, L=Zurück, Semikolon=Vorwärts; U/I=Rad hoch/runter, O/P=horizontal.** M halten scrollt mit dem Ball; rechte Leertaste halten aktiviert Mouse manuell. Der Basis-Drehgeber sendet pro Sensorereignis einen diskreten Radschritt, statt der bisherigen zu kurzen 20-ms-Simulation.

Gespeicherte DYA-Werte bleiben unabhängig erhalten: mouse Temp-layer aktiviert, Ebene 1, Aktivierungsschutz 200 ms und Deaktivierung 1200 ms beibehalten. Alte Drehgeberwerte für L0/L1/L2/L3/L5/L6 gegebenenfalls auf CW=wheel up und CCW=wheel down ändern und speichern; die Lautstärke-Ebenen L4/L7 bleiben unverändert. Das Zurücksetzen des Studio-Keymaps löscht diese Werte nicht; settings-reset ist unnötig.

Normale Updates behalten Studio-Belegungen. Für neue Standardwerte zuerst exportieren und dann in Studio die Standardbelegung wiederherstellen. settings-reset ist dafür unnötig. Symbole verwenden übliche US-Keycodes; ausgegebene Zeichen hängen vom PC-Tastaturlayout ab.

In **L1 Mouse** hält **links 46 (Zeile 4, Spalte 6: unten rechts auf der linken Hälfte, Leertaste auf Base)** die Zeigergeschwindigkeit auf einem Viertel des normalen DYA-Werts; Loslassen stellt den normalen Wert wieder her. Base-Leertaste/Ctrl und Richtung bleiben erhalten. Bei einer in Studio gespeicherten Belegung L1 links 46 **Precision 0.25x (hold)** zuweisen, links 41 wieder auf transparent setzen und speichern; weder die ganze Belegung noch settings-reset zurücksetzen.

## LEDs und Akku

Rechts zeigt die rote LED die ausgewählte PC-Bluetooth-Verbindung: wartend 100 ms alle 2 s für höchstens 30 s; verbunden 2 s an, danach aus. Links zeigt sie nur den eigenen Akkustand, nicht die PC-Verbindung. Unter 15% geschätztem Akkustand leuchtet jede Seite 100 ms alle 30 s; ab 20% endet die Warnung. USB-Strom unterdrückt die Akkuwarnung. Im Leerlauf/Tiefschlaf ist Rot aus. Das Ende des Blinkfensters beendet keine Bluetooth-Werbung; normale USB-Ausgabe zeigt kein unnötiges Bluetooth-Warten.

Blau bleibt die hardwaregesteuerte Ladezyklusanzeige. Nach einem normalen ersten Ladezyklus erlischt sie; Dunkelheit allein bestätigt keinen vollen Akku. Geschätzte 100% erzeugen keine Vollladeanzeige. Siehe [LED-Regeln und Grenzen](docs/led-status.md).

Der vorhandene einzelne Akkusampler läuft aktiv alle 60 s, stoppt im Leerlauf und liefert nach dem Aufwachen einen frischen Wert. LEDs starten keinen zweiten ADC-Poller und erzeugen keine Aktivität gegen den Schlafmodus. Beide Hälften aktualisieren; settings-reset ist unnötig. Kopplungen und Studio-/DYA-Einstellungen bleiben erhalten.

## Energiesparen und Aufwachen

- Nach **30 Sekunden** ohne Eingabe beginnt der Leerlauf; Bluetooth bleibt verfügbar.
- Im Akkubetrieb beginnt nach **15 Minuten** ohne Eingabe der Tiefschlaf. Drücken Sie auf jeder schlafenden Hälfte eine Taste und warten Sie auf die Bluetooth-Verbindung. Trackball- oder Drehgeberbewegungen sind keine zugesicherten Weckquellen.
- USB-versorgte Hälften bleiben für USB/Studio wach. Speichern Sie Studio-Änderungen vor dem Schlafmodus, da ungesicherte RAM-Inhalte verloren gehen.
- Der Trackball nutzt MOTION-Interrupts und vorhandene Ruhemodi des Sensors. Stromaufnahme und Aufwachverhalten müssen am Gerät geprüft werden.
- Bei BLE werden Bewegungen unter Erhalt der gesamten Strecke zu Berichten mit mindestens **8 ms** Abstand zusammengefasst. USB bleibt unmittelbar. Die rechte Hälfte fordert **7,5 ms** Verbindungsintervall ohne Peripheral Latency an; die tatsächlichen Werte bestimmt der Host. Der Verbrauch im verbundenen Leerlauf kann steigen. Bewegungsqualität und Stromaufnahme müssen noch am Gerät geprüft werden.

Siehe [Wartung](docs/maintenance.md), [Firmware-Kompatibilität](docs/hardware.md) und [Prüfstatus](docs/validation.md). Abhängigkeiten sind in config/west.yml festgeschrieben. Eigener Code steht unter MIT; Lizenzen der Abhängigkeiten stehen in den [Drittanbieterhinweisen](THIRD_PARTY_NOTICES.md).
