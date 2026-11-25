import random
from models import Uppgift
from utils import formatera_polynom


def skapa_problemlosning_uppgift(niva: int) -> Uppgift:
    """Problemlösning med ekvationssystem, andragradsekvationer i text, dubbelrot och extremvärden."""
    if niva == 1:
        typ = random.choice(['ekvationssystem_text', 'andragrad_rektangel_text'])

        if typ == 'ekvationssystem_text':
            # Två varor med pris x och y:
            # 3x + 2y = s1 och 2x + 3y = s2 (eller 2x + y = s1 och x + 2y = s2)
            x_pris = random.randint(15, 35)
            y_pris = random.randint(12, 30)
            s1 = 3 * x_pris + 2 * y_pris
            s2 = 2 * x_pris + 3 * y_pris
            return Uppgift(
                info_box_text=(
                    f"På ett café kostar 3 koppar kaffe och 2 bullar {s1} kr. "
                    f"2 koppar kaffe och 3 bullar kostar {s2} kr."
                ),
                info_box_style="blue",
                fraga="Bestäm priset för en kopp kaffe (x) och en bulle (y):",
                ratt_svar=[float(x_pris), float(y_pris)],
                input_typ="flera_text",
                svarstyp="punkt",
                flera_labels=["Kaffe x (kr) =", "Bulle y (kr) ="],
                undertext="Ställ upp ett ekvationssystem med två obekanta och lös ut x och y."
            )

        else:  # andragrad_rektangel_text
            # Kortaste sidan x, längden x + d, area = x * (x + d)
            d = random.choice([3, 4, 5, 6])
            x_kort = random.randint(4, 9)
            area = x_kort * (x_kort + d)
            return Uppgift(
                info_box_text=(
                    f"En rektangel har en sida som är {d} cm längre än den kortaste sidan. "
                    f"Rektangelns area är {area} cm²."
                ),
                info_box_style="blue",
                fraga="Beräkna längden på rektangelns kortaste sida (i cm):",
                ratt_svar=x_kort,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext="Beteckna kortaste sidan med x. Då är den andra sidan x + " + str(d) + " och arean x(x + " + str(d) + ")."
            )

    else:  # Nivå 2
        typ = random.choice(['konstant_dubbelrot', 'stangsel_max_area', 'extrempunkt_koordinater_prob'])

        if typ == 'konstant_dubbelrot':
            # x^2 + cx + c = k => x^2 + cx + (c - k) = 0
            # Dubbelrot i PQ-formeln: (c/2)^2 - (c - k) = 0 => låt c = 2*m => m^2 - 2m + k = 0
            # Väljer m och k så att c = 2*m blir ett tydligt heltal
            m_rot = random.choice([2, 3, 4, 5])
            c_val = 2 * m_rot
            k_val = 2 * m_rot - (m_rot ** 2)
            hl_str = f" = {k_val}" if k_val != 0 else " = 0"
            return Uppgift(
                info_box_text=f"Ekvationen x² + cx + c{hl_str} ska ha exakt en lösning (en dubbelrot).",
                info_box_style="blue",
                fraga="Bestäm värdet på konstanten c:",
                ratt_svar=c_val,
                input_typ="text",
                svarstyp="int",
                undertext="Samla alla termer i ett led och använd PQ-formeln: uttrycket under rottecknet ska vara 0."
            )

        elif typ == 'stangsel_max_area':
            # Rektangulär hage längs en rak vägg med total stängsellängd L (jämnt delbar med 4)
            # Om sidorna vinkelrätt mot väggen är x vardera, är parallella sidan L - 2x
            # A(x) = x(L - 2x) = Lx - 2x^2, max vid x = L/4, A_max = (L/4) * (L/2) = L^2 / 8
            halv_x = random.choice([4, 5, 6, 7, 8])
            L_stangsel = 4 * halv_x
            max_area = halv_x * (2 * halv_x)
            return Uppgift(
                info_box_text=(
                    f"En odlare har {L_stangsel} m stängsel för att inhägna en rektangulär odlingsyta "
                    f"längs en rak husvägg (husväggen kräver inget stängsel)."
                ),
                info_box_style="blue",
                fraga="Vilken är den största möjliga arean (i m²) som odlingsytan kan få?",
                ratt_svar=max_area,
                input_typ="text",
                svarstyp="int",
                suffix="m²",
                undertext="Kalla sidorna vinkelräta mot väggen för x. Då blir sidan parallell med väggen " + f"({L_stangsel} − 2x) m."
            )

        else:  # extrempunkt_koordinater_prob
            a = random.choice([1, -1])
            sym = random.randint(-3, 4)
            p = -2 * sym
            q = random.randint(-5, 6)
            funk_str = f"f(x) = {formatera_polynom([(a, 'x^2'), (a*p, 'x'), (q, '')])}"
            extrem_y = a * (sym**2) + a * p * sym + q
            typ_ord = "minimipunktens" if a > 0 else "maximipunktens"
            return Uppgift(
                info_box_text=f"En funktion ges av {funk_str}.",
                info_box_style="blue",
                fraga=f"Bestäm {typ_ord} koordinater (x och y):",
                ratt_svar=[float(sym), float(extrem_y)],
                input_typ="flera_text",
                svarstyp="punkt",
                flera_labels=["x =", "y ="],
                undertext="Bestäm symmetrilinjens ekvation för att få x-koordinaten och beräkna sedan f(x)."
            )
