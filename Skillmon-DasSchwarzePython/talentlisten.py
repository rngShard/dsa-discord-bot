import re
from . import ipop
from . import proben

basis_eigenschaften = ("mu","kl","in","ch","ff","ge","ko","kk")
erst = ("erste", "zweite", "dritte")

BEx2 = "Das Talent wird um die zweifache BE erschwert."
BEx1 = "Das Talent wird um die einfache BE erschwert."
def BE(inp,add="ein"):
    return "Das Talent wird um die %sfache BE%+d erschwert."%(add,inp)

class Talentliste(object):# {{{
    def __init__(self,namenUproben=False):
        if not namenUproben:
            self.namen     = []
            self.proben    = []
            self.kategorie = []
            self.anmerkung = []
        else:
            self.namen     = [ nUp[0] for nUp in namenUproben ]
            self.proben    = [ nUp[1] for nUp in namenUproben ]
            self.kategorie = [ (False if len(nUp) < 3 else nUp[2])
                    for nUp in namenUproben ]
            self.anmerkung = [ (False if len(nUp) < 4 else nUp[3])
                    for nUp in namenUproben ]
    def add(self,nameUprobe):
        self.namen.append(nameUprobe[0])
        self.proben.append(nameUprobe[1])
        if len(nameUprobe) < 3:
            self.kategorie.append(False)
            self.anmerkung.append(False)
        else:
            self.kategorie.append(nameUprobe[2])
            if len(nameUprobe) > 3: self.anmerkung.append(nameUprobe[3])
            else: self.anmerkung.append(False)
# }}}

class Suche(object):# {{{
    def talent(self,name):
        return self.suche(name,talentliste.namen)
    def talent_kategorie(self,name):
        return self.suche(name,talentliste.kategorie)
    def zauber(self,name):
        return self.suche(name,zauberliste.namen)
    def zauber_kategorie(self,name):
        return self.suche(name,talentliste.kategorie)
    def gabe(self,name):
        return self.suche(name,gabenliste.namen)
    def gabe_kategorie(self,name):
        return self.suche(name,gabenliste.kategorie)
    def suche(self,name,liste):
        pattern = re.compile(".*" + name + ".*",re.I)
        return [ i for i,l in enumerate(liste) if re.search(pattern,l) != None ]
# }}}

class Probe(object):# {{{
    def talent(self,name,stats,skill,harder=0,fullmatch=False):# {{{
        return self.probe(name, talentliste, stats, skill, "Welches", "Talent",
                harder=harder, fullmatch=fullmatch)
    # }}}
    def zauber(self,name,stats,skill,harder=0,fullmatch=False):# {{{
        return self.probe(name, zauberliste, stats, skill, "Welcher", "Zauber",
                harder=harder, fullmatch=fullmatch)
    # }}}
    def gabe(self,name,stats,skill,harder=0,fullmatch=False):# {{{
        return self.probe(name, gabenliste, stats, skill, "Welche", "Gabe",
                harder=harder, fullmatch=fullmatch)
    # }}}
    def probe(self,name,liste,stats,skill,welchers,talauber,harder=0,# {{{
            fullmatch=False):
        if fullmatch:
            if name not in liste.namen:
                print("'%s' nicht bekannt."%(name))
                return False
            entry = liste.namen.index(name)
        else:
            matches = suche.suche(name, liste.namen)
            if len(matches) == 0:
                print(talauber+" '%s' nicht bekannt."%(name))
                return False
            elif len(matches) != 1:
                if type(name) == str and len(name) > 0:
                    print("'%s' konnte nicht eindeutig ermittelt werden!"%(
                        name))
                print(welchers+" "+talauber+" ist gemeint?")
                entry = ipop.choice_from_list(matches, print_list=liste.namen)
            else: entry = matches[0]
        probe = self.proben_eigenschaften(liste.namen[entry], liste,
                fullmatch=True)
        if probe:
            harder = harder + probe[1]
            probe = probe[0]
        else: return False
        return proben.probe3(
                probe[0], probe[1], probe[2], harder=harder, skill=skill,
                stats=stats)
    # }}}
    def proben_eigenschaften(self, name, liste, fullmatch=False):# {{{
        if fullmatch:
            if name not in liste.namen:
                print("'%s' nicht bekannt."%(name))
                return False
            entry = liste.namen.index(name)
        else:
            matches = suche.suche(name, liste.namen)
            if len(matches) == 0:
                print("'%s' nicht bekannt."%(name))
                return False
            elif len(matches) != 1:
                if type(name) == str and len(name) > 0:
                    print("'%s' konnte nicht eindeutig ermittelt werden!"%(
                        name))
                print("Was ist gemeint?")
                entry = ipop.choice_from_list(matches, print_list=liste.namen)
            else: entry = matches[0]
        probe  = list(liste.proben[entry])
        harder = 0
        for i in range(min(len(probe),3)):
            if type(probe[i]) == list or type(probe[i]) == tuple:
                print("Die %s Eigenschaft der Probe scheint wählbar."%(
                    erst[i]))
                print("Welche Eigenschaft soll verwendet werden?")
                probe[i] = ipop.choice_from_list(probe[i])
        if len(probe) == 3: pass
        elif len(probe) == 4:# {{{
            if probe[3] == "+Mod":
                print("Die Probe kann von Modifikationen erschwert werden.")
                harder = harder + ipop.int_input("Zusätzliche Erschwernis? ")
            elif probe[3] == "+MR":
                print("Die Probe wird von der Magieresistenz des Ziels "
                        "erschwert.")
                harder = harder + ipop.int_input("Zusätzliche Erschwernis? ")
            elif probe[3] == "Eig":
                print("Die dritte Eigenschaft der Probe kann frei gewählt "
                    "werden.")
                print("Welche Eigenschaft soll verwendet werden?")
                probe[2] = ipop.choice_from_list(basis_eigenschaften)
            else:
                print("Kritischer Fehler in Talentlistenstruktur.")
                print("Das vierte Feld in 'Proben' hat eine unbekannte "
                        "Struktur.")
                return False
        # }}}
        elif len(probe) == 5:
            if probe[3] == True:
                print(probe[4])
                harder = harder + ipop.int_input("Zusätzliche Erschwernis? ")
            else:
                print("Kritischer Fehler in Talentlistenstruktur.")
                print("Das vierte Feld in 'Proben' hat eine unbekannte "
                        "Struktur.")
                return False
        elif len(probe) == 1:
            if type(probe[0]) == str:
                return self.proben_eigenschaften(probe[0], liste,
                        fullmatch=True)
            else:
                print("Kritischer Fehler in Talentlistenstruktur.")
                print("Das einzige Feld in 'Proben' ist kein String.")
                return False
        else:
            print("Kritischer Fehler in Talentlistenstruktur.")
            print("Das Feld 'Proben' hat weder 1, 3, 4 noch 5 Elemente.")
            return False
        return [probe[:3],harder]
    # }}}
# }}}

suche = Suche()
probe = Probe()

## Alle Zauber aus dem Liber Cantiones mit zugehörigen Proben
zauberliste = Talentliste(namenUproben=(# {{{
    ("Abvenenum reine Speise",              ("kl","kl","ff","+Mod"), "Objekt",
        "Kosten: 4 AsP (Sch. 3) pro Mahlzeit für 10 Pers."),
    ("Accuratum Zaubernadel",               ("kl","ch","ff","+Mod"), "Objekt",
        "Kosten: 4 AsP pro Stein Gewicht, min. 4"),
    ("Adamantium Erzstruktur",              ("kl","ff","ko",),
        "Objekt, Elementar (Erz)", "Kosten: 5 AsP +2 pro angef. Stein Gewicht"),
    ("Adlerauge Luchsenohr",                ("kl","in","ff",),
        "Hellsicht, Eigenschaft", "Kosten: 4 AsP"),
    ("Adlerschwinge Wolfsgestalt",          ("mu","in","ge","+Mod"), "Form",
        "Kosten: 4 AsP +2 AsP/SR bei amphib., +3 AsP/SR bei wasser. o. flieg."),
    ("Aeolitus Windgebraus",                ("kl","ch","ko",)),
    ("Aerofugo Vakuum",                     ("mu","ko","kk",)),
    ("Aerogelo Atemqual",                   ("mu","in","ko",)),
    ("Agrimothbann",                        ("Dämonenbann",)),
    ("Alpgestalt",                          ("mu","ch","ge","+MR")),
    ("Amazerothbann",                       ("Dämonenbann",)),
    ("Analys Arcanstruktur",                ("kl","kl","in","+Mod")),
    ("Ängste lindern",                      ("mu","in","ch",)),
    ("Animatio stummer Diener",             ("kl","ff","ge",)),
    ("Applicatus Zauberspeicher",           ("kl","ff","ff",)),
    ("Aquafaxius",                          ("Ignifaxius Flammenstrahl",)),
    ("Arachnea Krabbeltier",                ("mu","in","ch",)),
    ("Arcanovi Artefakt",                   ("kl","kl","ff",)),
    ("Armatrutz",                           ("in","ge","ko",)),
    ("Archofaxius",                         ("Ignifaxius Flammenstrahl",)),
    ("Atemnot",                             ("mu","ko","kk","+MR")),
    ("Attributo",                           ("kl","ch",basis_eigenschaften)),
    ("Aufgeblasen abgehoben",               ("ch","kk","ko","+MR")),
    ("Auge des Limbus",                     ("mu","ko","kk",)),
    ("Aureolus Güldenglanz",                ("in","ch","ff",)),
    ("Auris Nasus Oculus",                  ("kl","ch","ff",)),
    ("Axxeleratus blitzgeschwind",          ("kl","ge","ko",)),

    ("Balsam Salabunde",                    ("kl","in","ch","+Mod")),
    ("Band und Fessel",                     ("kl","ch","kk","+MR")),
    ("Bannbaladin",                         ("in","ch","ch","+MR")),
    ("Bärenruhe Winterschlaf",              ("mu","ko","kk","+Mod")),
    ("Beherrschung brechen",                ("kl","in","ch","+Mod")),
    ("Belhalharbann",                       ("Dämonenbann",)),
    ("Belzhorashbann",                      ("Dämonenbann",)),
    ("Beschwörung vereiteln",               ("mu","in","ch","+Mod")),
    ("Bewegung stören",                     ("kl","in","ff","+Mod")),
    ("Blakharazbann",                       ("Dämonenbann",)),
    ("Blendwerk",                           ("in","ch","ge",)),
    ("Blick aufs Wesen",                    ("kl","in","ch","+MR")),
    ("Blick durch fremde Augen",            ("mu","in","ch","+MR")),
    ("Blick in die Gedanken",               ("kl","kl","ch","+MR")),
    ("Blick in die Vergangenheit",          ("kl","kl","in","+Mod")),
    ("Blitz dich find",                     ("kl","in","ge","+MR")),
    ("Böser Blick",                         ("mu","ch","ch","+MR")),
    ("Brenne toter Stoff!",                 ("mu","kl","ko",)),

    ("Caldofrigo heiß und kalt",            ("in","ch","ko",)),
    ("Chamaelioni Mimikry",                 ("in","ch","ge",)),
    ("Chimaeroform Hybridgestalt",          ("kl","in","ko","+Mod")),
    ("Chronoklassis Urfossil",              ("kl","in","ko","+Mod")),
    ("Chrononautos Zeitenfahrt",            ("mu","ch","ko","+Mod")),
    ("Claudibus Clavistibor",               ("kl","ff","kk",)),
    ("Corpofesso Gliederschmerz",           ("kl","kk","kk","+MR")),
    ("Corpofrigo Kälteschock",              ("ch","ge","ko","+MR")),
    ("Cryptographo Zauberschrift",          ("kl","kl","in",)),
    ("Custodosigil Diebesbann",             ("kl","ff","ff",)),

    ("Dämonenbann",                         ("mu","ch","ko","+Mod")),
    ("Delicioso Gaumenschmaus",             ("kl","ch","ff",)),
    ("Desintegratus Pulverstaub",           ("kl","kk","ko",)),
    ("Destructibo Arcanitas",               ("kl","kl","ff","+Mod")),
    ("Dichter und Denker",                  ("kl","in","ch","+MR")),
    ("Dschinnenruf",                        ("mu","kl","ch","+Mod")),
    ("Dunkelheit",                          ("kl","kl","ff",)),
    ("Duplicatus Doppelbild",               ("kl","ch","ge",)),

    ("Ecliptifactus Schattenkraft",         ("mu","kl","ko",)),
    ("Eigensch. wiederherstellen",          ("kl","in","ch","+Mod")),
    ("Eigne Ängste quälen dich!",           ("mu","in","ch","+MR")),
    ("Einfluss bannen",                     ("in","ch","ch","+Mod")),
    ("Eins mit der Natur",                  ("in","ge","ko",)),
    ("Eisbann",                             ("Elementarbann",)),
    ("Eisenrost und Patina",                ("kl","ch","ge",)),
    ("Eiseskälte Kämpferherz",              ("mu","in","ko",)),
    ("Eiswirbel",                           ("Mahlstrom",)),
    ("Elementarbann",                       ("in","ch","ko","+Mod")),
    ("Elementarer Diener",                  ("mu","kl","ch","+Mod")),
    ("Elementarer Wirbel",                  ("Mahlstrom",)),
    ("Elfenstimme Flötenton",               ("in","ch","ko",)),
    ("Erinnerung verlasse dich!",           ("mu","in","ch","+MR")),
    ("Erzbann",                             ("Elementarbann",)),
    ("Exposami Lebenskraft",                ("kl","in","in",)),

    ("Falkenauge Meisterschuss",            ("in","ff","ge",)),
    ("Favilludo Funkentanz",                ("in","ch","ff",)),
    ("Feuerbann (I)",                       ("Elementarbann",)),
    ("Feuerbann (II)",                      ("Leib des Feuers",)),
    ("Feuersturm",                          ("Mahlstrom",)),
    ("Firnlauf",                            ("mu","kl","ge",)),
    ("Fledermausruf",                       ("Krähenruf",)),
    ("Flim Flam Funkel",                    ("kl","kl","ff",)),
    ("Fluch der Pestilenz",                 ("mu","kl","ch","+MR")),
    ("Foramen Foraminor",                   ("kk","kl","ff","+Mod")),
    ("Fortifex arkane Wand",                ("in","kk","ko",)),
    ("Frigifaxius",                         ("Ignifaxius Flammenstrahl",)),
    ("Frigosphaero",                        ("Ignisphaero Feuerball",)),
    ("Fulminictus Donnerkeil",              ("in","ge","ko",)),

    ("Gardianum Zauberschild",              ("kl","in","ko",)),
    ("Gedankenbilder Elfenruf",             ("kl","in","ch",)),
    ("Gefäß der Jahre",                     ("mu","kl","ko",)),
    ("Gefunden!",                           ("kl","in","ge","+Mod")),
    ("Geister beschwören",                  ("Geisterruf",)),
    ("Geisterbann",                         ("mu","mu","ch","+Mod")),
    ("Geisterruf",                          ("mu","mu","ch","+Mod")),
    ("Gletscherwand",                       ("Wand aus Dornen",)),
    ("Granit und Marmor",                   ("mu","ch","ko","+MR")),
    ("Große Gier",                          ("kl","kl","ch","+MR")),
    ("Große Verwirrung",                    ("kl","kl","ch","+MR")),

    ("Halluzination",                       ("kl","in","ch","+MR")),
    ("Harmlose Gestalt",                    ("kl","ch","ge",)),
    ("Hartes schmelze!",                    ("mu","kl","kk",)),
    ("Haselbusch und Ginsterkraut",         ("ch","ff","ko",)),
    ("Heilkraft bannen",                    ("kl","ch","ff","+Mod")),
    ("Hellsicht trüben",                    ("kl","in","ch","+MR")),
    ("Herbeirufung vereiteln",              ("mu","in","ch","+Mod")),
    ("Herr über das Tierreich",             ("mu","mu","ch","+MR")),
    ("Herzschlag ruhe!",                    ("mu","ch","kk","+MR")),
    ("Hexenblick",                          ("in","in","ch",)),
    ("Hexengalle",                          ("mu","in","ch",)),
    ("Hexenholz",                           ("kl","ff","kk",)),
    ("Hexenknoten",                         ("kl","in","ch",)),
    ("Hexenkrallen",                        ("mu","in","ko",)),
    ("Hexenspeichel",                       ("in","ch","ff",)),
    ("Hilfreiche Tatze, rettende Schwinge", ("mu","in","ch","+MR")),
    ("Höllenpein zerreiße dich!",           ("kl","ch","ko","+MR")),
    ("Holterdipolter",                      ("in","in","ff",)),
    ("Hornissenruf",                        ("Krähenruf",)),
    ("Horriphobus Schreckgestalt",          ("in","in","ff",)),
    ("Humofaxius",                          ("Ignifaxius Flammenstrahl",)),
    ("Humusbann",                           ("Elementarbann",)),

    ("Ignifaxius Flammenstrahl",            ("kl","ff","ko",)),
    ("Ignisphaero Feuerball",               ("kl","ff","ko",)),
    ("Ignorantia ungesehn",                 ("in","ch","ge",)),
    ("Illusion auflösen",                   ("kl","in","ch",)),
    ("Immortalis Lebenszeit",               ("mu","ch","ko",)),
    ("Imperavi Handlungszwang",             ("kl","ch","ch","+MR")),
    ("Impersona Maskenbild",                ("kl","in","ff",)),
    ("Infinitum Immerdar",                  ("kl","ch","ko","+Mod")),
    ("Invercano Spiegeltrick",              ("mu","in","ff",)),
    ("Invocatio maior",                     ("mu","mu","ch","+Mod")),
    ("Invocatio minor",                     ("mu","mu","ch","+Mod")),
    ("Iribaars Hand",                       ("mu","mu","in","+MR")),

    ("Juckreiz, dämlicher!",                ("mu","in","ch","+MR")),

    ("Karnifilo Raserei",                   ("mu","in","ch","+MR")),
    ("Katzenaugen",                         ("kl","ff","ko",)),
    ("Klarum Purum",                        ("kl","kl","ch","+Mod")),
    ("Klickeradomms",                       ("kl","ff","kk",)),
    ("Koboldgeschenk",                      ("in","ch","ff","+MR")),
    ("Koboldovision",                       ("mu","ch","ch",)),
    ("Komm Kobold komm",                    ("in","in","ch",)),
    ("Körperlose Reise",                    ("mu","kl","in",)),
    ("Krabbelnder Schrecken",               ("mu","mu","ch",)),
    ("Kraft des Erzes",                     ("kl","ko","kk",)),
    ("Krähenruf",                           ("mu","ch","ch",)),
    ("Krötensprung",                        ("in","ge","kk",)),
    ("Kulminatio Kugelblitz",               ("mu","in","ff",)),
    ("Kusch!",                              ("mu","in","ch","+MR")),

    ("Lach dich gesund",                    ("in","ch","ch",)),
    ("Lachkrampf",                          ("ch","ch","ff","+MR")),
    ("Langer Lulatsch",                     ("ch","ge","kk","+MR")),
    ("Last des Alters",                     ("in","ch","ko","+MR")),
    ("Leib der Erde",                       ("mu","in","ge",)),
    ("Leib der Wogen",                      ("mu","kl","ge",)),
    ("Leib des Eises",                      ("mu","kl","ge",)),
    ("Leib des Erzes",                      ("mu","ge","kk",)),
    ("Leib des Feuers",                     ("mu","mu","ge",)),
    ("Leib des Windes",                     ("mu","ge","kk",)),
    ("Leidensbote",                         ("Leidensbund",)),
    ("Leidensbund",                         ("mu","in","ko",)),
    ("Levthans Feuer",                      ("in","ch","ch","+MR")),
    ("Limbus versiegeln",                   ("kl","in","ko","+Mod")),
    ("Lockruf und Feenfüße",                ("in","ch","ff",)),
    ("Lolgramothbann",                      ("Dämonenbann",)),
    ("Luftbann",                            ("Elementarbann",)),
    ("Lunge des Leviatan",                  ("in","ch","ko",)),

    ("Madas Spiegel",                       ("mu","kl","in",)),
    ("Magischer Raub",                      ("mu","kl","ko","+MR")),
    ("Mahlstrom",                           ("mu","in","kk",)),
    ("Malmkreis",                           ("Mahlstrom",)),
    ("Manifesto Element",                   ("kl","in","ch","+Mod")),
    ("Meister der Elemente",                ("mu","kl","ch","+Mod")),
    ("Meister minderer Geister",            ("mu","ch","ch",)),
    ("Memorabia Falsifir",                  ("kl","in","ch","+Mod")),
    ("Memorans Gedächtniskraft",            ("kl","kl","in",)),
    ("Menetekel Flammenschrift",            ("kl","ch","ff",)),
    ("Metamagie neutralisieren",            ("kl","kl","ko","+Mod")),
    ("Metamorpho Gletscherform",            ("kl","ff","kk",)),
    ("Motoricus Geisteshand",               ("kl","ff","kk","+Mod")),
    ("Movimento Dauerlauf",                 ("in","ge","ko",)),
    ("Murks und Patz",                      ("in","in","ff","+Mod")),

    ("Nackedei",                            ("kl","in","ff","+Mod")),
    ("Nebelleib",                           ("mu","in","ko",)),
    ("Nebelwand und Morgendunst",           ("kl","ff","ko",)),
    ("Nekropathia Seelenreise",             ("mu","kl","ch",)),
    ("Niederhöllen Eisgestalt",             ("Granit und Marmor",)),
    ("Nihilogravo schwerelos",              ("kl","ko","kk",)),
    ("Nuntiovolo Botenvogel",               ("mu","kl","ch",)),

    ("Objecto Obscuro",                     ("kl","ff","ko",)),
    ("Objectofixo",                         ("kl","kl","kk",)),
    ("Objectovoco",                         ("kl","in","ch",)),
    ("Objekt entzaubern",                   ("kl","in","ff","+ Mod")),
    ("Oculus Astralis",                     ("kl","in","ch",)),
    ("Odem Arcanum",                        ("kl","in","in",)),
    ("Orcanofaxius",                        ("Ignifaxius Flammenstrahl",)),
    ("Orcanosphaero",                       ("Ignisphaero Feuerball",)),
    ("Orkanwand",                           ("Wand aus Dornen",)),

    ("Pandaemonium",                        ("mu","mu","ch",)),
    ("Panik überkomme euch!",               ("mu","ch","ch",)),
    ("Papperlapapp",                        ("in","in","ff","+MR")),
    ("Paralysis starr wie Stein",           ("in","ch","kk","+MR")),
    ("Pectetondo Zauberhaar",               ("kl","ch","ff",)),
    ("Penetrizzel Tiefenblick",             ("kl","kl","ko",)),
    ("Pentagramma Sphärenbann",             ("mu","mu","ch","+Mod")),
    ("Pestilenz erspüren",                  ("kl","in","ch","+Stufe")),
    ("Pfeil des [Elements]",                ("kl","in","ch",)),
    ("Planastrale Anderwelt",               ("mu","mu","ko",)),
    ("Plumbumbarum schwerer Arm",           ("ch","ge","kk","+MR")),
    ("Projektimago Ebenbild",               ("mu","in","ch","+Mod")),
    ("Protectionis Kontrabann",             ("kl","ch","ko",)),
    ("Psychostabilis",                      ("mu","kl","ko",)),

    ("Radau",                               ("mu","ch","ko",)),
    ("Reflectimago Spiegelschein",          ("kl","ch","ff",)),
    ("Reptilea Natternnest",                ("mu","in","ch",)),
    ("Respondami Wahrheitszwang",           ("mu","in","ch","+MR")),
    ("Reversalis Revidum",                  ("kl","in","ch",)),
    ("Ruhe Körper, ruhe Geist",             ("kl","ch","ko",)),

    ("Salander Mutander",                   ("kl","ch","ko","+MR")),
    ("Sanftmut",                            ("mu","ch","ch","+MR")),
    ("Sapefacta Zauberschwamm",             ("kl","ch","ff",)),
    ("Saturias Herrlichkeit",               ("in","ch","ch",)),
    ("Schabernack",                         ("kl","in","ch","+MR")),
    ("Schadenszauber bannen",               ("mu","in","ko","+Mod")),
    ("Schelmenkleister",                    ("in","ff","ge",)),
    ("Schelmenlaune",                       ("mu","in","ch","+Mod")),
    ("Schelmenmaske",                       ("in","ch","ge",)),
    ("Schelmenrausch",                      ("in","ch","ch","+MR")),
    ("Schlangenruf",                        ("Krähenruf",)),
    ("Schleier der Unwissenheit",           ("kl","kl","ff",)),
    ("Schwarz und Rot",                     ("mu","ch","ko","+MR")),
    ("Schwarzer Schrecken",                 ("mu","in","ch","+MR")),
    ("Seelenfeuer lichterloh",              ("Granit und Marmor",)),
    ("Seelentier erkennen",                 ("in","in","ch","+MR")),
    ("Seelenwanderung",                     ("mu","ch","ko",)),
    ("Seidenweich schuppengleich",          ("in","ff","ff",)),
    ("Seidenzunge Elfenwort",               ("kl","in","ch","+MR")),
    ("Sensattacco Meisterstreich",          ("mu","in","ge",)),
    ("Sensibar Empathicus",                 ("kl","in","ch","+MR")),
    ("Serpentialis Schlangenleib",          ("mu","ch","ge",)),
    ("Silentium Schweigekreis",             ("kl","in","ch",)),
    ("Sinesigil unerkannt",                 ("kl","in","ff",)),
    ("Skelettarius Totenheer",              ("mu","mu","ch","+Mod")),
    ("Solidirid Weg aus Licht",             ("in","ko","kk",)),
    ("Somnigravis tiefer Schlaf",           ("kl","ch","ch","+MR")),
    ("Spinnenlauf",                         ("in","ge","kk",)),
    ("Spinnenruf",                          ("Krähenruf",)),
    ("Spurlos trittlos",                    ("in","ge","ge",)),
    ("Standfest Katzengleich",              ("in","ff","ge",)),
    ("Staub wandle!",                       ("mu","kl","ch","+Mod")),
    ("Stein wandle!",                       ("mu","ch","kk","+Mod")),
    ("Stillstand",                          ("mu","in","ge",)),
    ("Sumpfstrudel",                        ("Mahlstrom",)),
    ("Sumus Elixiere",                      ("in","ch","ff",)),

    ("Tauschrausch",                        ("in","ff","ko",)),
    ("Tempus Stasis",                       ("mu","kl","kk","+Mod")),
    ("Thargunitothbann",                    ("Dämonenbann",)),
    ("Tiere besprechen",                    ("mu","in","ch","+Mod")),
    ("Tiergedanken",                        ("mu","in","ch","+MR")),
    ("Tlalucs Odem Pestgestank",            ("mu","in","ge",)),
    ("Totes handle!",                       ("mu","ch","ko",)),
    ("Transformatio Formgestalt",           ("kl","ff","kk","+Mod")),
    ("Transmutare Körperform",              ("ch","ge","ko","+MR")),
    ("Transversalis Teleport",              ("kl","in","ko",)),
    ("Traumgestalt",                        ("in","ch","ch","+MR")),

    ("Unberührt von Satinav",               ("kl","ff","ko","+Mod")),
    ("Unitatio Geistesbund",                ("in","ch","ko",)),
    ("Unsichtbarer Jäger",                  ("in","ff","ge",)),

    ("Valetudo Lebenskraft",                ("Fulminictus Donnerkeil",)),
    ("Veränderung aufheben",                ("kl","in","ko","+Mod")),
    ("Verschwindibus",                      ("in","ch","ge",)),
    ("Verständigung stören",                ("kl","kl","in","+MR")),
    ("Verwandlung beenden",                 ("kl","ch","ff","+Mod")),
    ("Vipernblick",                         ("mu","mu","ch","+MR")),
    ("Visibili Vanitar",                    ("kl","in","ge",)),
    ("Vocolimbo hohler Klang",              ("kl","ch","ff",)),
    ("Vogelzwitschern Glockenspiel",        ("mu","in","ge",)),

    ("Wand aus Flammen",                    ("Wand aus Dornen",)),
    ("Wand aus [Element]",                  ("Wand aus Dornen",)),
    ("Wand aus Dornen",                     ("mu","kl","ch",)),
    ("Wand aus Erz",                        ("Wand aus Dornen",)),
    ("Warmes Blut",                         ("mu","in","in",)),
    ("Wasseratem",                          ("mu","kl","ko",)),
    ("Wasserbann",                          ("Elementarbann",)),
    ("Wasserwand",                          ("Wand aus Dornen",)),
    ("Weiches erstarre!",                   ("mu","kl","kk",)),
    ("Weihrauchwolke Wohlgeruch",           ("in","ch","ff",)),
    ("Weisheit der Bäume",                  ("mu","in","ko","+Mod")),
    ("Weiße Mähn und goldner Huf",          ("kl","in","ch",)),
    ("Wellenlauf",                          ("mu","ge","ge",)),
    ("Wettermeisterschaft",                 ("mu","ch","ge","+Mod")),
    ("Widerwille Ungemach",                 ("mu","in","ge",)),
    ("Windhose",                            ("mu","in","kk",)),
    ("Windstille",                          ("kl","ch","kk","+Mod")),
    ("Wipfellauf",                          ("mu","in","ge",)),

    ("Xenographus Schriftenkunde",          ("kl","kl","in",)),

    ("Zagibu Ubigaz",                       ("in","ch","ff",)),
    ("Zappenduster",                        ("in","in","ff",)),
    ("Zauberklinge Geisterspeer",           ("kl","ff","ko",)),
    ("Zaubernahrung Hungerbann",            ("mu","mu","ko","+Mod")),
    ("Zauberwesen der Natur",               ("mu","in","ch",)),
    ("Zauberzwang",                         ("mu","ch","ch","+MR")),
    ("Zorn der Elemente",                   ("mu","ch","ko",)),
    ("Zunge lähmen",                        ("mu","ch","ff","+MR")),
    ("Zwang zur Wahrheit",                  ("Respondami Wahrheitszwang",)),
    ("Zwingtanz",                           ("mu","kl","ch","+MR")),
    ))# }}}

## Alle Talente aus Wege der Helden ab Seite 315 mit zugehörigen Proben
talentliste = Talentliste(namenUproben=(# {{{
    ("Akrobatik",               ("mu","ge","kk",True,BEx2),   "körperlich"),
    ("Athletik",                ("ge","ko","kk",True,BEx2),   "körperlich"),
    ("Fliegen",                 ("mu","in","ge",True,BEx1),   "körperlich"),
    ("Gaukeleien",              ("mu","ch","ff",True,BEx2),   "körperlich"),
    ("Klettern",                ("mu","ge","kk",True,BEx2),   "körperlich"),
    ("Körperbeherrschung",      ("mu","in","ge",True,BEx2),   "körperlich"),
    ("Reiten",                  ("ch","ge","kk",True,BE(-2)), "körperlich"),
    ("Schleichen",              ("mu","in","ge",True,BEx1),   "körperlich"),
    ("Schwimmen",               ("ge","ko","kk",True,BEx2),   "körperlich"),
    ("Selbstbeherrschung",      ("mu","ko","kk"),             "körperlich"),
    ("Sich Verstecken",         ("mu","in","ge",True,BE(-2)), "körperlich"),
    ("Singen",                  ("in","ch",("ch","ko"),True,BE(-3)),"körperlich"),
    ("Sinnenschärfe",           ("kl","in",("in","ff")),      "körperlich"),
    ("Skifahren",               ("ge","ge","ko",True,BE(-2)), "körperlich"),
    ("Stimmen Imitieren",       ("kl","in","ch",True,BE(-4)), "körperlich"),
    ("Tanzen",                  ("ch","ge","ge",True,BEx2),   "körperlich"),
    ("Taschendiebstahl",        ("mu","in","ff",True,BEx2),   "körperlich"),
    ("Zechen",                  ("in","ko","kk"),             "körperlich"),

    ("Betören",                 ("in","ch","ch"),       "gesellschaftlich"),
    ("Etikette",                ("kl","in","ch"),       "gesellschaftlich"),
    ("Gassenwissen",            ("kl","in","ch"),       "gesellschaftlich"),
    ("Lehren",                  ("kl","in","ch"),       "gesellschaftlich"),
    ("Menschenkenntnis",        ("kl","in","ch"),       "gesellschaftlich"),
    ("Schauspielerei",          ("mu","kl","ch"),       "gesellschaftlich"),
    ("Schriftlicher Ausdruck",  ("kl","in","in"),       "gesellschaftlich"),
    ("Sich Verkleiden",         ("mu","ch","ge"),       "gesellschaftlich"),
    ("Überreden",               ("mu","in","ch"),       "gesellschaftlich"),
    ("Überzeugen",              ("kl","in","ch"),       "gesellschaftlich"),

    ("Fährtensuchen",           ("kl","in",("in","ko")),    "Natur"),
    ("Fallenstellen",           ("kl","ff","kk"),           "Natur"),
    # ("Fallen stellen",          ("kl","ff","kk"),           "Natur"),
    ("Fesseln/Entfesseln",      ("ff","ge","kk"),           "Natur"),
    ("Fischen/Angeln",          ("in","ff","kk"),           "Natur"),
    ("Orientierung",            ("kl","in","in"),           "Natur"),
    ("Wettervorhersage",        ("kl","in","in"),           "Natur"),
    ("Wildnisleben",            ("in","ge","ko"),           "Natur"),

    ("Anatomie",                ("mu","kl","ff"),       "Wissen"),
    ("Baukunst",                ("kl","kl","ff"),       "Wissen"),
    ("Brett-/Kartenspiel",      ("kl","kl","in"),       "Wissen"),
    ("Geografie",               ("kl","kl","in"),       "Wissen"),
    ("Geschichtswissen",        ("kl","kl","in"),       "Wissen"),
    ("Gesteinskunde",           ("kl","in","ff"),       "Wissen"),
    ("Götter/Kulte",            ("kl","kl","in"),       "Wissen"),
    ("Heraldik",                ("kl","kl","ff"),       "Wissen"),
    ("Hüttenkunde",             ("kl","in","ko"),       "Wissen"),
    ("Kriegskunst",             ("mu","kl","ch"),       "Wissen"),
    ("Kryptographie",           ("kl","kl","in"),       "Wissen"),
    ("Magiekunde",              ("kl","kl","in"),       "Wissen"),
    ("Mechanik",                ("kl","kl","ff"),       "Wissen"),
    ("Pflanzenkunde",           ("kl","in","ff"),       "Wissen"),
    ("Philosophie",             ("kl","kl","in"),       "Wissen"),
    ("Rechnen",                 ("kl","kl","in"),       "Wissen"),
    ("Rechtskunde",             ("kl","kl","in"),       "Wissen"),
    ("Sagen/Legenden",          ("kl","in","ch"),       "Wissen"),
    ("Schätzen",                ("kl","in","in"),       "Wissen"),
    ("Sprachenkunde",           ("kl","kl","in"),       "Wissen"),
    ("Staatskunst",             ("kl","in","ch"),       "Wissen"),
    ("Sternkunde",              ("kl","kl","in"),       "Wissen"),
    ("Tierkunde",               ("mu","kl","in"),       "Wissen"),

    ("Sprache",                    ("kl","in","ch"),    "Sprachen & Schriften"),
    ("Alaani",                     ("Sprache",),        "Sprachen & Schriften"),
    ("Asdharia (Sprache)",         ("Sprache",),        "Sprachen & Schriften"),
    ("Atak",                       ("Sprache",),        "Sprachen & Schriften"),
    ("Bosparano",                  ("Sprache",),        "Sprachen & Schriften"),
    ("Füchsisch",                  ("Sprache",),        "Sprachen & Schriften"),
    ("Garethi",                    ("Sprache",),        "Sprachen & Schriften"),
    ("Goblinisch",                 ("Sprache",),        "Sprachen & Schriften"),
    ("Isdira (Sprache)",           ("Sprache",),        "Sprachen & Schriften"),
    ("Mohisch",                    ("Sprache",),        "Sprachen & Schriften"),
    ("Nujuka",                     ("Sprache",),        "Sprachen & Schriften"),
    ("Oloarkh",                    ("Sprache",),        "Sprachen & Schriften"),
    ("Ologhaijan",                 ("Sprache",),        "Sprachen & Schriften"),
    ("Orkisch",                    ("Sprache",),        "Sprachen & Schriften"),
    ("Rogolan (Sprache)",          ("Sprache",),        "Sprachen & Schriften"),
    ("Rssahh",                     ("Sprache",),        "Sprachen & Schriften"),
    ("Thorwalsch",                 ("Sprache",),        "Sprachen & Schriften"),
    ("Tulamidya (Sprache)",        ("Sprache",),        "Sprachen & Schriften"),
    ("Ur-Tulamidya (Sprache)",     ("Sprache",),        "Sprachen & Schriften"),
    ("Zhayad",                     ("Sprache",),        "Sprachen & Schriften"),

    ("Schrift",                    ("kl","kl","ff"),    "Sprachen & Schriften"),
    ("Asdharia (Schrift)",         ("Schrift",),        "Sprachen & Schriften"),
    ("Chrmk",                      ("Schrift",),        "Sprachen & Schriften"),
    ("Geheilgte Glyphen von Unau", ("Schrift",),        "Sprachen & Schriften"),
    ("Hjaldingsche Runen",         ("Schrift",),        "Sprachen & Schriften"),
    ("Isdira (Schrift)",           ("Schrift",),        "Sprachen & Schriften"),
    ("Kusliker Zeichen",           ("Schrift",),        "Sprachen & Schriften"),
    ("Nanduria",                   ("Schrift",),        "Sprachen & Schriften"),
    ("Rogolan (Schrift)",          ("Schrift",),        "Sprachen & Schriften"),
    ("Tulamidya (Schrift)",        ("Schrift",),        "Sprachen & Schriften"),
    ("Ur-Tulamidya (Schrift)",     ("Schrift",),        "Sprachen & Schriften"),
    ("Zhayad",                     ("Schrift",),        "Sprachen & Schriften"),

    ("Abrichten",               ("mu","in","ch"),       "Handwerk"),
    ("Ackerbau",                ("in","ff","ko"),       "Handwerk"),
    ("Alchimie",                ("mu","kl","ff"),       "Handwerk"),
    ("Bergbau",                 ("in","ko","kk"),       "Handwerk"),
    ("Bogenbau",                ("kl","in","ff"),       "Handwerk"),
    ("Boote Fahren",            ("ge","ko","kk"),       "Handwerk"),
    ("Brauer",                  ("kl","ff","kk"),       "Handwerk"),
    ("Drucker",                 ("kl","ff","kk"),       "Handwerk"),
    ("Fahrzeug Lenken",         ("in","ch","ff"),       "Handwerk"),
    ("Falschspiel",             ("mu","ch","ff"),       "Handwerk"),
    ("Feinmechanik",            ("kl","ff","ff"),       "Handwerk"),
    ("Feuersteinbearbeitung",   ("kl","ff","ff"),       "Handwerk"),
    ("Fleischer",               ("kl","ff","kk"),       "Handwerk"),
    ("Gerber/Kürschner",        ("kl","ff","ko"),       "Handwerk"),
    ("Glaskunst",               ("ff","ff","ko"),       "Handwerk"),
    ("Grobschmied",             ("ff","ko","kk"),       "Handwerk"),
    ("Handel",                  ("kl","in","ch"),       "Handwerk"),
    ("Hauswirtschaft",          ("in","ch","ff"),       "Handwerk"),
    ("Heilkunde Gift",          ("mu","kl","in"),       "Handwerk"),
    ("Heilkunde Krankheiten",   ("mu","kl","ch"),       "Handwerk"),
    ("Heilkunde Seele",         ("in","ch","ch"),       "Handwerk"),
    ("Heilkunde Wunden",        ("kl","ch","ff"),       "Handwerk"),
    ("Holzbearbeitung",         ("kl","ff","kk"),       "Handwerk"),
    ("Instrumentenbauer",       ("kl","in","ff"),       "Handwerk"),
    ("Kartographie",            ("kl","kl","ff"),       "Handwerk"),
    ("Kochen",                  ("kl","in","ff"),       "Handwerk"),
    ("Kristallzucht",           ("kl","in","ff"),       "Handwerk"),
    ("Lederarbeiten",           ("kl","ff","ff"),       "Handwerk"),
    ("Malen/Zeichnen",          ("kl","in","ff"),       "Handwerk"),
    ("Maurer",                  ("ff","ge","kk"),       "Handwerk"),
    ("Metallguss",              ("kl","ff","kk"),       "Handwerk"),
    ("Musizieren",              ("in","ch","ff"),       "Handwerk"),
    ("Schlösser Knacken",       ("in","ff","ff"),       "Handwerk"),
    ("Schnaps Brennen",         ("kl","in","ff"),       "Handwerk"),
    ("Schneidern",              ("kl","ff","ff"),       "Handwerk"),
    ("Seefahrt",                ("ff","ge","kk"),       "Handwerk"),
    ("Seiler",                  ("ff","ff","kk"),       "Handwerk"),
    ("Steinmetz",               ("ff","ff","kk"),       "Handwerk"),
    ("Steinschneider/Juwelier", ("in","ff","ff"),       "Handwerk"),
    ("Stellmacher",             ("kl","ff","kk"),       "Handwerk"),
    ("Stoffe Färben",           ("kl","ff","kk"),       "Handwerk"),
    ("Tätowieren",              ("in","ff","ff"),       "Handwerk"),
    ("Töpfern",                 ("kl","ff","ff"),       "Handwerk"),
    ("Viehzucht",               ("kl","in","kk"),       "Handwerk"),
    ("Webkunst",                ("ff","ff","kk"),       "Handwerk"),
    ("Winzer",                  ("kl","ff","kk"),       "Handwerk"),
    ("Zimmermann",              ("kl","ff","kk"),       "Handwerk"),
    ))# }}}

## Gaben mit zugehörigen Proben
gabenliste = Talentliste(namenUproben=(# {{{
    ("Empathie",                ("mu","in","in"),       "Gaben"),
    ("Gefahreninstinkt",        ("kl","in","in"),       "Gaben"),
    ("Geräuschhexerei",         ("in","ch","ko"),       "Gaben"),
    ("Kräfteschub",             ("mu","in","ko"),       "Gaben"),
    ("Magiegespür",             ("mu","in","in"),       "Gaben"),
    ("Prophezeien",             ("in","in","ch"),       "Gaben"),
    ("Talentschub",             ("mu","in","ko"),       "Gaben"),
    ("Tierempathie",            ("mu","in","ch"),       "Gaben"),
    ("Zwergennase",             ("ff","in","in"),       "Gaben"),
    ))# }}}
