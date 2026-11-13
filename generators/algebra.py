import math
import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift
from utils import formatera_polynom

def skapa_potensregler_uppgift(niva: int) -> Uppgift:
    """Potenslagarna: Nivå 1 (grundläggande + koefficienter + negativa exponenter), Nivå 2 (olika baser, sammansatta uttryck, potenssummor)."""
    var = random.choice(['x', 'a', 'y'])
    if niva == 1:
        typ = random.choice(['mult', 'div', 'potens_potens', 'kombinerat_brak', 'negativ_exp_siffra', 'negativ_exp_var'])
        if typ == 'mult':
            m = random.randint(2, 7)
            n = random.randint(2, 7)
            latex_str = f"{var}^{{{m}}} \\cdot {var}^{{{n}}}"
            ratt = f"{var}^{m + n}"
            tips = "Använd potenslagen a^m · a^n = a^(m+n)."
        elif typ == 'div':
            n = random.randint(2, 5)
            m = n + random.randint(2, 6)
            latex_str = f"\\frac{{{var}^{{{m}}}}}{{{var}^{{{n}}}}}"
            ratt = f"{var}^{m - n}" if (m - n) > 1 else var
            tips = "Använd potenslagen a^m / a^n = a^(m-n)."
        elif typ == 'potens_potens':
            m = random.randint(2, 5)
            n = random.randint(2, 4)
            latex_str = f"({var}^{{{m}}})^{{{n}}}"
            ratt = f"{var}^{m * n}"
            tips = "Använd potenslagen (a^m)^n = a^(m·n)."
        elif typ == 'kombinerat_brak':
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
                ("5^{-2}", "1/25", "Kom ihåg att a^(-n) = 1 / a^n. Svara i bråk- eller decimalform."),
                ("2^{-3}", "1/8", "Kom ihåg att a^(-n) = 1 / a^n. Svara i bråk- eller decimalform."),
                ("4^{-2}", "1/16", "Kom ihåg att a^(-n) = 1 / a^n. Svara i bråk- eller decimalform."),
                ("10^{-2}", "1/100", "Kom ihåg att a^(-n) = 1 / a^n. Svara i bråk- eller decimalform."),
                ("3^0 + 2^{-2}", "5/4", "Kom ihåg att a^0 = 1 och a^(-n) = 1 / a^n.")
            ])
            expr_latex, ratt, tips = val
            return Uppgift(
                info_text="Beräkna värdet av uttrycket:",
                latex_text=expr_latex,
                fraga="Ange uttryckets värde:",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="string_math",
                undertext=tips,
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
                undertext="Använd potenslagen a^m / a^n = a^(m-n).",
                krav_inga_parenteser=True
            )
            
        return Uppgift(
            info_text="Förenkla potensuttrycket så långt som möjligt:",
            latex_text=latex_str,
            fraga="Skriv svaret på potensform:",
            ratt_svar=ratt,
            input_typ="text",
            svarstyp="string_math",
            undertext=tips,
            krav_inga_parenteser=True
        )
    else:
        typ = random.choice(['olika_baser_siffra', 'potens_av_produkt', 'lika_potenstermer', 'ekvation_olika_baser'])
        
        if typ == 'olika_baser_siffra':
            bas, stor_bas, k_exp = random.choice([
                (2, 4, 2),
                (2, 8, 3),
                (3, 9, 2),
                (3, 27, 3),
                (5, 25, 2)
            ])
            op = random.choice(['mult', 'div', 'kombi'])
            if op == 'mult':
                e1 = random.randint(2, 6)
                e2 = random.randint(2, 4)
                if random.choice([True, False]):
                    latex_str = f"{bas}^{{{e1}}} \\cdot {stor_bas}^{{{e2}}}"
                else:
                    latex_str = f"{stor_bas}^{{{e2}}} \\cdot {bas}^{{{e1}}}"
                ratt_exp = e1 + k_exp * e2
            elif op == 'div':
                e2 = random.randint(2, 5)
                e1 = random.randint(2, 4)
                if k_exp * e1 == e2:
                    e1 += 1
                latex_str = f"\\frac{{{stor_bas}^{{{e1}}}}}{{{bas}^{{{e2}}}}}"
                ratt_exp = k_exp * e1 - e2
            else:
                e1 = random.randint(2, 4)
                e2 = random.randint(2, 5)
                e3 = random.randint(2, 4)
                ratt_exp = k_exp * e1 + e2 - e3
                if ratt_exp in [0, 1]:
                    e1 += 1
                    ratt_exp = k_exp * e1 + e2 - e3
                latex_str = f"\\frac{{{stor_bas}^{{{e1}}} \\cdot {bas}^{{{e2}}}}}{{{bas}^{{{e3}}}}}"
                
            return Uppgift(
                info_text="Skriv uttrycket som en enda potens:",
                latex_text=latex_str,
                fraga=f"Skriv svaret på potensform med basen {bas} (t.ex. {bas}^5):",
                ratt_svar=f"{bas}^{ratt_exp}",
                input_typ="text",
                svarstyp="potensform",
                undertext=f"Skriv om {stor_bas} som en potens med basen {bas} innan du använder potenslagarna."
            )
            
        elif typ == 'potens_av_produkt':
            fall = random.choice(['mult_neg', 'div_koeff'])
            if fall == 'mult_neg':
                c1 = random.choice([2, 3, 4])
                e1 = random.randint(2, 4)
                p = random.choice([2, 3])
                c2 = random.choice([2, 3, 5])
                e2 = random.randint(1, e1 * p - 1)
                
                koeff = (c1 ** p) * c2
                res_exp = e1 * p - e2
                var_del = var if res_exp == 1 else f"{var}^{res_exp}"
                latex_str = f"({c1}{var}^{{{e1}}})^{{{p}}} \\cdot {c2}{var}^{{-{e2}}}"
                ratt = f"{koeff}{var_del}"
            else:
                c1 = random.choice([2, 3, 4])
                p = random.choice([2, 3])
                c2 = c1 if p == 2 else random.choice([2, 4])
                koeff = (c1 ** p) // c2
                e1 = random.randint(2, 4)
                e2 = random.randint(2, e1 * p - 1)
                res_exp = e1 * p - e2
                var_del = var if res_exp == 1 else f"{var}^{res_exp}"
                latex_str = f"\\frac{{({c1}{var}^{{{e1}}})^{{{p}}}}}{{{c2}{var}^{{{e2}}}}}"
                ratt = f"{koeff}{var_del}" if koeff > 1 else var_del
                
            return Uppgift(
                info_text="Förenkla uttrycket så långt som möjligt:",
                latex_text=latex_str,
                fraga="Ange det förenklade uttrycket:",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="string_math",
                undertext="Använd potenslagen (a·b)^n = a^n · b^n på parentesen först.",
                krav_inga_parenteser=True
            )
            
        elif typ == 'lika_potenstermer':
            scenario = random.choice([
                ("3^x + 3^x + 3^x", 3, "3^(x+1)", "Tre stycken 3^x kan skrivas som 3 · 3^x."),
                ("2^x + 2^x + 2^x + 2^x", 2, "2^(x+2)", "Fyra stycken 2^x är 4 · 2^x. Skriv 4 som en potens med basen 2."),
                ("5 \\cdot 2^x - 2^x", 2, "2^(x+2)", "Förenkla koefficienterna framför 2^x först (5 - 1 = 4)."),
                ("10 \\cdot 3^x - 3^x", 3, "3^(x+2)", "Förenkla koefficienterna framför 3^x först (10 - 1 = 9)."),
                ("4 \\cdot 5^x + 5^x", 5, "5^(x+1)", "Lägg ihop termerna (4 + 1 = 5) och använd sedan potenslagarna."),
                ("3 \\cdot 2^x + 5 \\cdot 2^x", 2, "2^(x+3)", "Lägg ihop termerna (3 + 5 = 8) och skriv 8 med basen 2.")
            ])
            latex_str, bas, ratt, tips = scenario
            return Uppgift(
                info_text="Förenkla uttrycket och skriv det som en enda potens:",
                latex_text=latex_str,
                fraga=f"Skriv svaret som en potens med basen {bas} (t.ex. {bas}^(x+1)):",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="potensform",
                undertext=tips
            )
            
        else:  # ekvation_olika_baser
            ekv_fall = random.choice([
                ("2^x = 8^3", 9, "Skriv om 8 som en potens med basen 2."),
                ("2^x = 4^5", 10, "Skriv om 4 som en potens med basen 2."),
                ("3^x = 9^4", 8, "Skriv om 9 som en potens med basen 3."),
                ("3^x = 27^2", 6, "Skriv om 27 som en potens med basen 3."),
                ("5^x = 25^3", 6, "Skriv om 25 som en potens med basen 5."),
                ("2^x = \\frac{1}{16}", -4, "Skriv 1/16 som en potens med basen 2 och negativ exponent."),
                ("3^x = \\frac{1}{27}", -3, "Skriv 1/27 som en potens med basen 3 och negativ exponent."),
                ("5^x = \\frac{1}{25}", -2, "Skriv 1/25 som en potens med basen 5 och negativ exponent.")
            ])
            latex_str, ratt_x, tips = ekv_fall
            return Uppgift(
                info_text="Bestäm exponenten x i ekvationen:",
                latex_text=latex_str,
                fraga="Ange värdet på x:",
                ratt_svar=ratt_x,
                input_typ="text",
                svarstyp="int",
                undertext=tips
            )

def skapa_kvadrering_konjugat_uppgift(niva: int) -> Uppgift:
    """Kvadrerings- och konjugatreglerna: Nivå 1 (utveckling & enklare kombinationer), Nivå 2 (koefficienter, ekvationer, okänd konstant, faktorisering, huvudräkning)."""
    if niva == 1:
        typ = random.choice(['kvad1', 'kvad2', 'konjugat', 'kvad_minus_konj', 'koeff_minus_kvad', 'tva_kvadrater'])
        if typ == 'kvad1':
            a = random.randint(2, 8)
            uttryck = f"(x + {a})^2"
            svar = formatera_polynom([(1, 'x^2'), (2*a, 'x'), (a**2, '')])
            tips = "Använd första kvadreringsregeln: (a + b)² = a² + 2ab + b²."
        elif typ == 'kvad2':
            a = random.randint(2, 8)
            uttryck = f"(x - {a})^2"
            svar = formatera_polynom([(1, 'x^2'), (-2*a, 'x'), (a**2, '')])
            tips = "Använd andra kvadreringsregeln: (a - b)² = a² - 2ab + b²."
        elif typ == 'konjugat':
            a = random.randint(2, 8)
            uttryck = f"(x + {a})(x - {a})"
            svar = formatera_polynom([(1, 'x^2'), (-a**2, '')])
            tips = "Använd konjugatregeln: (a + b)(a - b) = a² - b²."
        elif typ == 'kvad_minus_konj':
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
            tips = f"Kom ihåg att ({k}x)² = {k**2}x² när du använder kvadreringsregeln."
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
    else:
        typ = random.choice([
            'yttre_koeff_omvand',
            'ekvation_kvad_konj',
            'okand_konstant',
            'faktorisering_tva_steg',
            'smart_huvudrakning'
        ])
        
        if typ == 'yttre_koeff_omvand':
            if random.choice(['yttre_koeff', 'omvand_ordning']) == 'yttre_koeff':
                c = random.choice([2, 3])
                k = random.choice([2, 3])
                a = random.randint(1, 3)
                m = random.choice([2, 3])
                b = random.randint(1, 4)
                uttryck = f"{c}({k}x - {a})^2 - ({m}x - {b})({m}x + {b})"
                koeff_x2 = c * (k**2) - (m**2)
                koeff_x = -2 * c * k * a
                konst = c * (a**2) + (b**2)
                svar = formatera_polynom([(koeff_x2, 'x^2'), (koeff_x, 'x'), (konst, '')])
                tips = f"Utveckla ({k}x - {a})² först innan du multiplicerar in {c}, och var noga med minustecknet."
            else:
                a = random.randint(2, 6)
                k = random.choice([2, 3])
                uttryck = f"({a} - {k}x)^2 - ({a} + {k}x)({k}x - {a})"
                svar = formatera_polynom([(-2 * a * k, 'x'), (2 * (a**2), '')])
                tips = f"Observera ordningen på termerna i ({a} + {k}x)({k}x - {a}) innan du använder konjugatregeln."
                
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
            
        elif typ == 'ekvation_kvad_konj':
            x_sol = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            if random.choice(['variant_a', 'variant_b']) == 'variant_a':
                a = random.randint(2, 6)
                b = random.choice([-4, -3, -2, 2, 3, 4])
                c = -(a**2) - (b**2) - 2 * b * x_sol
                par_b = f"(x + {b})^2" if b > 0 else f"(x - {abs(b)})^2"
                hl = par_b if c == 0 else (f"{par_b} + {c}" if c > 0 else f"{par_b} - {abs(c)}")
                ekv_str = f"(x + {a})(x - {a}) = {hl}"
            else:
                k = random.choice([2, 3])
                a = random.randint(1, 4)
                b = random.randint(1, 5)
                hl = -2 * a * k * x_sol + (a**2) + (b**2)
                ekv_str = f"({k}x - {a})^2 - ({k}x + {b})({k}x - {b}) = {hl}"
                
            return Uppgift(
                info_text="Lös ekvationen algebraiskt:",
                latex_text=ekv_str,
                fraga="Ange värdet på x:",
                ratt_svar=x_sol,
                input_typ="text",
                svarstyp="int",
                undertext="Utveckla parenteserna med konjugat- och kvadreringsregeln och förenkla."
            )
            
        elif typ == 'okand_konstant':
            if random.choice(['konst_a_pos', 'konst_a_diff']) == 'konst_a_pos':
                k = random.choice([1, 2, 3])
                a = random.randint(2, 7)
                kx_str = "x" if k == 1 else f"{k}x"
                k2x2_str = "x^2" if k == 1 else f"{k**2}x^2"
                uttryck = f"({kx_str} + a)^2 - {k2x2_str}"
                forenklat = formatera_polynom([(2 * a * k, 'x'), (a**2, '')])
                return Uppgift(
                    info_text=f"Uttrycket nedan kan förenklas till {forenklat}:",
                    latex_text=uttryck,
                    fraga="Bestäm det positiva talet a:",
                    ratt_svar=a,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Utveckla vänsterledet med kvadreringsregeln och jämför termerna."
                )
            else:
                a = random.randint(2, 7)
                b = random.choice([x for x in range(1, 6) if x != a])
                uttryck = f"(x + a)^2 - (x - {b})^2"
                forenklat = formatera_polynom([(2 * a + 2 * b, 'x'), (a**2 - b**2, '')])
                return Uppgift(
                    info_text=f"För ett visst värde på konstanten a gäller att uttrycket nedan är lika med {forenklat}:",
                    latex_text=uttryck,
                    fraga="Bestäm värdet på konstanten a:",
                    ratt_svar=a,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Utveckla båda parenteserna och jämför koefficienten framför x."
                )
                
        elif typ == 'faktorisering_tva_steg':
            if random.choice(['utbryt_konj', 'kvad_baklanges']) == 'utbryt_konj':
                k = random.choice([2, 3, 4, 5])
                a = random.randint(2, 7)
                uttryck = formatera_polynom([(k, 'x^2'), (-k * (a**2), '')])
                svar = f"{k}*(x - {a})*(x + {a})"
                tips = f"Bryt först ut den gemensamma faktorn {k} och använd sedan konjugatregeln baklänges."
            else:
                k = random.choice([2, 3])
                a = random.choice([x for x in range(1, 6) if math.gcd(k, x) == 1])
                tecken = random.choice([1, -1])
                uttryck = formatera_polynom([(k**2, 'x^2'), (tecken * 2 * k * a, 'x'), (a**2, '')])
                svar = f"({k}x + {a})^2" if tecken > 0 else f"({k}x - {a})^2"
                tips = "Använd kvadreringsregeln baklänges."
                
            return Uppgift(
                info_text="Faktorisera uttrycket så långt som möjligt:",
                latex_text=uttryck,
                fraga="Skriv det faktoriserade uttrycket:",
                ratt_svar=svar,
                input_typ="text",
                svarstyp="faktoriserad",
                undertext=tips
            )
            
        else:  # smart_huvudrakning
            if random.choice(['ab_varde', 'tal_kvadrater']) == 'ab_varde':
                s = random.randint(11, 25)
                d = random.randint(3, 9)
                ratt = s * d
                return Uppgift(
                    info_box_text=f"Talen a och b uppfyller att a + b = {s} och a - b = {d}.",
                    info_box_style="blue",
                    fraga="Beräkna värdet av a² - b²:",
                    ratt_svar=ratt,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Skriv om a² - b² med hjälp av konjugatregeln."
                )
            else:
                mitt = random.choice([50, 100, 200])
                diff = random.choice([2, 3, 4, 5])
                x_val = mitt + diff
                y_val = mitt - diff
                ratt = (x_val + y_val) * (x_val - y_val)
                return Uppgift(
                    info_text="Beräkna värdet av uttrycket med hjälp av konjugatregeln:",
                    latex_text=f"{x_val}^2 - {y_val}^2",
                    fraga="Ange uttryckets värde:",
                    ratt_svar=ratt,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Faktorisera uttrycket med konjugatregeln a² - b² = (a + b)(a - b)."
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
            tips = "Faktorisera täljaren med konjugatregeln."
        elif typ == 'konjugat_minus':
            talj = formatera_polynom([(1, 'x^2'), (-a**2, '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = formatera_polynom([(1, 'x'), (a, '')])
            tips = "Faktorisera täljaren med konjugatregeln."
        elif typ == 'kvadrering_plus':
            talj = formatera_polynom([(1, 'x^2'), (2*a, 'x'), (a**2, '')])
            namn = formatera_polynom([(1, 'x'), (a, '')])
            svar = formatera_polynom([(1, 'x'), (a, '')])
            tips = "Faktorisera täljaren baklänges med första kvadreringsregeln."
        else:
            talj = formatera_polynom([(1, 'x^2'), (-2*a, 'x'), (a**2, '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = formatera_polynom([(1, 'x'), (-a, '')])
            tips = "Faktorisera täljaren baklänges med andra kvadreringsregeln."
            
        return Uppgift(
            info_text="Förenkla det rationella uttrycket så långt som möjligt:",
            latex_text=f"\\frac{{{talj}}}{{{namn}}}",
            fraga="Ange det förenklade uttrycket:",
            ratt_svar=svar,
            input_typ="text",
            svarstyp="string_math",
            undertext=tips
        )
    else:
        k = random.choice([2, 3, 4])
        typ = random.choice(['tva_steg_konj', 'namnare_konj', 'namnare_kvad'])
        if typ == 'tva_steg_konj':
            talj = formatera_polynom([(k, 'x^2'), (-k*(a**2), '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = f"{k}*(x + {a})"
            tips = f"Bryt först ut {k} i täljaren och använd sedan konjugatregeln."
        elif typ == 'namnare_konj':
            talj = formatera_polynom([(k, 'x'), (-k*a, '')])
            namn = formatera_polynom([(1, 'x^2'), (-a**2, '')])
            svar = f"{k}/(x + {a})"
            tips = f"Bryt ut {k} i täljaren och faktorisera nämnaren med konjugatregeln."
        else:
            talj = formatera_polynom([(1, 'x'), (-a, '')])
            namn = formatera_polynom([(1, 'x^2'), (-2*a, 'x'), (a**2, '')])
            svar = f"1/(x - {a})"
            tips = "Faktorisera nämnaren med andra kvadreringsregeln."
            
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
            tips = "Ekvationen är redan faktoriserad – använd nollproduktmetoden direkt!"
        elif typ == 'nollprod_utbryt':
            r2 = random.choice([-8, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8])
            ekv_str = f"{formatera_polynom([(1, 'x^2'), (-r2, 'x')])} = 0"
            ratt_svar = sorted([0.0, float(r2)])
            tips = "Bryt ut x och använd nollproduktmetoden."
        elif typ == 'ren_kvadrat':
            a = random.choice([1, 2, 3])
            r = random.randint(2, 6)
            ekv_str = f"{formatera_polynom([(a, 'x^2'), (-a*(r**2), '')])} = 0"
            ratt_svar = sorted([float(-r), float(r)])
            tips = "Isolera x² och dra roten ur båda leden (glöm inte ±)."
        else:
            r1 = random.randint(-6, 5)
            r2 = random.choice([x for x in range(-6, 7) if x != r1])
            p = -(r1 + r2)
            q = r1 * r2
            ekv_str = f"{formatera_polynom([(1, 'x^2'), (p, 'x'), (q, '')])} = 0"
            ratt_svar = sorted([float(r1), float(r2)])
            tips = "Använd PQ-formeln."
            
        return Uppgift(
            info_text="Lös andragradsekvationen:",
            latex_text=ekv_str,
            fraga="Ange ekvationens två lösningar:",
            ratt_svar=ratt_svar,
            input_typ="flera_text",
            svarstyp="array_float",
            flera_labels=["x₁ =", "x₂ ="],
            undertext=tips
        )
    else:
        typ = random.choice(['koefficient_a', 'omskriv_parentes', 'omskriv_kvadrat', 'dubbelrot'])
        if typ == 'koefficient_a':
            a = random.choice([2, 3, 4])
            r1 = random.randint(-4, 3)
            r2 = random.choice([x for x in range(-4, 5) if x != r1])
            p = -(r1 + r2)
            q = r1 * r2
            ekv_str = f"{formatera_polynom([(a, 'x^2'), (a*p, 'x'), (a*q, '')])} = 0"
            ratt_svar = sorted([float(r1), float(r2)])
            return Uppgift(
                info_text="Lös ekvationen algebraiskt:",
                latex_text=ekv_str,
                fraga="Ange ekvationens två lösningar:",
                ratt_svar=ratt_svar,
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x₁ =", "x₂ ="],
                undertext=f"Tips: Dividera först hela ekvationen med {a} så att x² står ensamt."
            )
        elif typ == 'omskriv_parentes':
            r1 = random.randint(-5, 4)
            r2 = random.choice([x for x in range(-5, 6) if x != r1 and (r1 + x) != 0 and (r1 * x) != 0])
            p = -(r1 + r2)
            q = r1 * r2
            parentes = formatera_polynom([(1, 'x'), (p, '')])
            ekv_str = f"x({parentes}) = {-q}"
            ratt_svar = sorted([float(r1), float(r2)])
            return Uppgift(
                info_text="Lös ekvationen algebraiskt:",
                latex_text=ekv_str,
                fraga="Ange ekvationens två lösningar:",
                ratt_svar=ratt_svar,
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x₁ =", "x₂ ="],
                undertext="Tips: Multiplicera in x i parentesen och samla alla termer i vänsterledet (= 0)."
            )
        elif typ == 'omskriv_kvadrat':
            a = random.choice([-4, -3, -2, 2, 3, 4])
            r = random.randint(2, 5)
            hl = formatera_polynom([(2*a, 'x'), (a**2 + r**2, '')])
            vl = f"(x + {a})^2" if a > 0 else f"(x - {abs(a)})^2"
            ekv_str = f"{vl} = {hl}"
            ratt_svar = sorted([float(-r), float(r)])
            return Uppgift(
                info_text="Lös ekvationen algebraiskt:",
                latex_text=ekv_str,
                fraga="Ange ekvationens två lösningar:",
                ratt_svar=ratt_svar,
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x₁ =", "x₂ ="],
                undertext="Tips: Utveckla vänsterledet med kvadreringsregeln och förenkla."
            )
        else:
            r = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            p = -2 * r
            q = r ** 2
            ekv_str = f"{formatera_polynom([(1, 'x^2'), (p, 'x'), (q, '')])} = 0"
            return Uppgift(
                info_text="Lös andragradsekvationen:",
                latex_text=ekv_str,
                fraga="Ekvationen har endast en lösning (dubbelrot). Ange lösningen:",
                ratt_svar=r,
                input_typ="text",
                svarstyp="int",
                undertext="Använd PQ-formeln eller kvadreringsregeln baklänges."
            )

def skapa_ekvationssystem_uppgift(niva: int) -> Uppgift:
    """Linjära ekvationssystem (grafiskt och algebraiskt)."""
    if niva == 1:
        typ = random.choice(['grafisk', 'substitution'])
        x_sol = random.randint(-3, 4)
        y_sol = random.randint(-3, 4)
        
        if typ == 'grafisk':
            k1 = random.choice([-2, -1, 1, 2])
            k2 = random.choice([k for k in [-2, -1, 1, 2, 3] if k != k1])
            m1 = y_sol - k1 * x_sol
            m2 = y_sol - k2 * x_sol
            
            while abs(m1) > 6 or abs(m2) > 6:
                x_sol = random.randint(-2, 3)
                y_sol = random.randint(-2, 3)
                m1 = y_sol - k1 * x_sol
                m2 = y_sol - k2 * x_sol
                
            x_vals = np.linspace(-6, 6, 100)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=k1*x_vals + m1, mode='lines', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
            fig.add_trace(go.Scatter(x=x_vals, y=k2*x_vals + m2, mode='lines', line=dict(color='#d9534f', width=3), hoverinfo='skip'))
            fig.update_layout(
                xaxis=dict(title="x", range=[-6, 6], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                yaxis=dict(title="y", range=[-6, 6], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                height=360, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
            )
            
            ekv1_str = f"y = {formatera_polynom([(k1, 'x'), (m1, '')])}"
            ekv2_str = f"y = {formatera_polynom([(k2, 'x'), (m2, '')])}"
            return Uppgift(
                info_text="Lös ekvationssystemet grafiskt med hjälp av figuren:",
                latex_text=f"\\begin{{cases}} {ekv1_str} \\\\ {ekv2_str} \\end{{cases}}",
                plotly_fig=fig,
                fraga="Avläs skärningspunktens koordinater (x och y):",
                ratt_svar=[float(x_sol), float(y_sol)],
                input_typ="flera_text",
                svarstyp="ekvationssystem",
                flera_labels=["x =", "y ="],
                undertext="Läs av x- och y-koordinaten där linjerna korsar varandra."
            )
        else:
            k = random.choice([-2, -1, 2, 3])
            m = y_sol - k * x_sol
            a = random.choice([2, 3, 4])
            b = random.choice([1, 2])
            c = a * x_sol + b * y_sol
            
            ekv1 = f"y = {formatera_polynom([(k, 'x'), (m, '')])}"
            ekv2 = f"{formatera_polynom([(a, 'x'), (b, 'y')])} = {c}"
            return Uppgift(
                info_text="Lös ekvationssystemet algebraiskt:",
                latex_text=f"\\begin{{cases}} {ekv1} \\\\ {ekv2} \\end{{cases}}",
                fraga="Ange lösningen (x och y):",
                ratt_svar=[float(x_sol), float(y_sol)],
                input_typ="flera_text",
                svarstyp="ekvationssystem",
                flera_labels=["x =", "y ="],
                undertext="Tips: Använd substitutionsmetoden genom att sätta in uttrycket för y i den andra ekvationen."
            )
    else:
        typ = random.choices(['forlang_bada', 'antal_losningar'], weights=[0.7, 0.3], k=1)[0]
        if typ == 'forlang_bada':
            x_sol = random.randint(-3, 5)
            y_sol = random.randint(-3, 5)
            par = random.choice([(2, 3), (3, 4), (2, 5), (3, 5)])
            a1, a2 = random.sample(par, 2)
            b1 = random.choice([-3, -2, 2, 3])
            b2_kandidater = [v for v in [-4, -3, -2, 2, 3, 4] if v % b1 != 0 and b1 % v != 0 and (a1 * v - a2 * b1) != 0]
            b2 = random.choice(b2_kandidater)
            
            c1 = a1 * x_sol + b1 * y_sol
            c2 = a2 * x_sol + b2 * y_sol
            
            ekv1 = f"{formatera_polynom([(a1, 'x'), (b1, 'y')])} = {c1}"
            ekv2 = f"{formatera_polynom([(a2, 'x'), (b2, 'y')])} = {c2}"
            return Uppgift(
                info_text="Lös ekvationssystemet algebraiskt:",
                latex_text=f"\\begin{{cases}} {ekv1} \\\\ {ekv2} \\end{{cases}}",
                fraga="Ange lösningen (x och y):",
                ratt_svar=[float(x_sol), float(y_sol)],
                input_typ="flera_text",
                svarstyp="ekvationssystem",
                flera_labels=["x =", "y ="],
                undertext="Tips: Använd additionsmetoden – här behöver du förlänga båda ekvationerna."
            )
        else:
            k = random.choice([-3, -2, 2, 3])
            m1 = random.randint(-4, 4)
            fall = random.choice(['parallella', 'sammanfallande'])
            mult = random.choice([2, 3])
            if fall == 'parallella':
                m2 = m1 + random.choice([-3, -2, 2, 3])
                ekv1 = f"y = {formatera_polynom([(k, 'x'), (m1, '')])}"
                ekv2 = f"{formatera_polynom([(-mult*k, 'x'), (mult, 'y')])} = {mult*m2}"
                ratt = "0 lösningar (linjerna är parallella)"
            else:
                ekv1 = f"y = {formatera_polynom([(k, 'x'), (m1, '')])}"
                ekv2 = f"{formatera_polynom([(-mult*k, 'x'), (mult, 'y')])} = {mult*m1}"
                ratt = "Oändligt många lösningar (samma linje)"
                
            alts = [
                "0 lösningar (linjerna är parallella)",
                "1 lösning",
                "Oändligt många lösningar (samma linje)"
            ]
            return Uppgift(
                info_text="Undersök följande ekvationssystem:",
                latex_text=f"\\begin{{cases}} {ekv1} \\\\ {ekv2} \\end{{cases}}",
                fraga="Hur många lösningar har ekvationssystemet?",
                ratt_svar=ratt,
                alternativ=alts,
                input_typ="radio",
                svarstyp="string",
                undertext="Skriv om den andra ekvationen på formen y = kx + m och jämför lutning (k) och m-värde."
            )
