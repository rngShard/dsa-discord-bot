import xml.etree.ElementTree as ET # xml parsing
import re
from . import ipop
from . import proben
from . import talentlisten as talente

msg_endung_welche = {# {{{
        "Gabe"   : "",
        "Talent" : "s",
        "Zauber" : "r",
        }# }}}
msg_endung_kein   = {# {{{
        "Gabe"   : "e",
        "Talent" : "",
        "Zauber" : "en",
        }# }}}
# msg_endung_plural = {# {{{
        # "Gabe"   : "n",
        # "Talent" : "e",
        # "Zauber" : "",
        # }# }}}

class Zauber(object):# {{{
    def __init__(self,probe,ZfW,name=False):
        self.name  = name
        self.probe = probe
        self.skill = ZfW
#}}}

class Talent(object):# {{{
    def __init__(self,probe,TaW,name=False):
        self.name  = name
        self.probe = probe
        self.skill = TaW
#}}}

class Gabe(object):# {{{
    def __init__(self,probe,TaW,name=False):
        self.name  = name
        self.probe = probe
        self.skill = TaW
#}}}

class Held(object):# {{{
    def __init__(self, name=None, spitzname=None):# {{{
        self.name = name
        self.spitzname = spitzname
        self.eigenschaften = self.Eigenschaften()
        self.asp = self.Eig_mods()
        self.aup = self.Eig_mods()
        self.kap = self.Eig_mods()
        self.lep = self.Eig_mods()
        self.mr  = self.Eig_mods()
    # }}}
    class Eig_mods(object):
        def __init__(self):
            self.modifikator = 0
            self.perma_minus = 0
            self.perma_plus  = 0
            self.zugekauft   = 0
        def set(self,mod=False,minus=False,plus=False,zug=False):
            if mod != False:    self.modifikator = mod
            if minus != False:  self.perma_minus = minus
            if plus  != False:  self.perma_plus  = plus
            if zug    != False: self.zugekauft   = zug
    class Eigenschaften(object):# {{{
        def __init__(self):
            self.basis = {
                    "mu":0,"kl":0,"in":0,"ch":0,"ff":0,"ge":0,"ko":0,"kk":0 }
            self.zauber  = {}
            self.talente = {}
            self.gaben   = {}
    # }}}
    def zauber(self, name='', harder=0):# {{{
        return ipop.trywrap(self._skill_probe,(name, talente.suche.zauber,
                talente.zauberliste.namen, self.eigenschaften.zauber, "Zauber",
                talente.probe.zauber, harder))
    # }}}
    def talent(self, name='', harder=0):# {{{
        return ipop.trywrap(self._skill_probe,(name, talente.suche.talent,
                talente.talentliste.namen, self.eigenschaften.talente, "Talent",
                talente.probe.talent, harder))
    # }}}
    def gabe(self, name='', harder=0):# {{{
        return ipop.trywrap(self._skill_probe,(name, talente.suche.gabe,
                talente.gabenliste.namen, self.eigenschaften.gaben, "Gabe",
                talente.probe.gabe, harder))
    # }}}
    def _skill_probe(self, name, suche, talentliste, bekannt, talauber,# {{{
            probe, harder=0):
        name = self._suche(name, suche, talentliste, bekannt, talauber)
        if name == -1: return -1
        print("Würfle Probe auf '%s'"%(name))
        skill = bekannt[name].skill
        stats = self.eigenschaften.basis
        return probe(name, stats, skill, harder=harder, fullmatch=True)
    # }}}
    def probe(self, st, harder=0, skill=0, silent=False, nonstop=False):# {{{
        return ipop.trywrap(proben.probe,(
                st, harder, skill, silent, nonstop, self.eigenschaften.basis))
    # }}}
    def neues_talent(self, name, TaW, fullmatch=False):# {{{
        return ipop.trywrap(self._neuer_skill,(name, TaW, talente.suche.talent,
                talente.talentliste, self.eigenschaften.talente, "Talent",
                Talent, fullmatch))
    # }}}
    def neuer_zauber(self, name, ZfW, fullmatch=False):# {{{
        return ipop.trywrap(self._neuer_skill,(name, ZfW, talente.suche.zauber,
                talente.zauberliste, self.eigenschaften.zauber, "Zauber",
                Zauber, fullmatch))
    # }}}
    def neue_gabe(self, name, TaW, fullmatch=False):# {{{
        return ipop.trywrap(self._neuer_skill,(name, TaW, talente.suche.gabe,
                talente.gabenliste, self.eigenschaften.gaben, "Gabe",
                Gabe, fullmatch))
    # }}}
    def _neuer_skill(self, name, skill, suche, talentliste, bekannt,# {{{
            talauber, Talauber, fullmatch=False):
        if fullmatch:
            if name not in talentliste.namen:
                print(talauber+" '%s' nicht bekannt."%(name))
                return False
            entry = talentliste.namen.index(name)
        else:
            matches = suche(name)
            if len(matches) == 0:
                print(talauber+" '%s' nicht bekannt."%(name))
                return False
            elif len(matches) != 1:
                print("'%s' konnte nicht eindeutig ermittelt werden!"%(name))
                print("Welche%s %s ist gemeint?"%(
                    msg_endung_welche[talauber], talauber))
                entry = ipop.choice_from_list(matches,
                        print_list=talentliste.namen)
            else: entry = matches[0]
        name = talentliste.namen[entry]
        if name in bekannt:
            print(talauber+" bereits bekannt.")
            return False
        probe = talentliste.proben[entry]
        bekannt[name] = Talauber(probe, skill, name=name)
        return True
    # }}}
    def liste_talente(self, name=False, probe=True):# {{{
        return ipop.trywrap(self._liste_skills,
                (self.eigenschaften.talente.items(), "Talent", name, probe))
    # }}}
    def liste_zauber(self, name=False, probe=True):# {{{
        return ipop.trywrap(self._liste_skills,
                (self.eigenschaften.zauber.items(), "Zauber", name, probe))
    # }}}
    def liste_gaben(self, name=False, probe=True):# {{{
        return ipop.trywrap(self._liste_skills,
                (self.eigenschaften.gaben.items(), "Gabe", name, probe))
    # }}}
    def _liste_skills(self, liste, talauber, name=False, probe=True):# {{{
        if len(liste) == 0:
            self._kein_talent(talauber)
            return -1
        l = 0
        if name:
            pattern = re.compile(".*" + name + ".*",re.I)
            matches = [ (k, v) for k, v in liste
                    if re.search(pattern, k) != None ]
            if len(matches) == 0:
                self._print_name()
                print(" kennt %s '%s' nicht!"%(talauber, name))
                return -1
        else: matches = liste
        for k, v in matches:
            l = max(l,len(k))
        for k, v in matches:
            print(k,end="")
            for i in range(l - len(k)):
                print(" ",end="")
            print("  ",end="")
            print("%2d"%(v.skill),end="")
            if probe:
                print("    ",end="")
                print(v.probe,end="")
            print("")
    # }}}
    def chance_zauber(self,name='',harder=0):# {{{
        return ipop.trywrap(self._chance,(name, talente.suche.zauber,
                talente.zauberliste, self.eigenschaften.zauber, "Zauber",
                harder))
    # }}}
    def chance_talent(self,name='',harder=0):# {{{
        return ipop.trywrap(self._chance,(name, talente.suche.talent,
                talente.talentliste, self.eigenschaften.talente, "Talent",
                harder))
    # }}}
    def chance_gaben(self,name='',harder=0):# {{{
        return ipop.trywrap(self._chance,(name, talente.suche.gabe,
                talente.gabenliste, self.eigenschaften.gaben, "Gabe",
                harder))
    # }}}
    def _chance(self, name, suche, talentliste, bekannt,# {{{
            talauber, harder=0):
        name = self._suche(name, suche, talentliste.namen, bekannt, talauber)
        if name == -1: return -1
        print("Ermittle Wahrscheinlichkeit von '%s'"%(name))
        skill = bekannt[name].skill
        stats = self.eigenschaften.basis
        probe = talente.probe.proben_eigenschaften(name, talentliste,
                fullmatch=True)
        if probe:
            harder = harder + probe[1]
            probe = probe[0]
        else: return False
        return proben.chance(probe[0], probe[1], probe[2],
                harder=harder, skill=skill, stats=stats)
    # }}}
    def aktiv(self):# {{{
        """Setzt die momentan vom Submodule 'proben' verwendeten stats auf die
        Basiseigenschaften des momentanen Helden"""
        proben.set_stats(self.eigenschaften.basis)
    # }}}
    def held_von_helden_xml(self,infile):# {{{
        traits  = {}
        talents = {}
        fights  = {}
        spells  = {}
        tree    = ET.parse(infile)
        root    = tree.getroot()
        for trait in root.iter('eigenschaft'):
            traits[trait.attrib['name']] = int(trait.attrib['value'])
        for talent in root.iter('talent'):
            talents[talent.attrib['name']] = int(talent.attrib['value'])
        # for fight in root.iter('kampfwerte'):
            # fights[fight.attrib['name']] = int(fight.attrib['value'])
        spellslist = root[0].find('zauberliste')
        spe
        talents = hero.getElementsByTagName('talent')
        fights  = hero.getElementsByTagName('kampfwerte')
        spells  = hero.getElementsByTagName('zauber')
        return [hero,traits,talents,fights,spells]
    # }}}
    def _suche(self, name, suche, talentliste, bekannt, talauber):# {{{
        if len(bekannt) == 0:
            self._kein_talent(talauber)
            return -1
        matches = suche(name)
        if len(matches) == 0:
            print("%s '%s' nicht bekannt."%(talauber, name))
            return -1
        elif len(matches) != 1:
            evtl = [ i for i in matches if talentliste[i] in bekannt ]
            if len(evtl) == 0:
                self._print_name()
                print(" kennt %s '%s' nicht."%(talauber, name))
                return -1
            elif len(evtl) != 1:
                if len(name) > 0:
                    print("'%s' konnte nicht eindeutig ermittelt werden!"%(
                        name))
                print("Welche%s %s ist gemeint?"%(
                    msg_endung_welche[talauber], talauber))
                name = ipop.choice_from_list(evtl, print_list=talentliste,
                        out_list=talentliste)
            else: name = talentliste[evtl[0]]
        else:
            zz = talentliste[matches[0]]
            if zz not in bekannt:
                self._print_name()
                print(" kennt %s '%s' nicht."%(talauber, name))
                return -1
            name = zz
        return name
    # }}}
    def _print_name(self):# {{{
        print(self._get_name(),end="")
    #}}}
    def _get_name(self):# {{{
        return ( self.spitzname if self.spitzname != None else 
                ( self.name if self.name != None else "Held" ) )
    #}}}
    def _kein_talent(self, talauber):# {{{
        self._print_name()
        if talauber == "Zauber": print(" kann ",end="")
        else: print(" hat ",end="")
        print("kein%s %s!"%(msg_endung_kein[talauber], talauber))
    # }}}
# }}}
