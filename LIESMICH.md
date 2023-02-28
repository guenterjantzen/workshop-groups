Workshop Gruppenaufteilung
==========================

Ein Workshop findet in mehreren Runden statt und wird aufgeteilt in kleinere Gruppen. Dabei soll niemand der gleichen Person ein zweites Mal begegnen. Hier werden nur *ausgeglichene* Workshops betrachtet, bei denen die Aufteilung in jeder Runde gleich ist, und die Gruppengrößen möglichst gleich sind. Maximale und minimale Gruppengröße unterscheiden sich dann höchstens um 1. Ein Beispiel ist 14 Personen und 4 Gruppen mit Aufteilung 3,3,4,4.


## wg3.py
*Quadratische Workshops* sind Workshops mit n^2 Teilnehmern, die in jeder Runde n Gruppen mit jeweils n Personen bilden.

Diese Voraussetzung *quadratischer Workshops* klingt zunächst wie eine heftige Einschränkung, ist es aber nicht, da sich viele andere Workshops davon ableiten lassen.

Ein *vollständiger Workshop* ist ein Workshop, bei dem alle Teilnehmer in irgendeiner Runde einmal aufeinander treffen.

Das Programm *wg3.py* ermittelt mit Backtracking eine Liste lexikalisch sortierter vollständiger quadratischer Workshops für n^2 Personen, die durch Nummern 0,1,2,...,n^2 - 1 angegeben werden. So ein vollständiger Workshop hat n+1 Runden, von denen aber nur n Runden aufgelistet werden. Die initiale Runde mit der einfach durchnummerierten Gruppenaufteilung [0,1,2 ... n-1], [n, n+1, n+2 ... 2n - 1] ... [n^2 - n, n^2 - n+1, n^2 - n+2 ... n^2 -1] wird nicht immer angegeben.

Man mache sich klar, dass es sich z.B. bei n=3 um die Aufteilung [0,1,2], [3,4,5], [6,7,8] handelt.

`python wg3.py 3` ermittelt die lexikalisch sortierten vollständigen quadratischen Workshops für n=3, also für 9 Personen. Aufruf von `python wg3.py`gibt eine kurze Aufrufbeschreibung, `python wg3.py -h` eine Hilfe, die die Kommandozeilenoptionen beschreibt.

Größeres n als 5 ist nicht sinnvoll, das Programm läuft dann zu lange.

## wg_gf.py
Das Programm *wg_gf.py* ermittelt zu einer gegebenen Anzahl Personen einen ausgeglichenen Workshop. Wenn es Workshops mit unterschiedlichen Gruppenanzahlen gibt, kann wie im folgenden Beispiel eines Workshops für 17 Personen gezeigt wird,  sukzessive eingegrenzt werden:

    guenter@Hasepeter01:~/GJ/dev/github/workshop-groups$ ./wg_gf.py 17
    No Workshop found for person_count=17, groupcount=None, maxsize=None.
    Supported partitions for person_count 17 are:
    --groupcount  5 --maxsize  4 # 3-3-3-4-4
    --groupcount  7 --maxsize  3 # 2-2-2-2-3-3-3
    --groupcount  8 --maxsize  3 # 2-2-2-2-2-2-2-3
    guenter@Hasepeter01:~/GJ/dev/github/workshop-groups$ ./wg_gf.py 17 --maxsize 3
    Several Workshops found for person_count 17.
    Supported partitions for person_count 17 are:
    --groupcount  7 --maxsize  3 # 2-2-2-2-3-3-3
    --groupcount  8 --maxsize  3 # 2-2-2-2-2-2-2-3
    guenter@Hasepeter01:~/GJ/dev/github/workshop-groups$ ./wg_gf.py 17 --maxsize 3 --groupcount 7

    Workshop2 GF(7^1) for 17 persons, maxsize 3, groupcount 7
     0  7 14  |  1  8 15  |  2  9 16  |  3 10     |  4 11     |  5 12     |  6 13
     0  8 16  |  1  9     |  2 10     |  3 11     |  4 12     |  5 13 14  |  6  7 15
     0  9     |  1 10     |  2 11     |  3 12 14  |  4 13 15  |  5  7 16  |  6  8
     0 10     |  1 11 14  |  2 12 15  |  3 13 16  |  4  7     |  5  8     |  6  9
     0 11 15  |  1 12 16  |  2 13     |  3  7     |  4  8     |  5  9     |  6 10 14
     0 12     |  1 13     |  2  7     |  3  8     |  4  9 14  |  5 10 15  |  6 11 16
     0 13     |  1  7     |  2  8 14  |  3  9 15  |  4 10 16  |  5 11     |  6 12

## Installation
Es wird eine aktuelle *Python 3* Installation mit der Bibliothek *galois-field* benötigt.
Diese ist unter *https://github.com/syakoo/galois-field* zu finden. Die Installation wird dort beschrieben.
