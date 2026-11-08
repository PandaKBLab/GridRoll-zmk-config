# GridRoll

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · **Deutsch**

ZMK-Firmware für PandaKB GridRoll: 47 Tasten, linker Drehgeber, rechter PAW3222-Trackball, USB/Bluetooth sowie ZMK Studio und DYA Studio. **Rechts verbindet sich mit dem PC, links drahtlos mit rechts.** Der Gerätename ist **GridRoll**. PCB-Projekte, Schaltpläne, Leiterbahnen und interne Schaltungsunterlagen werden nicht verteilt.

## Aktualisieren

Ein erfolgreicher [Actions-Lauf](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/workflows/build.yml) liefert nur **GridRoll-firmware** mit drei UF2-Dateien: links, rechts und settings-reset. Die normalen Dateien auf die entsprechende Hälfte schreiben. **Bei normalen Updates kein settings-reset verwenden**; Kopplungen und gespeicherte Einstellungen bleiben erhalten. Siehe [Erstinstallation](docs/first-flash.md). Artefakte sind 30 Tage verfügbar.

## Vier Funktionsebenen

| Ebene | Zweck und Zugriff | Drehgeber CW/CCW |
|---|---|---|
| L0 Base | QWERTY; linke Leertaste und rechte Eingabetaste als normale Tasten | Rad hoch/runter |
| L1 Mouse | Automatisch durch Ballbewegung oder manuell Fn+B; Esc beendet | Rad hoch/runter |
| L2 Symbols | Symbols links neben der linken Leertaste halten | Rad hoch/runter |
| L3 Function | Fn rechts neben Enter halten; auch Ballscrollen | Lauter/leiser |
| L4–L7 | Leere editierbare Plätze; Tasten und Drehgeber ohne Aktion | Keine |

Untere Reihe: Ctrl, Alt, GUI, Mittelklick, Symbols, **Leertaste** | **Enter**, Fn, Trackballöffnung, Links, Unten, Rechts. Der frühere Enter-Platz rechts in Reihe 3 ist jetzt rechte Umschalttaste. [Alle Tastenwerte und Diagramme](docs/keymap.md).

Gespeicherte Studio-Belegungen überschreiben Quelltextvorgaben. Für die neue Belegung zuerst exportieren, dann **Restore Stock Settings für die Tastenbelegung in ZMK Studio** verwenden und speichern. Kein Kopplungsreset ist nötig. DYA-Drehgeberwerte separat ändern: L0–L2 Rad hoch/runter, L3 Lauter/leiser, L4–L7 keine Aktion.

## Trackball und Verbindungen

Standard ist der freigegebene native Wert **798 CPI, ungefähr 800 DPI**, ohne weitere Korrektur. Bei DYA-Skalierung 1/1 hält L1 links Reihe 4/Spalte 6 (Leertastenplatz) ein Viertel der normalen Geschwindigkeit, ungefähr **200 DPI**; Loslassen stellt die normale Geschwindigkeit her. J/K/H sind Links-/Rechts-/Mittelklick, L Zurück, Semikolon Vorwärts, U/I und O/P vertikales/horizontales Rad. M in Mouse oder Fn in Base halten aktiviert Ballscrollen. 200ms Tippschutz, 1200ms Mouse-Auslauf und Ziehschutz bleiben erhalten.

Fn+A/S/D/F/G wählen BLE-Profile 0–4; Fn+Z löscht bei Bedarf nur die aktuelle Kopplung. Fn+X wählt USB, Fn+C BLE. Neue PC-USB-Erkennung bevorzugt USB automatisch, reines Laden erzwingt keinen Wechsel.

**Beide Studios bleiben entsperrt**, ohne Entsperrtaste oder erneute Sperre im Leerlauf/nach Trennung. Für Kabelbetrieb rechte USB-Buchse, USB-Ausgabe und den richtigen seriellen Port verwenden. Für Funk mit demselben PC gekoppelt bleiben, BLE-Ausgabe wählen und **Fn+V** drücken, dann in DYA erneut suchen.

Das Erkennungsfenster dauert höchstens **60 Sekunden**. Eine neue BLE-Hostverbindung oder Auswahl von BLE nach USB öffnet ebenfalls ein Fenster. Leerlauf, USB-Ausgabe, Trennung oder Ablauf beenden die zusätzliche Werbung. Normale Eingaben verlängern sie nicht endlos; bestehende GATT-Sitzungen werden dabei nicht absichtlich getrennt. Dies ist keine Entsperrtaste. Die Firmware korrigiert die fehlende Werbung bei verbundenem Host und ergänzt die Studio-UUID in der Scan-Antwort. Echte Windows-/Browser-Verbindung und Speichern müssen am Gerät geprüft werden. [Schritte und Grenzen](docs/studio-wireless.md).

## Energie und LEDs

Nach 30s ohne Eingabe Leerlauf, nach 15min im Akkubetrieb Tiefschlaf. Jede schlafende Hälfte per Taste wecken; Ball-/Drehgeberbewegung ist keine zugesicherte Tiefschlaf-Weckquelle. USB-versorgte Hälften bleiben wach. Drahtlose Studio-Änderungen vor dem Schlaf speichern. Das Erkennungsfenster erzeugt keine künstliche Aktivität, dauerhafte Werbung oder zusätzliche Akkupolling-Schleife.

Rot zeigt rechts den PC-Verbindungszustand und auf jeder Seite deren niedrigen Akkustand; im Leerlauf/Schlaf aus. Blau bleibt die Hardware-Ladezyklusanzeige; Dunkelheit allein beweist keinen vollen Akku. [LED-Regeln](docs/led-status.md). Stromverbrauch, Bediengefühl und Aufwachen müssen am Gerät geprüft werden.

[Wartung](docs/maintenance.md) · [Prüfstatus](docs/validation.md). Abhängigkeiten bleiben festgeschrieben. Eigener Code MIT, siehe [Drittanbieterhinweise](THIRD_PARTY_NOTICES.md).
