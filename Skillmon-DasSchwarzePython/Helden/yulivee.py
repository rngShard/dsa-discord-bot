from ..proben import *
from ..held import *

# yulivee initialisieren
yulivee = Held("Yulivee Timerlan al'Jamila", "Yulivee")

## Basiseigenschaften {{{
yulivee.eigenschaften.basis = \
        {"mu":12,"kl":13,"in":13,"ch":12,"ff":12,"ge":15,"ko":12,"kk":11}
# }}}

## Talente {{{
# Körper
yulivee.neues_talent("Akrobatik",              1)
yulivee.neues_talent("Athletik",               1)
yulivee.neues_talent("Klettern",               2)
yulivee.neues_talent("Körperbeherrschung",     4)
yulivee.neues_talent("Schleichen",             5)
yulivee.neues_talent("Schwimmen",              0)
yulivee.neues_talent("Selbstbeherrschung",     0)
yulivee.neues_talent("Sich Verstecken",        4)
yulivee.neues_talent("Singen",                 1)
yulivee.neues_talent("Sinnenschärfe",          4)
yulivee.neues_talent("Tanzen",                 2)
yulivee.neues_talent("Taschendiebstahl",       1)
yulivee.neues_talent("Zechen",                 0)
# Gesellschaft
yulivee.neues_talent("Betören",                1)
yulivee.neues_talent("Etikette",               1)
yulivee.neues_talent("Gassenwissen",           3)
yulivee.neues_talent("Lehren",                 0)
yulivee.neues_talent("Menschenkenntnis",       4)
yulivee.neues_talent("Sich Verkleiden",        1)
yulivee.neues_talent("Überreden",              5)
# Natur
yulivee.neues_talent("Fährtensuche",           2)
yulivee.neues_talent("Fallenstellen",          3)
yulivee.neues_talent("Fesseln/Entfesseln",     3)
yulivee.neues_talent("Orientierung",           2)
yulivee.neues_talent("Wettervorhersage",       1)
yulivee.neues_talent("Wildnisleben",           2)
# Wissen
yulivee.neues_talent("Anatomie",               0)
yulivee.neues_talent("Brett-/Kartenspiel",     2)
yulivee.neues_talent("Geografie",              2)
yulivee.neues_talent("Geschichtswissen",       1)
yulivee.neues_talent("Götter/Kulte",           1)
yulivee.neues_talent("Pflanzenkunde",          2)
yulivee.neues_talent("Rechnen",                1)
yulivee.neues_talent("Rechtskunde",            1)
yulivee.neues_talent("Sagen/Legenden",         2)
yulivee.neues_talent("Schätzen",               4)
yulivee.neues_talent("Tierkunde",              1)
# Handwerk
yulivee.neues_talent("Bogenbau",               2)
yulivee.neues_talent("Fahrzeug lenken",        1)
yulivee.neues_talent("Hauswirtschaft",         1)
yulivee.neues_talent("Heilkunde Gift",         0)
yulivee.neues_talent("Heilkunde Wunden",       3)
yulivee.neues_talent("Holzbearbeitung",        4)
yulivee.neues_talent("Kochen",                 0)
yulivee.neues_talent("Lederarbeiten",          2)
yulivee.neues_talent("Malen/Zeichnen",         0)
yulivee.neues_talent("Schlösser knacken",      0)
yulivee.neues_talent("Schneidern",             1)
# }}}

## Gaben {{{
yulivee.neue_gabe("Gefahreninstinkt", 3)
# }}}

## globalisieren {{{
yulivee.aktiv()
# }}}
