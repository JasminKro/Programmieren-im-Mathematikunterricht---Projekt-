# Programmieren im Mathematikunterricht - Projekt

Dies ist das GitHub-Repository für die Implementierung des Projekts für das Fach "Programmieren im Mathematikunterricht"! Implementiert wurde ein kleines Spiel, bei der ein Spieler den kürzesten Pfad zwischen zwei Punkten finden muss. 

## Ersteller
- Manfred Trauner
- Philip Hallwirth
- Jasmin Kropshofer

## Spielprinzip
Der Spieler sieht ein Feld mit 20x20 Blöcken. Zwei dieser Blöcke sind gefärbt, einer grün und der andere rot. Diese Felder markieren den Start- und den Endpunkt. Das Ziel ist es, den kürzesten Weg zwischen Start- und Endpunkt zu finden, indem man per Mausklick Blöcke setzt. Dabei ist es nur erlaubt, nach rechts, links, oben und unten Blöcke zu setzen. Einen Weg diagonal setzen, ist also nicht zulässig.

## Todo
- Leider funktioniert das Anzeigen des kürzesten Pfads noch nicht (wenn man die Leertaste drückt, sollte sie den Benutzereingang überschreiben). Ich habe mich noch nicht damit beschäftigt.
- Press R macht leider noch nichts, sollte das Feld neu laden und alles zurücksetzen.

## Benötigte Module
Folgende Module müssen installiert werden, um das volle Spielerlebnis zu genießen:
- `pygame`
- `pygame_menu`
