import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift
from utils import formatera_polynom

def skapa_potensregler_uppgift(niva: int) -> Uppgift:
    """Potenslagarna (multiplikation, division, potens av potens och negativa exponenter)."""
    var = random.choice(['x', 'a', 'y'])
    if niva == 1:
        typ = random.choice(['mult', 'div', 'potens_potens'])
        if typ == 'mult':
            m = random.randint(2, 7)
            n = random.randint(2, 7)
            latex_str = f"{var}^{{{m}}} \\cdot {var}^{{{n}}}"
            ratt = f"{var}^{m + n}"
        elif typ == 'div':
            n = random.randint(2, 5)
            m = n + random.randint(2, 6)
            latex_str = f"\\frac{{{var}^{{{m}}}}}{{{var}^{{{n}}}}}"
            ratt = f"{var}^{m - n}" if (m - n) > 1 else var
        else:
            m = random.randint(2, 5)
            n = random.randint(2, 4)
            latex_str = f"({var}^{{{m}}})^{{{n}}}"
            ratt = f"{var}^{m * n}"
            
        return Uppgift(
            info_text="Förenkla potensuttrycket så långt som möjligt:",
            latex_text=latex_str,
            fraga="Skriv svaret på potensform:",
            ratt_svar=ratt,
            input_typ="text",
            svarstyp="string_math",
            undertext="Använd potenslagarna (se formelbladet vid behov).",
            krav_inga_parenteser=True
        )
    else:
        typ = random.choice(['kombinerat_brak', 'negativ_exp_siffra', 'negativ_exp_var'])
        if typ == 'kombinerat_brak':
            c3 = random.choice([2, 3, 4, 5])
            kvot = random.randint(2, 5)
            c1 = random.choice([2, 3, 4, 6])
            c2 = (c3 * kvot) // c1 if (c3 * kvot) % c1 == 0 else c3
            kvot_faktisk = (c1 * c2) // c3
            
            e1 = random.randint(3, 6)
            e2 = random.randint(2, 5)
            e3 = random.randint(2, e1 + e2 - 2)
            res_exp = e1 + e2 - e3
            
            latex_str = f"\\frac{{{c1}{var}^{{{e1}}} \\cdot {c2}{var}^{{{e2}}}}}{{{c3}{var}^{{{e3}}}}}"
            var_del = var if res_exp == 1 else f"{var}^{res_exp}"
            ratt = f"{kvot_faktisk}{var_del}"
            return Uppgift(
                info_text="Förenkla uttrycket så långt som möjligt:",
                latex_text=latex_str,
                fraga="Ange det förenklade uttrycket:",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="string_math",
                undertext="Förenkla sifferkoefficienterna och potenserna var för sig.",
                krav_inga_parenteser=True
            )
        elif typ == 'negativ_exp_siffra':
            val = random.choice([
                ("5^{-2}", "1/25"),
                ("2^{-3}", "1/8"),
                ("4^{-2}", "1/16"),
                ("10^{-2}", "1/100"),
                ("3^0 + 2^{-2}", "5/4")
            ])
            expr_latex, ratt = val
            return Uppgift(
                info_text="Beräkna värdet av uttrycket:",
                latex_text=expr_latex,
                fraga="Ange uttryckets värde:",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="string_math",
                undertext="Svara i bråk- eller decimalform (se potenslagarna på formelbladet vid behov).",
                krav_inga_parenteser=True
            )
        else:
            e1 = random.randint(2, 4)
            e2 = e1 + random.randint(2, 4)
            diff = e1 - e2
            latex_str = f"\\frac{{{var}^{{{e1}}}}}{{{var}^{{{e2}}}}}"
            ratt = f"{var}^{diff}"
            return Uppgift(
                info_text="Förenkla uttrycket:",
                latex_text=latex_str,
                fraga="Skriv svaret med negativ exponent eller i bråkform (t.ex. x^-2 eller 1/x^2):",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="string_math",
                undertext="Använd potenslagarna för division.",
                krav_inga_parenteser=True
            )

def skapa_kvadrering_konjugat_uppgift(niva: int) -> Uppgift:
    """Kvadrerings- och konjugatreglerna."""
    if niva == 1:
        a = random.randint(2, 8)
        typ = random.choice(['kvad1', 'kvad2', 'konjugat'])
        if typ == 'kvad1':
            uttryck = f"(x + {a})^2"
            svar = formatera_polynom([(1, 'x^2'), (2*a, 'x'), (a**2, '')])
            tips = "Använd kvadreringsregeln eller multiplicera ihop parenteserna."
        elif typ == 'kvad2':
            uttryck = f"(x - {a})^2"
            svar = formatera_polynom([(1, 'x^2'), (-2*a, 'x'), (a**2, '')])
            tips = "Använd kvadreringsregeln och var noggrann med tecknen."
        else:
            uttryck = f"(x + {a})(x - {a})"
            svar = formatera_polynom([(1, 'x^2'), (-a**2, '')])
            tips = "Använd konjugatregeln eller multiplicera ihop parenteserna."
            
        return Uppgift(
            info_text="Utveckla och förenkla uttrycket:",
            latex_text=uttryck,
            fraga="Skriv det utvecklade uttrycket:",
            ratt_svar=svar,
            input_typ="text",
            svarstyp="string_math",
            undertext=tips,
            krav_inga_parenteser=True
        )
    else:
        typ = random.choice(['kvad_minus_konj', 'koeff_minus_kvad', 'tva_kvadrater'])
        if typ == 'kvad_minus_konj':
            a = random.randint(2, 6)
            b = random.randint(2, 6)
            uttryck = f"(x + {a})^2 - (x - {b})(x + {b})"
            svar = formatera_polynom([(2*a, 'x'), (a**2 + b**2, '')])
            tips = "Utveckla parenteserna var för sig och var noga med minustecknet framför den andra parentesen!"
        elif typ == 'koeff_minus_kvad':
            k = random.choice([2, 3])
            a = random.randint(2, 5)
            uttryck = f"({k}x - {a})^2 - {k**2}x^2"
            svar = formatera_polynom([(-2*k*a, 'x'), (a**2, '')])
            tips = "Tänk på att hela uttrycket framför minustecknet ska kvadreras."
        else:
            a = random.randint(2, 6)
            uttryck = f"(x + {a})^2 - (x - {a})^2"
            svar = formatera_polynom([(4*a, 'x')])
            tips = "Utveckla båda kvadraterna och behåll parentesen runt det andra uttrycket tills du bytt tecken."
            
        return Uppgift(
            info_text="Utveckla och förenkla uttrycket så långt som möjligt:",
            latex_text=uttryck,
            fraga="Ange det förenklade uttrycket:",
            ratt_svar=svar,
            input_typ="text",
            svarstyp="string_math",
            undertext=tips,
            krav_inga_parenteser=True
        )

def skapa_rationella_uttryck_uppgift(niva: int) -> Uppgift:
    """Förenkling av rationella uttryck med konjugat- och kvadreringsreglerna."""
    a = random.randint(2, 7)
    if niva == 1:
        typ = random.choice(['konjugat_plus', 'konjugat_minus', 'kvadrering_plus', 'kvadrering_minus'])
        if typ == 'konjugat_plus':
            talj = formatera_polynom([(1, 'x^2'), (-a**2, '')])
            namn = formatera_polynom([(1, 'x'), (a, '')])
            svar = formatera_polynom([(1, 'x'), (-a, '')])
        elif typ == 'konjugat_minus':
            talj = formatera_polynom([(1, 'x^2'), (-a**2, '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = formatera_polynom([(1, 'x'), (a, '')])
        elif typ == 'kvadrering_plus':
            talj = formatera_polynom([(1, 'x^2'), (2*a, 'x'), (a**2, '')])
            namn = formatera_polynom([(1, 'x'), (a, '')])
            svar = formatera_polynom([(1, 'x'), (a, '')])
        else:
            talj = formatera_polynom([(1, 'x^2'), (-2*a, 'x'), (a**2, '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = formatera_polynom([(1, 'x'), (-a, '')])
            
        return Uppgift(
            info_text="Förenkla det rationella uttrycket så långt som möjligt:",
            latex_text=f"\\frac{{{talj}}}{{{namn}}}",
            fraga="Ange det förenklade uttrycket:",
            ratt_svar=svar,
            input_typ="text",
            svarstyp="string_math",
            undertext="Faktorisera täljaren och förkorta gemensamma faktorer."
        )
    else:
        k = random.choice([2, 3, 4])
        typ = random.choice(['tva_steg_konj', 'namnare_konj', 'namnare_kvad'])
        if typ == 'tva_steg_konj':
            talj = formatera_polynom([(k, 'x^2'), (-k*(a**2), '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = f"{k}*(x + {a})"
            tips = "Faktorisera täljaren i flera steg innan du förkortar."
        elif typ == 'namnare_konj':
            talj = formatera_polynom([(k, 'x'), (-k*a, '')])
            namn = formatera_polynom([(1, 'x^2'), (-a**2, '')])
            svar = f"{k}/(x + {a})"
            tips = "Faktorisera både täljare och nämnare så långt som möjligt."
        else:
            talj = formatera_polynom([(1, 'x'), (-a, '')])
            namn = formatera_polynom([(1, 'x^2'), (-2*a, 'x'), (a**2, '')])
            svar = f"1/(x - {a})"
            tips = "Faktorisera nämnaren innan du förkortar."
            
        return Uppgift(
            info_text="Förenkla det rationella uttrycket i två steg:",
            latex_text=f"\\frac{{{talj}}}{{{namn}}}",
            fraga="Ange det förenklade uttrycket:",
            ratt_svar=svar,
            input_typ="text",
            svarstyp="string_math",
            undertext=tips
        )

def skapa_pq_uppgift(niva: int) -> Uppgift:
    """Andragradsekvationer via nollproduktmetoden, kvadratrotsmetoden och PQ-formeln."""
    if niva == 1:
        typ = random.choice(['nollprod_faktor', 'nollprod_utbryt', 'ren_kvadrat', 'pq_enkel'])
        if typ == 'nollprod_faktor':
            r1 = random.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            r2 = random.choice([x for x in [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6] if x != r1])
            f1 = f"(x - {r1})" if r1 > 0 else f"(x + {abs(r1)})"
            f2 = f"(x - {r2})" if r2 > 0 else f"(x + {abs(r2)})"
            ekv_str = f"{f1}{f2} = 0"
            ratt_svar = sorted([float(r1), float(r2)])
            tips = "Ekvationen är skriven i faktorform."
        elif typ == 'nollprod_utbryt':
            r2 = random.choice([-8, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8])
            ekv_str = f"{formatera_polynom([(1, 'x^2'), (-r2, 'x')])} = 0"
            ratt_svar = sorted([0.0, float(r2)])
            tips = "Faktorisera vänsterledet innan du löser ekvationen."
        elif typ == 'ren_kvadrat':
            a = random.choice([1, 2, 3])
            r = random.randint(2, 6)
            ekv_str = f"{formatera_polynom([(a, 'x^2'), (-a*(r**2), '')])} = 0"
            ratt_svar = sorted([float(-r), float(r)])
            tips = "Lös ut x² och tänk på hur många lösningar ekvationen har."
        else:
            r1 = random.randint(-6, 5)
            r2 = random.choice([x for x in range(-6, 7) if x != r1])
            p = -(r1 + r2)
            q = r1 * r2
            ekv_str = f"{formatera_polynom([(1, 'x^2'), (p, 'x
