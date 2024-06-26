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

## Einblicke ins Spiel
Im Startbildschirm erhält der Spieler Instruktionen darüber, welche Tasen welche Befehle bedingen. 

<img src="images/start_menu.jpg" alt="Game Example" width="500">

Drückt der Spieler auf Start öffnet sich das Spielfeld mit verschiedenen Hindernissen. Der Spieler muss nun den kürzesten weg zwischen grünem und rotem Block finden durch setzen von Blöcken. Durch Hindernisse kann der Spieler nicht hindurch gehen. 

<img src="images/game_run1.jpg" alt="Game Example" width="500">

Drückt der Spieler nun die SPACE-Taste, dann erfährt er, ob er den tatsächlichen kürzesten Weg gefunden hat oder ob der Computer besser war.

<img src="images/game_run2.jpg" alt="Game Example" width="500">

## Benötigte Module
Folgende Module müssen installiert werden, um das volle Spielerlebnis zu genießen:
- `pygame`
- `pygame_menu`

Die beste Herangehensweise wäre, eine virutelle Umgebung für die Installation zu verwenden (https://docs.python.org/3/library/venv.html)
