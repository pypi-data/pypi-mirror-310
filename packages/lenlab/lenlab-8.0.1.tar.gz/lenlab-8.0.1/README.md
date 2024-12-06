# Lenlab 8 for MSPM0G3507

## Liebe Studierende im LEN Workshop A am KIT!

Lenlab in der Version 8.0 funktioniert für den LEN Workshop A. Ich werde in den nächsten Tagen
noch einige Details verbessern (Fehlermeldungen, Übersetzung, Screenshot, ...). Starten Sie Lenlab mit 

```shell
uvx lenlab@latest
```

wenn Sie Internet haben. Dann lädt `uvx` automatisch Updates herunter.

Wenn Sie nicht weiterkommen, fragen Sie bitte in der Übung am Mittwoch, im Ilias und in den Tutorien.

## Installation (uv)

Starten Sie das Programm "Terminal".

Installieren Sie `uv`:

Windows:

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

MacOS oder Linux:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Weitere Informationen zur Installation finden Sie in der Dokumentation zu `uv`:
https://docs.astral.sh/uv/getting-started/installation/

Schließen Sie das Terminal und starten Sie es neu, dann findet es die eben installierten Kommandos `uv` und `uvx`.

## Lenlab Starten

```shell
uvx lenlab@latest
```

`uvx` lädt Lenlab in der neuesten Version herunter und führt es aus.

Wenn Sie keine Internetverbindung haben starten Sie Lenlab ohne `@latest`

```shell
uvx lenlab
```

`uvx` hat den Download beim ersten Mal gespeichert und führt die lokale Kopie aus ohne Zugriff auf das Internet. 

## Lenlab Testen

Halten Sie die Taste S1 des Launchpads neben der grünen LED gedrückt und drücken Sie kurz auf die Taste RESET (NRST) neben
dem USB-Stecker. Der Mikrocontroller startet den "Bootstrap Loader" für das Programmieren (Flashen) einer
neuen Firmware. Sie haben dann 10 Sekunden Zeit, das Programmieren zu starten. Danach schläft der Mikrocontroller ein
und braucht ein neues S1 + RESET zum Aufwachen. Es kann sein, dass `uvx` beim ersten Mal zu lange braucht für den Download.
Versuchen Sie es in diesem Fall nochmal, `uvx` hat dann den Download in einem Zwischenspeicher und startet schneller. 

```shell
uvx lenlab@latest exercise --log lenlab.log
```

`uvx lenlab exercise` sammelt einige Information über Ihr System und die Verbindung zum Launchpad. Dann programmiert
es die Firmware auf das Launchpad, startet die Firmware und testet die Kommunikation. Es überträgt etwa 28 MB Daten
in etwa 6 Minuten. `lenlab exercise` kann jederzeit mit Strg+C (Command+Punkt auf Mac) unterbrochen werden.

Wenn es schreibt `ERROR:lenlab.flash:Programming failed`, versuchen Sie es bitte nochmal von Anfang an mit S1 + RESET.
Mit der Taste "Pfeil nach oben" blättert das Terminal zu vorherigen Befehlen.

Mit `--log DATEINAME` speichert es die Ausgabe in der Logdatei unter "DATEINAME". Bitte senden Sie mir diese Datei
per E-Mail. Die Datei befindet sich im Home-Verzeichnis, wenn Sie das Verzeichnis nicht gewechselt haben:

- Windows: `C:\Benutzer\BENUTZERNAME\DATEINAME` oder `C:\Users\BENUTZERNAME\DATEINAME`
- Mac: `/Users/BENUTZERNAME/DATEINAME`

Der Befehl `pwd` zeigt den Namen des Verzeichnisses an, in dem das Terminal momentan arbeitet (Linux, Mac und Windows):

```shell
pwd
```

Wenn Sie lesen möchten, welche Informationen Sie verschicken:

Windows:

```shell
ii lenlab.log
```

Mac:

```shell
open -e lenlab.log
```

## Lenlab CLI

```shell
lenlab --help 
```

### Commands

- sys_info
- profile
- flash
- exercise
