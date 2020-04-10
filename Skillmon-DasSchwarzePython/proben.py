import random
random.seed()

global remain
global stats
stats = {}

def w6(num=1):# {{{
    a = []
    for i in range(num):
        a.append(random.randint(1,6))
    return a
# }}}
def w6_1(): return random.randint(1,6)
def w6_c(num=1): return [ random.randint(1,6) for i in range(num) ]
def w20(num=1):# {{{
    # list comprehension is faster for num >= 3
    a = []
    for i in range(num):
        a.append(random.randint(1,20))
    return a
    # return [ random.randint(1,20) for i in range(num) ]
# }}}
def w20_1(): return random.randint(1,20)
def w20_c(num=1): return [ random.randint(1,20) for i in range(num) ]
def odd_die(sides, num=1): return [random.randint(1,sides) for i in range(num)]

# Meljow Stats (leider hier noch nötig, gute Lösung für Proben etc. gesucht)
# stats={"mu":13,"kl":14,"in":13,"ch":14,"ff":12,"ge":13,"ko":13,"kk":12}

def set_stats(newstats):# {{{
    global stats
    stats = newstats
# }}}

def probe1(st1,harder=0,skill=0,silent=False,stats=stats):# {{{
    global remain
    v1 = w20_1()
    s1 = (st1 if type(st1) == int else stats[st1])
    skarder = skill - harder
    rem = s1 + skarder - v1
    remain = rem
    if not silent:
        if type(st1) == str: print(st1,end="")
        else: print("  ",end="")
        print(" %2d / %2d"%(v1,s1),end="")
        if skarder < 0: print(" - %2d"%(abs(skarder)))
        else: print("")
    if v1 == 20:
        if not silent: print("Probe nicht bestanden")
        return False
    if v1 == 1:
        if not silent: print("Probe bestanden")
        remain = max(1,min(skill,rem))
        return True
    if rem >= 0:
        if not silent:
            print("Probe bestanden",end="")
            if skarder > 0:
                print(" mit %d übrig"%(min(min(skill,skarder),rem)),end="")
            print("")
        return True
    else:
        if not silent: print("Probe nicht bestanden mit %d zuviel"%(-rem))
        return False
# }}}

def probe3(st1,st2,st3,harder=0,skill=0,silent=False,stats=stats):# {{{
    global remain 
    v = w20_c(3)
    st = (st1,st2,st3)
    s = [ (st[i] if type(st[i]) == int else stats[st[i]]) for i in range(3) ]
    skarder = skill - harder
    if not silent:
        for i in range(3):
            if type(st[i]) == str: print(st[i],end=" ")
            else: print("  ",end=" ")
            print("%2d / %2d"%(v[i],s[i]),end=" ")
            if skarder < 0: print("- %d"%(abs(skarder)))
            else: print("")
    zwanzigen = v.count(20)
    einsen = v.count(1)  
    failed = 0
    if skarder < 0:
        rem = 1
        for i in range(3):
            if s[i] + skarder < v[i]: failed += v[i] - s[i] - skarder
    else:
        rem = skarder
        for i in range(3):
            if v[i] > s[i]: rem -= v[i] - s[i]
        failed = -rem
    return _probe_printout(skill,rem,failed,einsen,zwanzigen,3)
# }}}

def probe(st,harder=0,skill=0,silent=False,nonstop=False,stats=stats):# {{{
    global remain
    if type(st) == str or type(st) == int: st = (st,)
    skarder = skill - harder
    failed = 0
    zwanzigen = 0
    einsen = 0
    if skarder < 0:
        rem = 1
        for stat in st:
            s,v = _prope_stat(stat,silent)
            if not silent: print("%2d / %2d - %2d"%(v,s,abs(skarder)))
            if v == 20: zwanzigen += 1
            elif v == 1: einsen += 1
            if s + skarder < v: failed += v - s - skarder
    else:
        rem = skarder
        for stat in st:
            s,v = _prope_stat(stat,silent)
            if not silent: print("%2d / %2d"%(v,s))
            if v == 20: zwanzigen += 1
            elif v == 1: einsen += 1
            if v > s: rem -= v - s
        failed = -rem
    return _probe_printout(skill,rem,failed,einsen,zwanzigen,len(st))
# }}}

def _prope_stat(stat,silent):# {{{
    if type(stat) == str:
        s = stats[stat]
        if not silent: print(stat,end=" ")
    else:
        s = stat
        if not silent: print("  ",end=" ")
    return (s,w20_1())
# }}}

def _probe_printout(skill,rem,failed,einsen,zwanzigen,proben_len):# {{{
    global remain
    remain = max(1,min(skill,rem))
    if einsen == proben_len:
        print("Probe bestanden mit %d übrig!"%(remain),end=" ")
        print("Spektakulärer Erfolg!")
        return True
    if einsen == 2:
        print("Probe bestande mit %d übrig"%(remain))
        return True
    remain = failed
    if zwanzigen == proben_len:
        print("Probe nicht bestanden mit %d zuviel!"%(failed),end=" ")
        print("Spektakulärer Patzer!")
        return False
    if zwanzigen == 2:
        print("Probe nicht bestanden mit %d zuviel!"%(failed))
        return False
    if failed > 0:
        print("Probe nicht bestanden mit %d zuviel"%(failed))
        return False
    remain = max(1,min(skill,rem))
    print("Probe bestanden mit %d übrig"%(remain))
    return True
# }}}

def chance(st1,st2,st3,harder=0,skill=0,silent=False,# {{{
        stats=stats):
    skarder = skill - harder
    s1 = (st1 if type(st1) == int else stats[st1])
    s2 = (st2 if type(st2) == int else stats[st2])
    s3 = (st3 if type(st3) == int else stats[st3])
    if skarder <= 0:
        prob = ( s1 + skarder ) * ( s2 + skarder ) * ( s3 + skarder ) / 8000
    else:
        prob = 0
        for w1 in range(1,21):
            for w2 in range(1,21):
                for w3 in range(1,21):
                    num1  = (w1 ==  1) + (w2 ==  1) + (w3 ==  1)
                    if num1 > 1:
                        prob += 1
                        continue
                    num20 = (w1 == 20) + (w2 == 20) + (w3 == 20)
                    if num20 > 1: continue
                    d1 = s1 - w1
                    d2 = s2 - w2
                    d3 = s3 - w3
                    rem = skarder + min(0,d1) + min(0,d2) + min(0,d3)
                    if rem >= 0: prob += 1
        prob /= 8000
    prob = max(prob,0.00725)# mit mind. zwei Einsen hat man immer bestanden
    if not silent:
        print("Wahrscheinlichkeit des Bestehens: {0} %".format(
            round(100 * prob, 4)))
    return round(prob,6)
# }}}

# MU = "mu"
# KL = "kl"
# IN = "in"
# CH = "ch"
# FF = "ff"
# GE = "ge"
# KO = "ko"
# KK = "kk"
