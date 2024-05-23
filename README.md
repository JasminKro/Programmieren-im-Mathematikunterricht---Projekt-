# Programmieren im Mathematikunterricht - Projekt

Dies ist das GitHub-Repository für die Implementierung des Projekts für das Fach "Programmieren im Mathematikunterricht"! Implementiert wurde ein kleines Spiel, bei der ein Spieler den kürzesten Pfad zwischen zwei Punkten finden muss. 

## Ersteller
- Manfred Trauner
- Philip Hallwirth
- Jasmin Kropshofer

## Spielprinzip
Der Spieler sieht ein Feld mit 20x20 Blöcken. Zwei dieser Blöcke sind gefärbt, einer grün und der andere rot. Diese Felder markieren den Start- und den Endpunkt. Das Ziel ist es, den kürzesten Weg zwischen Start- und Endpunkt zu finden, indem man per Mausklick Blöcke setzt. Dabei ist es nur erlaubt, nach rechts, links, oben und unten Blöcke zu setzen. Einen Weg diagonal setzen, ist also nicht zulässig.

## Todo
- Ich bin mir noch unsicher, ob der Dijkstra 100% korrekt arbeitet
- Press R macht leider noch nichts, sollte das Feld neu laden und alles zurücksetzen.
- vll unnötige komplizierte Sachen einfacher gestalten
- vll im README ein paar Bilder einfügen vom Game-Verlauf so als Beispiele
- Optional bzw. to be dicussed: Erweiterung durch mehrere Knoten, damit der Dijkstra auch wirklich Sinn hat

## Benötigte Module
Folgende Module müssen installiert werden, um das volle Spielerlebnis zu genießen:
- `pygame`
- `pygame_menu`
