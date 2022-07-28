# workshop-groups
Ein Workshop findet in mehreren Runden statt und wird aufgeteilt in kleinere Gruppen. Dabei soll niemand der gleichen Person ein zweites Mal begegnen.
*Quadratische Workshops* sind Workshops mit n^2 Teilnehmern, die in jeder Runde n Gruppen mit jeweils n Personen bilden.

Diese Voraussetzung *quadratischer Workshops* klingt zunächst wie eine heftige Einschränkung, ist es aber nicht, da sich viele andere Workshops davon ableiten lassen.

Ein *vollständiger Workshop* ist ein Workshop, bei dem alle Teilnehmer in irgendeiner Runde einmal aufeinander treffen.

Das Programm *wg3.py* ermittelt eine Liste lexikalisch sortierter vollständiger quadratischer Workshops für n^2 Personen, die durch Nummern 0,1,2,...,n^2 - 1 angegeben werden. So ein vollständiger Workshop hat n+1 Runden, von denen aber nur n Runden aufgelistet werden. Die erste Runde mit der "trivialen" Gruppenaufteilung

[0,1,2 ... n-1], [n, n+1, n+2 ... 2n - 1] ... [n^2 - n, n^2 - n+1, n^2 - n+2 ... n^2 -1]

wird nicht angegeben. Trivial in Anführungsstrichen, aber man mache sich klar, dass es sich z.B. bei n=3 um die Aufteilung

[0,1,2], [3,4,5], [6,7,8] handelt.

```
python wg3.py 3
```

ermittelt die lexikalisch sortierten vollständigne Workshops für n=3.

Aufruf von `python wg3.py`gibt eine kurze Aufrufbeschreibung, `python wg3.py -h` eine Hilfe, die die Kommandozeilenoptionen beschreibt.

Größeres n als 5 ist nicht sinnvoll, das Programm läuft dann zu lange.

Aktuell ist das Programm noch in einer recht frühen Version, und es lässt sich noch manches verbessern.
