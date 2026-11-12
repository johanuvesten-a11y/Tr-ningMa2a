import random
import math
from models import Uppgift
from utils import formatera_polynom

def skapa_pq_uppgift(niva: int) -> Uppgift:
    """Andragradsekvationer via PQ-formeln eller nollproduktmetoden."""
    if niva == 1:
        # Enkla heltalsrötter
        r1 = random.randint(-6, 6)
        r2 = random.randint(-6, 6)
        p = -(r1 + r2)
        q = r1 * r2
        ekv_str = f"{formatera_polynom([(1, 'x^2'), (p, 'x'), (q, '')])} = 0"
        
        ratt_svar = sorted(list(set([float(r1), float(r2)])))
        return Uppgift(
            info_text="Lös andragradsekvationen:",
            latex_text=ekv_str,
            fraga="Ange ekvationens rötter/lösningar:",
            ratt_svar=ratt_svar,
            input_typ="flera_text" if len(ratt_svar) > 1 else "text",
            svarstyp="array_float" if len(ratt_svar) > 1 else "float",
            undertext="Om ekvationen har två rötter, fyll i båda fälten."
        )
    else:
        # Ekvationer med koefficient a != 1 eller nollprodukt
        typ = random.choice(['nollprodukt', 'koefficient_a'])
        if typ == 'nollprodukt':
            r2 = random.choice([-8, -5, -3, 3, 5, 8])
            ekv_str = f"{formatera_polynom([(1, 'x^2'), (-r2, 'x')])} = 0"
            ratt_svar = sorted([0.0, float(r2)])
            tips = "Tips: Bryt ut x och använd nollproduktmetoden."
        else:
            a = random.choice([2, 3, 4])
            r1 = random.randint(-4, 4)
            r2 = random.randint(-4, 4)
            p = -(r1 + r2)
            q = r1 * r2
            ekv_str = f"{formatera_polynom([(a, 'x^2'), (a*p, 'x'), (a*q, '')])} = 0"
            ratt_svar = sorted(list(set([float(r1), float(r2)])))
            tips = "Tips: Dividera med koefficienten framför x² först."

        return Uppgift(
            info_text="Lös ekvationen algebraiskt:",
            latex_text=ekv_str,
            fraga="Ange ekvationens lösningar:",
            ratt_svar=ratt_svar,
            input_typ="flera_text" if len(ratt_svar) > 1 else "text",
            svarstyp="array_float" if len(ratt_svar) > 1 else "float",
            undertext=tips
        )
def skapa_kvadrering_konjugat_uppgift(niva: int) -> Uppgift:
    """Kvadrerings- och konjugatreglerna."""
    a = random.randint(1, 5)
    b = random.randint(1, 6)
    a_str = "x" if a == 1 else f"{a}x"
    
    regler = ['första_kvadrering', 'andra_kvadrering', 'konjugat']
    val = random.choice(regler)
    
    if val == 'första_kvadrering':
        uttryck = f"({a_str} + {b})^2"
        svar = formatera_polynom([(a**2, 'x^2'), (2*a*b, 'x'), (b**2, '')])
        info = "Utveckla med första kvadreringsregeln:"
    elif val == 'andra_kvadrering':
        uttryck = f"({a_str} - {b})^2"
        svar = formatera_polynom([(a**2, 'x^2'), (-2*a*b, 'x'), (b**2, '')])
        info = "Utveckla med andra kvadreringsregeln:"
    else:
        uttryck = f"({a_str} + {b})({a_str} - {b})"
        svar = formatera_polynom([(a**2, 'x^2'), (-b**2, '')])
        info = "Utveckla med konjugatregeln:"
        
    return Uppgift(
        info_text=info,
        latex_text=uttryck,
        fraga="Skriv det utvecklade uttrycket:",
        ratt_svar=svar,
        input_typ="text",
        svarstyp="string_math",
        undertext="Använd ^ för upphöjt till (t.ex. 4x^2 + 12x + 9)."
    )

def skapa_ekvationssystem_uppgift(niva: int) -> Uppgift:
    """Linjära ekvationssystem med två variabler."""
    x = random.randint(-5, 8)
    y = random.randint(-5, 8)
    
    a1, b1 = random.randint(1, 4), random.choice([-3, -2, -1, 1, 2, 3])
    a2, b2 = random.choice([-3, -2, -1, 1, 2, 3]), random.randint(1, 4)
    while a1 * b2 == a2 * b1:  # Undvik parallella linjer
        b2 += 1
        
    c1 = a1 * x + b1 * y
    c2 = a2 * x + b2 * y
    
    eq1 = f"{formatera_polynom([(a1, 'x'), (b1, 'y')])} = {c1}"
    eq2 = f"{formatera_polynom([(a2, 'x'), (b2, 'y')])} = {c2}"
    
    return Uppgift(
        info_text="Givet ekvationssystemet:",
        latex_text=f"\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}",
        fraga="Lös ekvationssystemet:",
        ratt_svar=[float(x), float(y)],
        input_typ="flera_text",
        svarstyp="ekvationssystem",
        undertext="Bestäm värdet på både x och y. Lös systemet med substitutions- eller additionsmetoden."
    )
    
def skapa_rationella_uttryck_uppgift(niva: int) -> Uppgift:
    """Förenkling av rationella uttryck."""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    
    # (x^2 - b^2) / (x - b) = x + b
    uttryck = f"\\frac{{x^2 - {b**2}}}{{x - {b}}}"
    svar = f"x + {b}"
    
    return Uppgift(
        info_text="Förenkla det rationella uttrycket så långt som möjligt:",
        latex_text=uttryck,
        fraga="Vad blir det förenklade uttrycket?",
        ratt_svar=svar,
        input_typ="text",
        svarstyp="string_math",
        undertext="Tips: Faktorisera täljaren med konjugatregeln först."
    )
