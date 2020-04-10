from ..proben import *
from ..held import *

# Meljow initialisieren
witzbold = Held("Der Witzbold, der bin ich", "Witzbold")

## Basiseigenschaften {{{
witzbold.eigenschaften.basis = \
        {"mu":14,"kl":12,"in":13,"ch":14,"ff":13,"ge":12,"ko":11,"kk":11}
# }}}

## Zauber {{{
witzbold.neuer_zauber("Aufgeblasen Abgehoben",2)
witzbold.neuer_zauber("Blendwerk",7)
witzbold.neuer_zauber("Blitz dich find",4)
witzbold.neuer_zauber("Klickeradomms",5)
witzbold.neuer_zauber("Koboldgeschenk",6)
witzbold.neuer_zauber("Komm Kobold komm",7)
witzbold.neuer_zauber("Lach dich gesund",4)
witzbold.neuer_zauber("Lachkrampf",6)
witzbold.neuer_zauber("Lockruf und Feenfüße",3)
witzbold.neuer_zauber("Meister minderer Geister",5)
witzbold.neuer_zauber("Motoricus",2)
witzbold.neuer_zauber("Nackedei",6)
witzbold.neuer_zauber("Penetrizzel Tiefenblick",0)
witzbold.neuer_zauber("Schabernack",6)
witzbold.neuer_zauber("Schelmenmaske",3)
witzbold.neuer_zauber("Tauschrausch",3)
witzbold.neuer_zauber("Verschwindibus",5)
witzbold.neuer_zauber("Zagibu Ubigaz",3)
# }}}

## Talente {{{
witzbold.neues_talent("Akrobatik",5)
witzbold.neues_talent("Athletik",0)
witzbold.neues_talent("Gaukeleien",5)
witzbold.neues_talent("Klettern",4)
witzbold.neues_talent("Körperbeherrschung",4)
witzbold.neues_talent("Schleichen",3)
witzbold.neues_talent("Schwimmen",0)
witzbold.neues_talent("Selbstbeherrschung",2)
witzbold.neues_talent("Sich Verstecken",5)
witzbold.neues_talent("Singen",2)
witzbold.neues_talent("Sinnenschärfe",0)
witzbold.neues_talent("Stimmen imitieren",7)
witzbold.neues_talent("Tanzen",2)
witzbold.neues_talent("Zechen",1)
witzbold.neues_talent("Etikette",1)
witzbold.neues_talent("Gassenwissen",1)
witzbold.neues_talent("Menschenkenntnis",1)
witzbold.neues_talent("Sich Verkleiden",4)
witzbold.neues_talent("Überreden",7)
witzbold.neues_talent("Fährtensuchen",0)
witzbold.neues_talent("Fesseln/Entfesseln",2)
witzbold.neues_talent("Orientierung",0)
witzbold.neues_talent("Wildnisleben",1)
witzbold.neues_talent("Götter/Kulte",2)
witzbold.neues_talent("Heraldik",1)
witzbold.neues_talent("Rechnen",1)
witzbold.neues_talent("Rechtskunde",1)
witzbold.neues_talent("Sagen/Legenden",5)
witzbold.neues_talent("Tierkunde",4)
witzbold.neues_talent("Falschspiel",2)
witzbold.neues_talent("Hauswirtschaft",1)
witzbold.neues_talent("Heilkunde Wunden",1)
witzbold.neues_talent("Holzbearbeitung",0)
witzbold.neues_talent("Kochen",0)
witzbold.neues_talent("Lederarbeiten",0)
witzbold.neues_talent("Malen/Zeichnen",4)
witzbold.neues_talent("Musizieren",3)
witzbold.neues_talent("Schlösser Knacken",3)
witzbold.neues_talent("Schneidern",1)
# }}}

## Gaben {{{
witzbold.neue_gabe("Geräuschhexerei", 3)
# }}}

## globalisieren {{{
witzbold.aktiv()
# }}}
