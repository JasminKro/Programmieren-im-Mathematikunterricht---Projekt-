# Programmieren im Mathematikunterricht - Projekt

Dies ist das GitHub-Repository für die Implementierung des Projekts für das Fach "Programmieren im Mathematikunterricht"! Implementiert wurde ein kleines Spiel in Python, bei der ein Spieler den kürzesten Pfad zwischen zwei Punkten finden muss. 

## Ersteller
- Philip Hallwirth
- Jasmin Kropshofer
- Manfred Trauner

## Spielprinzip
Der Spieler sieht ein Feld mit 20x20 Blöcken. Zwei dieser Blöcke sind gefärbt, einer grün und der andere rot. Diese Felder markieren den Start- und den Endpunkt. Das Ziel ist es, den kürzesten Weg zwischen Start- und Endpunkt zu finden, indem man per Mausklick Blöcke setzt. Dabei ist es nur erlaubt, nach rechts, links, oben und unten Blöcke zu setzen. Einen Weg diagonal setzen, ist also nicht zulässig. Drückt man die SPACE Taste, dann wird der tatsächliche kürzeste Pfad berechnet. Hat der Spieler einen Pfad gefunden, der genauso lang ist wie der tatsächliche kürzeste Pfad, dann gewinnt der Spieler und eine entsprechende Meldung erscheint. Gelingt es dem Spieler nicht, den kürzesten Pfad zu finden, oder setzt er zu wenig Blöcke, dann verliert er leider. 

## Mögliche Erweiterung und Abgrenzung
Natürlich ist das Spiel so, wie es aktuell ist, recht simpel und man kann leicht gegen den Computer gewinnen. Es wäre also durchaus spannender, mehrere Knoten hinzuzufügen, die man auf seinem Weg nutzen muss, um zum Ende zu kommen, damit das Spiel schwieriger wird und der Dijkstra auch tatsächlich mehr Sinn ergibt. Leider ist das etwas außerhalb des Rahmens für das Projekt, weshalb das hier nicht implementiert wurde. 

## Todo
- vll unnötige komplizierte Sachen einfacher gestalten
- vll im README ein paar Bilder einfügen vom Game-Verlauf so als Beispiele --> kann ich gern noch machen am ende, will ich aber nicht machen, bevor nicht sicher ist, ob nicht doch noch änderungen durchgeführt werden
- Optional bzw. to be dicussed: Erweiterung durch mehrere Knoten, damit der Dijkstra auch wirklich Sinn hat (wenn, dann oberen Text umformulieren) --> wäre auf jeden fall toll(!), aber ist für die abgabe denke ich schon zu viel aufwand


## Done
- Press R macht leider noch nichts, sollte das Feld neu laden und alles zurücksetzen.
- Ich bin mir noch unsicher, ob der Dijkstra 100% korrekt arbeitet --> dürfte noch nicht zu hundert prozent funktionieren: ![Game Example](images/15bigger17.jpg)
konnte allerdings noch kein Problem finden, es dürfte allerdings daran liegen, dass der Algorithmus am falschen Punkt beginnt -> geht jetzt, da der user input überschrieben wird
- Die Ausgabe, ob gewonnen/verloren wurde sollte noch schöner/ausführlicher gestaltet werden (also der Text; zB "Congratulations! You found the shortest path and beat the computer" und vll wieder ein Emoji oder so) --> habe das "beat" entfernt, der spieler hat ja eig. nicht die chance den pc zu "beaten" und das end design  überarbeitet

## Benötigte Module
Folgende Module müssen installiert werden, um das volle Spielerlebnis zu genießen:
- `pygame`
- `pygame_menu`
