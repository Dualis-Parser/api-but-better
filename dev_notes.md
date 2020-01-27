# dev notes
## try to display accurate component names
The current way of parsing the modules is searching the exams section of the
modules details page and just returning the row that contains a grade. The 
content of that row may be a name like "Betriebssysteme", which is OK, but it
also may be "Klausurarbeit" or "Kombinierte Prüfung" which doesn't say anything
at all. A better way would be (if possible) to display the unit name and/or
number like: "T3INF2001.1 - Applied Mathematics". Dualis shows these components
in the list in different ways, I try to differentiate all of them and reliably
parse the correct unit name and number according to an exam.

## Ways of display
* For every module the table holds the semster name (one per row, no doubles)  
* **Multi-semester Modules hold the unit name + number in the `level102` row**
* **Some modules only have one unit, that is easy to parse :)**
* Some module units are not able to be parsed (only indexable by name, but it may be german vs english, so rip)
* The rest should be just read from the row (sorry, no possible parsing yet)