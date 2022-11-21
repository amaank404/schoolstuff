# Converts formula to name
import re

chpat = re.compile("^c(?P<catoms>[0-9]*)h(?P<hatoms>[0-9]*)")

primarygrp = {
    2: "an",
    0: "en",
    -2: "yn",
}

count = {
    1: "meth",
    2: "eth",
    3: "prop",
    4: "but",
    5: "pent",
    6: "hex",
    7: "hept",
    8: "oct",
    9: "non",
    10: "dec",
}

def hrevfm(n: int, q: int, h: int) -> int:   # Applies 2n+m-q=h to find m
    v = h + q - 2*n
    if v not in range(-2, 3, 2): # [-2  0  2]
        raise ValueError("Invalid number of Hydrogen Atoms with Given number of Carbon Atoms")
    return v

def convertformula2name(formula: str) -> str:
    formula = formula.lower() # Normalize the case

    m = chpat.match(formula)
    # Determine the number of Carbon and Hydrogen atoms
    catoms = m.group('catoms')
    hatoms = m.group('hatoms')

    if catoms == '':
        catoms = 1
    else:
        catoms = int(catoms)

    if hatoms == '':
        hatoms = 1
    else:
        hatoms = int(hatoms)
        
    if formula.endswith("cooh"): #Carboxylic Acid
        n = catoms+1
        q = 3
        h = hatoms
        m = hrevfm(n, q, h)
        return count[n] + primarygrp[m] + "oic acid"
    elif formula.endswith("cl") or formula.endswith("br"):  # Halo
        n = catoms
        q = 1
        h = hatoms
        m = hrevfm(n, q, h)
        return ("chloro" if formula.endswith("cl") else "bromo") + count[n] + primarygrp[m] + 'e'
    elif formula.endswith("oh"):  # Alcohol
        n = catoms
        q = 1
        h = hatoms
        m = hrevfm(n, q, h)
        return count[n] + primarygrp[m] + "ol"
    elif formula.endswith("cho"):  # Aldehyde
        n = catoms + 1
        q = 3
        h = hatoms
        m = hrevfm(n, q, h)
        return count[n] + primarygrp[m] + "al"
    elif formula.endswith("o"):  # Ketone
        n = catoms
        q = 2
        h = hatoms
        m = hrevfm(n, q, h)
        return count[n] + primarygrp[m] + "one"
    else:  # General
        return count[catoms] + primarygrp[hrevfm(catoms, 0, hatoms)] + 'e'


while True:
    fm = input("Tell the formula> ")
    print(f"Its name is {convertformula2name(fm).title()}")
    print()
