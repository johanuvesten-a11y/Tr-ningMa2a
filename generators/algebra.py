import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift
from utils import formatera_polynom


def skapa_potensregler_uppgift(niva: int) -> Uppgift:
    """Potenslagarna (multiplikation, division, potens av potens, negativa exponenter, bråkexponenter och olika baser)."""
    var = random.choice(['x', 'a', 'y'])
    if niva == 1:
        typ = random.choice([
            'mult', 'div', 'potens_potens',
            'kombinerat_brak', 'negativ_exp_siffra', 'negativ_exp_var'
        ])
        if typ == 'mult':
            m = random.randint(2, 7)
            n = random.randint(2, 7)
            latex_str = f"{var}^{{{m}}} \\cdot {var}^{{{n}}}"
            ratt = f"{var}^{m + n}"
            tips = "Använd potenslagen för multiplikation med samma bas (se formelbladet)."
        elif typ == 'div':
            n = random.randint(2, 5)
            m = n + random.randint(2, 6)
            latex_str = f"\\frac{{{var}^{{{m}}}}}{{{var}^{{{n}}}}}"
            ratt = f"{var}^{m - n}" if (m - n) > 1 else var
            tips = "Använd potenslagen för division med samma bas (se formelbladet)."
        elif typ == 'potens_potens':
            m = random.randint(2, 5)
            n = random.randint(2, 4)
            latex_str = f"({var}^{{{m}}})^{{{n}}}"
            ratt = f"{var}^{m * n}"
            tips = "Använd potenslagen för potens av en potens (se formelbladet)."
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
            tips = "Förenkla sifferkoefficienterna och potenserna var för sig."
        elif typ == 'negativ_exp_siffra':
            val = random.choice([
                ("5^{-2}", "1/25", "Skriv om den negativa exponenten till bråkform (se formelbladet). Svara i bråk- eller decimalform."),
                ("2^{-3}", "1/8", "Skriv om den negativa exponenten till bråkform (se formelbladet). Svara i bråk- eller decimalform."),
                ("4^{-2}", "1/16", "Skriv om den negativa exponenten till bråkform (se formelbladet). Svara i bråk- eller decimalform."),
                ("10^{-2}", "1/100", "Skriv om den negativa exponenten till bråkform (se formelbladet). Svara i bråk- eller decimalform."),
                ("3^0 + 2^{-2}", "5/4", "Utnyttja definitionen för exponenten 0 och negativa exponenter (se formelbladet).")
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
                undertext="Använd potenslagen för division (se formelbladet).",
                krav_inga_parenteser=True
            )

        return Uppgift(
            info_text="Förenkla potensuttrycket så långt som möjligt:",
            latex_text=latex_str,
            fraga="Ange det förenklade uttrycket:",
            ratt_svar=ratt,
            input_typ="text",
            svarstyp="string_math",
            undertext=tips,
            krav_inga_parenteser=True
        )
    else:
        typ = random.choice([
            'olika_baser',
            'potens_produkt_neg',
            'likadana_termer',
            'potensekv_olika_baser',
            'brak_exponent_varde',
            'potensekv_brak_exp'
        ])
        if typ == 'olika_baser':
            bas, mult_bas, k = random.choice([
                (2, 4, 2), (2, 8, 3), (3, 9, 2), (3, 27, 3), (5, 25, 2)
            ])
            variant = random.choice(['mult', 'div', 'brak'])
            if variant == 'mult':
                e1 = random.randint(2, 6)
                e2 = random.randint(2, 4)
                latex_str = f"{bas}^{{{e1}}} \\cdot {mult_bas}^{{{e2}}}"
                tot_exp = e1 + k * e2
            elif variant == 'div':
                e2 = random.randint(2, 4)
                e1 = k * e2 + random.randint(2, 5)
                latex_str = f"\\frac{{{bas}^{{{e1}}}}}{{{mult_bas}^{{{e2}}}}}"
                tot_exp = e1 - k * e2
            else:
                e1 = random.randint(2, 4)
                e2 = random.randint(2, 4)
                e3 = random.randint(1, 2)
                tot_exp = k * e1 + e2 - k * e3
                if tot_exp <= 1:
                    e1 += 2
                    tot_exp = k * e1 + e2 - k * e3
                latex_str = f"\\frac{{{mult_bas}^{{{e1}}} \\cdot {bas}^{{{e2}}}}}{{{mult_bas}^{{{e3}}}}}"

            return Uppgift(
                info_text=f"Förenkla uttrycket och skriv det som en enda potens med basen {bas}:",
                latex_text=latex_str,
                fraga=f"Skriv svaret på potensform med basen {bas} (t.ex. {bas}^6):",
                ratt_svar=f"{bas}^{tot_exp}",
                input_typ="text",
                svarstyp="potensform",
                undertext=f"Skriv först om alla potenser så att de får basen {bas}."
            )
        elif typ == 'potens_produkt_neg':
            variant = random.choice(['produkt_mult', 'produkt_div'])
            if variant == 'produkt_mult':
                c1 = random.choice([2, 3])
                e1 = random.randint(2, 4)
                p = random.choice([2, 3])
                c2 = random.randint(2, 5)
                e2 = random.randint(2, e1 * p - 1)
                tot_c = (c1 ** p) * c2
                tot_e = e1 * p - e2
                latex_str = f"({c1}{var}^{{{e1}}})^{{{p}}} \\cdot {c2}{var}^{{-{e2}}}"
            else:
                c1 = random.choice([2, 4])
                p = random.choice([2, 3])
                e1 = random.randint(2, 4)
                c2 = random.choice([2, 4, 8])
                while (c1 ** p) % c2 != 0:
                    c2 = 2
                e2 = random.randint(2, e1 * p - 1)
                tot_c = (c1 ** p) // c2
                tot_e = e1 * p - e2
                latex_str = f"\\frac{{({c1}{var}^{{{e1}}})^{{{p}}}}}{{{c2}{var}^{{{e2}}}}}"

            var_del = var if tot_e == 1 else f"{var}^{tot_e}"
            return Uppgift(
                info_text="Förenkla uttrycket så långt som möjligt:",
                latex_text=latex_str,
                fraga="Ange det förenklade uttrycket:",
                ratt_svar=f"{tot_c}{var_del}",
                input_typ="text",
                svarstyp="string_math",
                undertext="Utnyttja potenslagen för potens av en produkt (se formelbladet).",
                krav_inga_parenteser=True
            )
        elif typ == 'likadana_termer':
            bas, antal, steg = random.choice([
                (2, 2, 1), (2, 4, 2), (2, 8, 3),
                (3, 3, 1), (3, 9, 2),
                (5, 5, 1)
            ])
            if antal <= 4 and random.choice([True, False]):
                latex_str = " + ".join([f"{bas}^x"] * antal)
            else:
                koeff = antal + 1
                latex_str = f"{koeff} \\cdot {bas}^x - {bas}^x"

            return Uppgift(
                info_text="Förenkla summan och skriv uttrycket som en enda potens:",
                latex_text=latex_str,
                fraga=f"Skriv svaret som en potens med basen {bas} (t.ex. {bas}^(x+1)):",
                ratt_svar=f"{bas}^(x+{steg})",
                input_typ="text",
                svarstyp="potensform",
                undertext="Räkna hur många likadana potenstermer du har och skriv antalet som en potens."
            )
        elif typ == 'potensekv_olika_baser':
            bas, mult_bas, k = random.choice([
                (2, 4, 2), (2, 8, 3), (3, 9, 2), (3, 27, 3), (5, 25, 2)
            ])
            if random.choice([True, False]):
                exp_hl = random.randint(2, 4)
                latex_str = f"{bas}^x = {mult_bas}^{{{exp_hl}}}"
                ratt = k * exp_hl
            else:
                namn = mult_bas
                latex_str = f"{bas}^x = \\frac{{1}}{{{namn}}}"
                ratt = -k

            return Uppgift(
                info_text="Lös exponentialekvationen utan räknare:",
                latex_text=latex_str,
                fraga="Bestäm x:",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="int",
                undertext=f"Skriv om båda leden som potenser med basen {bas}."
            )
        elif typ == 'brak_exponent_varde':
            val = random.choice([
                ("8^{\\frac{1}{3}}", 2, "Upphöjningen till 1/3 motsvarar tredjeroten ur basen."),
                ("16^{\\frac{1}{2}}", 4, "Upphöjningen till 1/2 motsvarar kvadratroten ur basen."),
                ("27^{\\frac{1}{3}}", 3, "Upphöjningen till 1/3 motsvarar tredjeroten ur basen."),
                ("81^{\\frac{1}{4}}", 3, "Upphöjningen till 1/4 motsvarar fjärderoten ur basen."),
                ("4^{\\frac{3}{2}}", 8, "Skriv 4^(3/2) som (4^(1/2))^3 eller (4^3)^(1/2)."),
                ("9^{\\frac{3}{2}}", 27, "Skriv 9^(3/2) som (9^(1/2))^3 eller (9^3)^(1/2).")
            ])
            expr_latex, ratt, tips = val
            return Uppgift(
                info_text="Beräkna värdet av potensuttrycket utan räknare:",
                latex_text=expr_latex,
                fraga="Ange uttryckets värde:",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="int",
                undertext=tips
            )
        else:
            # Ekvationer av typen (x + a)^(1/n) = c eller x^(1/n) = c
            if random.choice([True, False]):
                n = random.choice([2, 3, 4])
                c = random.choice([2, 3]) if n >= 3 else random.choice([2, 3, 4, 5])
                a = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                x_sol = (c ** n) - a
                a_str = f"+ {a}" if a > 0 else f"- {abs(a)}"
                return Uppgift(
                    info_text="Lös ekvationen algebraiskt:",
                    latex_text=f"(x {a_str})^{{\\frac{{1}}{{{n}}}}} = {c}",
                    fraga="Bestäm x:",
                    ratt_svar=x_sol,
                    input_typ="text",
                    svarstyp="int",
                    undertext=f"Upphöj båda leden till {n} för att bli av med bråkexponenten."
                )
            else:
                n = random.choice([2, 3])
                c = random.choice([2, 3, 4])
                x_sol = c ** n
                return Uppgift(
                    info_text="Lös ekvationen algebraiskt:",
                    latex_text=f"x^{{\\frac{{1}}{{{n}}}}} = {c}",
                    fraga="Bestäm x:",
                    ratt_svar=x_sol,
                    input_typ="text",
                    svarstyp="int",
                    undertext=f"Upphöj båda leden till {n}."
                )


def skapa_kvadrering_konjugat_uppgift(niva: int) -> Uppgift:
    """Kvadrerings- och konjugatreglerna (utveckling, ekvationer, faktorisering, extremvärden och resonemang)."""
    if niva == 1:
        typ = random.choice([
            'kvad1', 'kvad2', 'konjugat',
            'kvad_minus_konj', 'koeff_minus_kvad', 'tva_kvadrater'
        ])
        if typ == 'kvad1':
            a = random.randint(2, 8)
            uttryck = f"(x + {a})^2"
            svar = formatera_polynom([(1, 'x^2'), (2 * a, 'x'), (a ** 2, '')])
            tips = "Använd första kvadreringsregeln (se formelbladet)."
        elif typ == 'kvad2':
            a = random.randint(2, 8)
            uttryck = f"(x - {a})^2"
            svar = formatera_polynom([(1, 'x^2'), (-2 * a, 'x'), (a ** 2, '')])
            tips = "Använd andra kvadreringsregeln (se formelbladet)."
        elif typ == 'konjugat':
            a = random.randint(2, 8)
            uttryck = f"(x + {a})(x - {a})"
            svar = formatera_polynom([(1, 'x^2'), (-a ** 2, '')])
            tips = "Använd konjugatregeln (se formelbladet)."
        elif typ == 'kvad_minus_konj':
            a = random.randint(2, 6)
            b = random.randint(2, 6)
            uttryck = f"(x + {a})^2 - (x - {b})(x + {b})"
            svar = formatera_polynom([(2 * a, 'x'), (a ** 2 + b ** 2, '')])
            tips = "Utveckla parenteserna var för sig och var noga med minustecknet framför den andra parentesen."
        elif typ == 'koeff_minus_kvad':
            k = random.choice([2, 3])
            a = random.randint(2, 5)
            uttryck = f"({k}x - {a})^2 - {k ** 2}x^2"
            svar = formatera_polynom([(-2 * k * a, 'x'), (a ** 2, '')])
            tips = "Kom ihåg att kvadrera både sifferkoefficienten och x i första termen."
        else:
            a = random.randint(2, 6)
            uttryck = f"(x + {a})^2 - (x - {a})^2"
            svar = formatera_polynom([(4 * a, 'x')])
            tips = "Behåll parentesen runt det andra utvecklade uttrycket tills du bytt tecken."

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
            'faktorisera_tva_steg',
            'huvudrakning_konj',
            'extremvarde_uttryck',
            'foljandetal_resonemang'
        ])
        if typ == 'yttre_koeff_omvand':
            if random.choice([True, False]):
                c = random.choice([2, 3])
                k1 = 2
                a = random.randint(1, 4)
                k2 = 3
                b = random.randint(1, 4)
                uttryck = f"{c}({k1}x - {a})^2 - ({k2}x - {b})({k2}x + {b})"
                x2_koeff = c * (k1 ** 2) - (k2 ** 2)
                x_koeff = -2 * c * k1 * a
                konst = c * (a ** 2) + (b ** 2)
                svar = formatera_polynom([(x2_koeff, 'x^2'), (x_koeff, 'x'), (konst, '')])
                tips = "Utveckla kvadraten och konjugatuttrycket inne i parenteser först, multiplicera därefter in faktorer och tecken."
            else:
                a = random.randint(2, 6)
                k = random.choice([2, 3])
                uttryck = f"({a} - {k}x)^2 - ({a} + {k}x)({k}x - {a})"
                svar = formatera_polynom([(2 * (k ** 2), 'x^2'), (-2 * a * k, 'x')])
                tips = "Studera tecknen i den andra produkten noga – ställ om termerna i samma ordning innan du använder konjugatregeln."

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
            k = random.choice([2, 3])
            a = random.randint(2, 5)
            b = random.randint(1, 4)
            x_sol = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            hl = -2 * k * a * x_sol + (a ** 2) + (b ** 2)
            uttryck = f"({k}x - {a})^2 - ({k}x + {b})({k}x - {b}) = {hl}"
            return Uppgift(
                info_text="Lös ekvationen algebraiskt:",
                latex_text=uttryck,
                fraga="Bestäm x:",
                ratt_svar=x_sol,
                input_typ="text",
                svarstyp="int",
                undertext="Utveckla vänsterledet med kvadrerings- och konjugatregeln – observera vad som händer med x²-termerna."
            )

        elif typ == 'okand_konstant':
            k = random.choice([2, 3])
            a_val = random.randint(2, 6)
            x_term = 2 * k * a_val
            konst = a_val ** 2
            uttryck = f"({k}x + a)^2 - {k ** 2}x^2 = {x_term}x + {konst}"
            return Uppgift(
                info_text="Likheten nedan gäller för alla värden på x:",
                latex_text=uttryck,
                fraga="Bestäm det positiva värdet på konstanten a:",
                ratt_svar=a_val,
                input_typ="text",
                svarstyp="int",
                undertext="Utveckla vänsterledet och jämför termerna med högerledet."
            )

        elif typ == 'faktorisera_tva_steg':
            if random.choice([True, False]):
                k = random.choice([2, 3, 4, 5])
                a = random.randint(2, 7)
                uttryck = formatera_polynom([(k, 'x^2'), (-k * (a ** 2), '')])
                svar = f"{k}*(x - {a})*(x + {a})"
                tips = "Faktorisera i två steg: bryt ut största gemensamma faktor och använd sedan konjugatregeln."
            else:
                k = random.choice([2, 3])
                a = random.randint(2, 5)
                tecken = random.choice([-1, 1])
                uttryck = formatera_polynom([(k ** 2, 'x^2'), (tecken * 2 * k * a, 'x'), (a ** 2, '')])
                svar = f"({k}*x + {a})^2" if tecken > 0 else f"({k}*x - {a})^2"
                tips = "Använd kvadreringsregeln baklänges."

            return Uppgift(
                info_text="Faktorisera uttrycket så långt som möjligt:",
                latex_text=uttryck,
                fraga="Skriv det faktoriserade uttrycket (t.ex. 3(x - 2)(x + 2) eller (2x - 3)^2):",
                ratt_svar=svar,
                input_typ="text",
                svarstyp="faktoriserad",
                undertext=tips
            )

        elif typ == 'huvudrakning_konj':
            if random.choice([True, False]):
                summa = random.choice([12, 15, 18, 20, 25])
                diff = random.choice([3, 4, 5, 6, 8])
                svar = summa * diff
                return Uppgift(
                    info_box_text=f"För två tal $a$ och $b$ gäller att $a + b = {summa}$ och $a - b = {diff}$.",
                    info_box_style="purple",
                    fraga="Beräkna värdet av a² − b²:",
                    ratt_svar=svar,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Skriv om a² − b² med hjälp av konjugatregeln."
                )
            else:
                bas = random.choice([50, 100, 200])
                delta = random.choice([2, 3, 4, 5])
                t1 = bas + delta
                t2 = bas - delta
                svar = (t1 + t2) * (t1 - t2)
                return Uppgift(
                    info_text="Beräkna värdet utan miniräknare:",
                    latex_text=f"{t1}^2 - {t2}^2",
                    fraga="Ange uttryckets värde:",
                    ratt_svar=svar,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Utnyttja konjugatregeln baklänges."
                )

        elif typ == 'extremvarde_uttryck':
            # Skapar uttryck som förenklas till k*x^2 + c (där k > 0 ger minsta värde c, och k < 0 ger största värde c)
            k = random.choice([-2, 2, 3])
            p = random.randint(1, 4)
            c = random.choice([-6, -4, 3, 5, 8])
            # Utgångspunkt: k*(x + p)^2 + c - k*x^2 = 2*k*p*x + k*p^2 + c
            # Vi väljer ett startuttryck av typen (k + 1)*x^2 + ... - x^2 så att x^2 blir k*x^2
            uttryck = f"({k + 1}x + {p})^2 - x^2 - {2 * (k + 1) * p}x + {c - (k + 1) * (p ** 2)}"
            extrem_typ = "minsta" if k > 0 else "största"
            return Uppgift(
                info_text="Förenkla uttrycket nedan och bestäm dess extremvärde:",
                latex_text=uttryck,
                fraga=f"Ange uttryckets {extrem_typ} värde:",
                ratt_svar=c,
                input_typ="text",
                svarstyp="int",
                undertext=f"Utveckla och förenkla uttrycket – undersök hur {extrem_typ} värdet uppnås för x."
            )

        else:
            # På varandra följande heltal: (n + 1)^2 - (n - 1)^2 = 4n, eller (n + 1)^2 - n^2 = 2n + 1
            if random.choice([True, False]):
                n_val = random.randint(4, 15)
                svar = 4 * n_val
                return Uppgift(
                    info_box_text="Låt $n$ vara ett heltal. Betrakta skillnaden mellan kvadraten på $(n + 1)$ och kvadraten på $(n - 1)$.",
                    info_box_style="purple",
                    fraga=f"Vilket värde får uttrycket (n + 1)² − (n − 1)² när n = {n_val}?",
                    ratt_svar=svar,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Utveckla båda kvadraterna och förenkla: (n + 1)² − (n − 1)² = 4n."
                )
            else:
                n_val = random.randint(4, 15)
                svar = 2 * n_val + 1
                return Uppgift(
                    info_box_text="Skillnaden mellan kvadraterna på två på varandra följande heltal $n$ och $(n + 1)$ kan skrivas som $(n + 1)^2 - n^2$.",
                    info_box_style="purple",
                    fraga=f"Beräkna värdet av (n + 1)² − n² när n = {n_val}:",
                    ratt_svar=svar,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Utveckla (n + 1)² och subtrahera n²."
                )


def skapa_rationella_uttryck_uppgift(niva: int) -> Uppgift:
    """Förenkling av rationella uttryck med konjugat- och kvadreringsreglerna."""
    a = random.randint(2, 7)
    if niva == 1:
        typ = random.choice(['konjugat_plus', 'konjugat_minus', 'kvadrering_plus', 'kvadrering_minus'])
        if typ == 'konjugat_plus':
            talj = formatera_polynom([(1, 'x^2'), (-a ** 2, '')])
            namn = formatera_polynom([(1, 'x'), (a, '')])
            svar = formatera_polynom([(1, 'x'), (-a, '')])
            tips = "Faktorisera täljaren med hjälp av formelbladets regler innan du förkortar."
        elif typ == 'konjugat_minus':
            talj = formatera_polynom([(1, 'x^2'), (-a ** 2, '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = formatera_polynom([(1, 'x'), (a, '')])
            tips = "Faktorisera täljaren med hjälp av formelbladets regler innan du förkortar."
        elif typ == 'kvadrering_plus':
            talj = formatera_polynom([(1, 'x^2'), (2 * a, 'x'), (a ** 2, '')])
            namn = formatera_polynom([(1, 'x'), (a, '')])
            svar = formatera_polynom([(1, 'x'), (a, '')])
            tips = "Skriv om täljaren i faktorform med hjälp av formelbladet."
        else:
            talj = formatera_polynom([(1, 'x^2'), (-2 * a, 'x'), (a ** 2, '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = formatera_polynom([(1, 'x'), (-a, '')])
            tips = "Skriv om täljaren i faktorform med hjälp av formelbladet."

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
            talj = formatera_polynom([(k, 'x^2'), (-k * (a ** 2), '')])
            namn = formatera_polynom([(1, 'x'), (-a, '')])
            svar = f"{k}*(x + {a})"
            tips = "Faktorisera täljaren i två steg innan du förkortar."
        elif typ == 'namnare_konj':
            talj = formatera_polynom([(k, 'x'), (-k * a, '')])
            namn = formatera_polynom([(1, 'x^2'), (-a ** 2, '')])
            svar = f"{k}/(x + {a})"
            tips = "Faktorisera både täljare och nämnare så långt som möjligt."
        else:
            talj = formatera_polynom([(1, 'x'), (-a, '')])
            namn = formatera_polynom([(1, 'x^2'), (-2 * a, 'x'), (a ** 2, '')])
            svar = f"1/(x - {a})"
            tips = "Skriv om nämnaren i faktorform med hjälp av formelbladet."

        return Uppgift(
            info_text="Förenkla det rationella uttrycket i flera steg:",
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
        typ = random.choice([
            'nollprod_faktor', 'nollprod_utbryt', 'ren_kvadrat',
            'pq_enkel', 'pq_udda_brak', 'koefficient_a',
            'omskriv_parentes', 'dubbelparentes_omskriv',
            'omskriv_kvadrat', 'dubbelrot'
        ])
        if typ == 'nollprod_faktor':
            r1 = random.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            r2 = random.choice([x for x in [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6] if x != r1])
            f1 = f"(x - {r1})" if r1 > 0 else f"(x + {abs(r1)})"
            f2 = f"(x - {r2})" if r2 > 0 else f"(x + {abs(r2)})"
            ekv_str = f"{f1}{f2} = 0"
            ratt_svar = sorted([float(r1), float(r2)])
            tips = "Ekvationen är redan faktoriserad – använd nollproduktmetoden."
        elif typ == 'nollprod_utbryt':
            r2 = random.choice([-8, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8])
            ekv_str = f"{formatera_polynom([(1, 'x^2'), (-r2, 'x')])} = 0"
            ratt_svar = sorted([0.0, float(r2)])
            tips = "Bryt ut gemensam faktor och använd nollproduktmetoden."
        elif typ == 'ren_kvadrat':
            a = random.choice([1, 2, 3])
            r = random.randint(2, 6)
            ekv_str = f"{formatera_polynom([(a, 'x^2'), (-a * (r ** 2), '')])} = 0"
            ratt_svar = sorted([float(-r), float(r)])
            tips = "Isolera x²-termen och använd kvadratrotsmetoden."
        elif typ == 'pq_enkel':
            r1 = random.randint(-6, 5)
            r2 = random.choice([x for x in range(-6, 7) if x != r1 and (r1 + x) % 2 == 0])
            p = -(r1 + r2)
            q = r1 * r2
            ekv_str = f"{formatera_polynom([(1, 'x^2'), (p, 'x'), (q, '')])} = 0"
            ratt_svar = sorted([float(r1), float(r2)])
            tips = "Använd PQ-formeln (se formelbladet)."
        elif typ == 'pq_udda_brak':
            if random.choice([True, False]):
                r1 = random.choice([-5, -3, -1, 1, 3, 5])
                r2 = random.choice([-6, -4, -2, 2, 4, 6])
                p = -(r1 + r2)
                q = r1 * r2
                ekv_str = f"{formatera_polynom([(1, 'x^2'), (p, 'x'), (q, '')])} = 0"
                ratt_svar = sorted([float(r1), float(r2)])
                tips = "Använd PQ-formeln och räkna noggrant med bråk eller decimaler under rottecknet."
            else:
                a = 2
                m = random.choice([-5, -3, -1, 1, 3, 5])
                r1 = m / 2.0
                r2 = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                ekv_str = f"{formatera_polynom([(a, 'x^2'), (-(m + a * r2), 'x'), (m * r2, '')])} = 0"
                ratt_svar = sorted([r1, float(r2)])
                tips = "Dividera först med koefficienten framför x². Rötter får anges i decimal- eller bråkform."
        elif typ == 'koefficient_a':
            a = random.choice([2, 3, 4])
            r1 = random.randint(-4, 3)
            r2 = random.choice([x for x in range(-4, 5) if x != r1])
            p = -(r1 + r2)
            q = r1 * r2
            ekv_str = f"{formatera_polynom([(a, 'x^2'), (a * p, 'x'), (a * q, '')])} = 0"
            ratt_svar = sorted([float(r1), float(r2)])
            tips = "Skriv ekvationen på normalform (x² + px + q = 0) innan du använder PQ-formeln."
        elif typ == 'omskriv_parentes':
            r1 = random.choice([x for x in range(-5, 5) if x != 0])
            r2 = random.choice([x for x in range(-5, 6) if x != r1 and (r1 + x) != 0 and (r1 * x) != 0])
            p = -(r1 + r2)
            q = r1 * r2
            parentes = formatera_polynom([(1, 'x'), (p, '')])
            ekv_str = f"x({parentes}) = {-q}"
            ratt_svar = sorted([float(r1), float(r2)])
            tips = "Utveckla parentesen och samla alla termer i ett led (= 0)."
        elif typ == 'dubbelparentes_omskriv':
            r1 = random.randint(-5, 4)
            r2 = random.choice([x for x in range(-5, 6) if x != r1])
            p = -(r1 + r2)
            q = r1 * r2
            a = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            b = random.choice([x for x in [-4, -3, -2, -1, 1, 2, 3, 4] if x != a and (a + x - p) != 0 and (a * x - q) != 0])
            c = (a + b) - p
            d = (a * b) - q
            f1 = f"(x + {a})" if a > 0 else f"(x - {abs(a)})"
            f2 = f"(x + {b})" if b > 0 else f"(x - {abs(b)})"
            hl = formatera_polynom([(c, 'x'), (d, '')])
            ekv_str = f"{f1}{f2} = {hl}"
            ratt_svar = sorted([float(r1), float(r2)])
            tips = "Multiplicera ihop parenteserna, samla alla termer i vänsterledet (= 0) och använd PQ-formeln."
        elif typ == 'omskriv_kvadrat':
            a = random.choice([-4, -3, -2, 2, 3, 4])
            r = random.randint(2, 5)
            hl = formatera_polynom([(2 * a, 'x'), (a ** 2 + r ** 2, '')])
            vl = f"(x + {a})^2" if a > 0 else f"(x - {abs(a)})^2"
            ekv_str = f"{vl} = {hl}"
            ratt_svar = sorted([float(-r), float(r)])
            tips = "Utveckla vänsterledet med kvadreringsregeln och förenkla."
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
        typ = random.choice([
            'rationell_x_namnare',
            'konstant_dubbelrot',
            'baklanges_pq',
            'faktorisering_falla'
        ])
        if typ == 'rationell_x_namnare':
            r1 = random.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            r2 = random.choice([x for x in [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6] if x != r1 and (r1 + x) != 0])
            p = -(r1 + r2)
            q = r1 * r2
            if q > 0:
                ekv_str = f"x + \\frac{{{q}}}{{x}} = {-p}"
            else:
                ekv_str = f"x - \\frac{{{abs(q)}}}{{x}} = {-p}"

            return Uppgift(
                info_text="Lös ekvationen algebraiskt:",
                latex_text=ekv_str,
                fraga="Ange ekvationens två lösningar:",
                ratt_svar=sorted([float(r1), float(r2)]),
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x₁ =", "x₂ ="],
                undertext="Multiplicera samtliga termer i båda leden med x för att bli av med nämnaren."
            )
        elif typ == 'konstant_dubbelrot':
            if random.choice([True, False]):
                k = random.randint(2, 7)
                q = k ** 2
                ratt = 2 * k
                return Uppgift(
                    info_text="Andragradsekvationen nedan har exakt en lösning (dubbelrot):",
                    latex_text=f"x^2 + ax + {q} = 0",
                    fraga="Bestäm det positiva värdet på konstanten a:",
                    ratt_svar=ratt,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Undersök uttrycket under rottecknet i PQ-formeln när ekvationen har exakt en lösning."
                )
            else:
                k = random.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
                p = 2 * k
                d = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                ratt = (k ** 2) + d
                vl = formatera_polynom([(1, 'x^2'), (p, 'x')])
                return Uppgift(
                    info_text="Andragradsekvationen nedan har exakt en lösning (dubbelrot):",
                    latex_text=f"{vl} + c = {d}",
                    fraga="Bestäm konstanten c:",
                    ratt_svar=ratt,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Skriv först ekvationen på formen x² + px + q = 0 och sätt därefter uttrycket under rottecknet till 0."
                )
        elif typ == 'baklanges_pq':
            r1 = random.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
            r2 = random.choice([x for x in range(-6, 7) if x != r1 and (r1 + x) != 0])
            p = -(r1 + r2)
            q = r1 * r2
            if random.choice([True, False]):
                q_str = f"+ {q}" if q > 0 else f"- {abs(q)}"
                ekv_str = f"x^2 + px {q_str} = 0"
            else:
                vl = formatera_polynom([(1, 'x^2'), (p, 'x')])
                ekv_str = f"{vl} + q = 0"

            return Uppgift(
                info_text=f"Andragradsekvationen nedan har en lösning $x_1 = {r1}$.",
                latex_text=ekv_str,
                fraga="Bestäm ekvationens andra lösning x₂:",
                ratt_svar=r2,
                input_typ="text",
                svarstyp="int",
                undertext="Sätt in den kända lösningen i ekvationen för att bestämma den okända konstanten först."
            )
        else:
            # Ekvationer av typen (x - a)^2 = c*(x - a) där division med (x - a) skulle tappa en rot
            a = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
            c = random.choice([-4, -3, -2, 2, 3, 4])
            r1 = a
            r2 = a + c
            f_a = f"(x - {a})" if a > 0 else f"(x + {abs(a)})"
            ekv_str = f"{f_a}^2 = {c}{f_a}"
            return Uppgift(
                info_text="Lös ekvationen algebraiskt:",
                latex_text=ekv_str,
                fraga="Ange ekvationens två lösningar:",
                ratt_svar=sorted([float(r1), float(r2)]),
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x₁ =", "x₂ ="],
                undertext="Flytta över högerledet och bryt ut den gemensamma parentesen i stället för att dividera bort den."
            )


def skapa_ekvationssystem_uppgift(niva: int) -> Uppgift:
    """Linjära ekvationssystem (grafiskt, algebraiskt, decimaler och parametervillkor)."""
    if niva == 1:
        typ = random.choice(['grafisk', 'substitution', 'addition'])
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
            fig.add_trace(go.Scatter(x=x_vals, y=k1 * x_vals + m1, mode='lines', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
            fig.add_trace(go.Scatter(x=x_vals, y=k2 * x_vals + m2, mode='lines', line=dict(color='#d9534f', width=3), hoverinfo='skip'))
            fig.update_layout(
                xaxis=dict(title="x", range=[-6, 6], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                yaxis=dict(title="y", range=[-6, 6], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                height=360, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
            )

            ekv1_str = f"y = {formatera_polynom([(k1, 'x'), (m1, '')])}"
            ekv2_str = f"y = {formatera_polynom([(k2, 'x'), (m2, '')])}"
            return Uppgift(
                info_text="Bestäm skärningspunkten (x, y) för linjerna i grafen:",
                latex_text=f"\\begin{{cases}} {ekv1_str} \\\\ {ekv2_str} \\end{{cases}}",
                fraga="Ange lösningen till ekvationssystemet:",
                ratt_svar=[float(x_sol), float(y_sol)],
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x =", "y ="],
                undertext="Avläs koordinaterna där de två linjerna skär varandra.",
                figur=fig
            )

        elif typ == 'substitution':
            a = random.choice([1, 2, 3])
            b = random.choice([-3, -2, -1, 1, 2, 3])
            y_sol = random.randint(-3, 4)
            x_sol = a * y_sol + b
            c = random.choice([1, 2])
            d = random.choice([1, 2, 3])
            hl2 = c * x_sol + d * y_sol

            ekv1 = f"x = {formatera_polynom([(a, 'y'), (b, '')])}"
            ekv2 = f"{formatera_polynom([(c, 'x'), (d, 'y')])} = {hl2}"
            return Uppgift(
                info_text="Lös ekvationssystemet algebraiskt:",
                latex_text=f"\\begin{{cases}} {ekv1} \\\\ {ekv2} \\end{{cases}}",
                fraga="Bestäm x och y:",
                ratt_svar=[float(x_sol), float(y_sol)],
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x =", "y ="],
                undertext="Sätt in uttrycket för x från den första ekvationen i den andra ekvationen."
            )

        else:
            x_sol = random.randint(-3, 4)
            y_sol = random.randint(-3, 4)
            a1, b1 = 2, 1
            a2, b2 = 3, -1
            hl1 = a1 * x_sol + b1 * y_sol
            hl2 = a2 * x_sol + b2 * y_sol

            ekv1 = f"{formatera_polynom([(a1, 'x'), (b1, 'y')])} = {hl1}"
            ekv2 = f"{formatera_polynom([(a2, 'x'), (b2, 'y')])} = {hl2}"
            return Uppgift(
                info_text="Lös ekvationssystemet algebraiskt:",
                latex_text=f"\\begin{{cases}} {ekv1} \\\\ {ekv2} \\end{{cases}}",
                fraga="Bestäm x och y:",
                ratt_svar=[float(x_sol), float(y_sol)],
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x =", "y ="],
                undertext="Addera ekvationerna ledvis för att eliminera y."
            )
    else:
        typ = random.choice(['decimal_system', 'omstuvning_system', 'oandligt_manga_losningar'])
        if typ == 'decimal_system':
            # System med decimaltal (t.ex. 0,5x + 0,2y = ... och x - y = ...)
            x_sol = random.choice([-4, -2, 2, 4, 6])
            y_sol = random.choice([-3, -1, 1, 3, 5])
            d1 = 0.5
            d2 = 0.2
            hl1 = round(d1 * x_sol + d2 * y_sol, 2)
            hl2 = x_sol - y_sol
            hl1_str = str(hl1).replace('.', ',')
            hl2_str = str(hl2).replace('.', ',')

            ekv1 = f"0,5x + 0,2y = {hl1_str}"
            ekv2 = f"x - y = {hl2_str}"
            return Uppgift(
                info_text="Lös ekvationssystemet algebraiskt:",
                latex_text=f"\\begin{{cases}} {ekv1} \\\\ {ekv2} \\end{{cases}}",
                fraga="Bestäm x och y:",
                ratt_svar=[float(x_sol), float(y_sol)],
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x =", "y ="],
                undertext="Multiplicera gärna den första ekvationen med 10 för att slippa decimaltal."
            )

        elif typ == 'omstuvning_system':
            # Ekvationer med termer på båda sidor som behöver ordnas om först
            x_sol = random.randint(-3, 4)
            y_sol = random.randint(-3, 4)
            # Ekv 1: 2x - y + c = d  => 2x - y = d - c
            c = random.randint(1, 5)
            d = 2 * x_sol - y_sol + c
            # Ekv 2: x + 3y - e = f  => x + 3y = f + e
            e = random.randint(1, 5)
            f = x_sol + 3 * y_sol - e

            ekv1 = f"2x - y + {c} = {d}"
            ekv2 = f"x + 3y - {e} = {f}"
            return Uppgift(
                info_text="Ordna om ekvationerna och lös systemet algebraiskt:",
                latex_text=f"\\begin{{cases}} {ekv1} \\\\ {ekv2} \\end{{cases}}",
                fraga="Bestäm x och y:",
                ratt_svar=[float(x_sol), float(y_sol)],
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x =", "y ="],
                undertext="Samla x- och y-termer i vänsterledet och konstanterna i högerledet."
            )

        else:
            # Oändligt många lösningar: t.ex. 2x + 3y = a och 6x + 9y = b => b = 3a
            mult = random.choice([2, 3])
            a_val = random.randint(2, 6)
            ratt_b = mult * a_val
            ekv1 = f"2x + 3y = {a_val}"
            ekv2 = f"{2 * mult}x + {3 * mult}y = b"
            return Uppgift(
                info_text="Ekvationssystemet nedan ska ha oändligt många lösningar:",
                latex_text=f"\\begin{{cases}} {ekv1} \\\\ {ekv2} \\end{{cases}}",
                fraga="Bestäm konstanten b:",
                ratt_svar=ratt_b,
                input_typ="text",
                svarstyp="int",
                undertext="För oändligt många lösningar måste den andra ekvationen vara en multipel av den första."
            )
