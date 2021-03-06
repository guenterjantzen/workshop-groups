# workshop-groups
Ein Workshop findet in mehreren Runden statt und wird aufgeteilt in kleinere Gruppen. Dabei soll niemand der gleichen Person ein zweites Mal begegnen. Der Einfachheit halber haben alle Gruppen die gleiche Größe von n Personen. Weiter gibt es auch in jeder Runde n Gruppen. Die Gesamtzahl aller Teilnehmer ist also n^2. 

Diese Voraussetzung *quadratischer Workshops* klingt zunächst wie eine heftige Einschränkung, ist es aber nicht, da sich viele andere Workshops davon ableiten lassen.

Ein *vollständiger Workshop* ist ein Workshop, bei dem alle Teilnehmer in irgendeiner Runde einmal aufeinander treffen. 

Das Programm *wg3.py* ermittelt einen vollständigen Workshop für n^2 Personen, die durch Nummern 1,2,3,...,n^2 angegeben werden. So ein vollständiger Workshop hat n+1 Runden, von denen aber nur n Runden aufgelistet werden. Die erste Runde mit der "trivialen" Gruppenaufteilung

[1,2 ... n], [n+1, n+2 ... 2n] ... [n^2 - n+1, n^2 - n+2 ... n^2 ]

wird nicht angegeben. Trivial in Anführungsstrichen, aber man mache sich klar, dass es sich z.B. bei n=3 um die Aufteilung 

[1,2,3], [4,5,6], [7,8,9] handelt.

```
python wg3.py 3
```

ermittelt einen vollständigen Workshop für n=3.


Analog ermittelt

```
python wg3.py 4
```

oder 


```
python wg3.py 5
```

einen vollständigen Workshop für n=4 oder n=5.

Größeres n ist nicht sinnvoll, das Programm läuft dann zu lange.

Aktuell ist das Programm noch in einer recht frühen Version, und es lässt sich noch manches verbessern.  