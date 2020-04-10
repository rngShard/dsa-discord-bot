from ..proben import *
from ..held import *

# shaya initialisieren
shaya = Held("Shaya Lovara", "Shaya")

## Basiseigenschaften {{{
shaya.eigenschaften.basis = \
        {"mu":11,"kl":14,"in":14,"ch":13,"ff":14,"ge":13,"ko":11,"kk":11}
# }}}

## Talente {{{
# Körper
shaya.neues_talent("Akrobatik",              3)
shaya.neues_talent("Athletik",               2)
shaya.neues_talent("Gaukeleien",             2)
shaya.neues_talent("Klettern",               1)
shaya.neues_talent("Körperbeherrschung",     3)
shaya.neues_talent("Schleichen",             4)
shaya.neues_talent("Schwimmen",              0)
shaya.neues_talent("Selbstbeherrschung",     3)
shaya.neues_talent("Sich Verstecken",        4)
shaya.neues_talent("Singen",                 1)
shaya.neues_talent("Sinnenschärfe",          3)
shaya.neues_talent("Tanzen",                 4)
shaya.neues_talent("Taschendiebstahl",       4)
shaya.neues_talent("Zechen",                 3)
# Gesellschaft
shaya.neues_talent("Betören",                9)
shaya.neues_talent("Etikette",               4)
shaya.neues_talent("Gassenwissen",           4)
shaya.neues_talent("Menschenkenntnis",       7)
shaya.neues_talent("Sich Verkleiden",        5)
shaya.neues_talent("Überreden",              7)
# Natur
shaya.neues_talent("Fährtensuche",           2)
shaya.neues_talent("Orientierung",           2)
shaya.neues_talent("Wildnisleben",           2)
# Wissen
shaya.neues_talent("Brett-/Kartenspiel",     6)
shaya.neues_talent("Geografie",              1)
shaya.neues_talent("Götter/Kulte",           1)
shaya.neues_talent("Magiekunde",             0)
shaya.neues_talent("Rechnen",                5)
shaya.neues_talent("Sagen/Legenden",         4)
shaya.neues_talent("Schätzen",               5)
shaya.neues_talent("Sternkunde",             1)
# Sprachen
shaya.neues_talent("Atak",                   4)
shaya.neues_talent("Füchsisch",              4)
shaya.neues_talent("Garethi",               10)
shaya.neues_talent("Tulamidya (Sprache)",   12, fullmatch=True)
# Schriften
shaya.neues_talent("Tulamidya (Schrift)",    0, fullmatch=True)
# Handwerk
shaya.neues_talent("Fahrzeug lenken",        2)
shaya.neues_talent("Falschspiel",           10)
shaya.neues_talent("Heilkunde Wunden",       1)
shaya.neues_talent("Holzbearbeitung",        1)
shaya.neues_talent("Kochen",                 1)
shaya.neues_talent("Lederarbeiten",          1)
shaya.neues_talent("Malen/Zeichnen",         0)
shaya.neues_talent("Schlösser knacken",      5)
shaya.neues_talent("Schneidern",             1)
# }}}

## Gaben {{{
shaya.neue_gabe("Gefahreninstinkt", 4)
# }}}

## globalisieren {{{
shaya.aktiv()
# }}}
