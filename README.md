# Simple Websocket RPC Server

Ein einfaches Remote Procedure Call System, mit der Möglichkeit, Serverfunktionen Asynchron aufzurufen.

## Inhaltsverzeichnis:

- [Installation](#installation)
- [Setup und Ausführung](#setup-und-ausführung)
- [Verwendung](#verwendung)
- [Anmerkungen](#anmerkungen)

## Installation

pip install -r requirements.txt

## Setup und Ausführung

### 1. Server starten

In einem Terminal führe das aus:
```bash
python websocket_server.py
```

**Erwartete Ausgabe:**
```
Server läuft auf localhost:3000
```

Der Server läuft und wartet auf den Client.

### 2. Client ausführen

In einem neuen Terminal führe das aus, ohne den Server zu schließen:

```bash
python websocket_client.py
```

Falls Server nicht läuft (oder die falsche konfig eingestellt ist, standardmäßig ist es localhost:3000), dann wird folgendes ausgegeben:

```
WS-Server konnte nicht verbunden werden, überprüfe ob er läuft
```

## Verwendung
Standardmäßig sind ein paar Tests implementiert im websocket_client. Weitere Tests können über die `main()` Methode hinzugefügt oder geändert werden.

Die `call()` Methode wird in `main()` verwendet, um Aufrufe an den Server zu starten. Derzeit ist jedoch nur `add_two_numbers()` implementiert.

## Anmerkungen

Ich habe in dem Call auch noch die Aufgabe bekommen, zu zeigen, wie "effizient" ich bin und deswegen habe ich meine eigene Zeit getrackt. Um 17:04 habe ich begonnen und um 17:55 war ich exklusive Documentation und README.md fertig.

Optional könnte man die Scripts noch erweitern, dass sie beide auf eine .env datei zugreifen, die zb den Host und den Port vom Server beinhalten, damit es dazwischen keine probleme gibt, war hier aber nicht gefragt.
