import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift
from utils import formatera_polynom


def _formatera_olikhet_intervall(var: str, low_val: int, low_sluten: bool, high_val: int, high_sluten: bool) -> str:
    """Formaterar ett dubbelt intervall som t.ex. '2 ≤ x < 10'."""
    op1 = "≤" if low_sluten else "<"
    op2 = "≤" if high_sluten else "<"
    return f"{low_val} {op1} {var} {op2} {high_val}"


def _bygg_olikhets_alternativ(var: str, low_val: int, low_sluten: bool, high_val: int, high_sluten: bool) -> list[str]:
    """Skapar rätt olikhetsintervall och tre distraktorer med olika kombinationer av < och ≤."""
    ratt = _formatera_olikhet_intervall(var, low_val, low_sluten, high_val, high_sluten)
    kandidater = [
        _formatera_olikhet_intervall(var, low_val, True, high_val, True),
        _formatera_olikhet_intervall(var, low_val, False, high_val, False),
        _formatera_olikhet_intervall(var, low_val, True, high_val, False),
        _formatera_olikhet_intervall(var, low_val, False, high_val, True),
    ]
    unika = []
    for k in [ratt] + kandidater:
        if k not in unika:
            unika.append(k)
    return unika[:4]


def skapa_rata_linjen_uppgift(niva: int) -> Uppgift:
    """Räta linjens ekvation y = kx + m."""
    if niva == 1:
        typ = random.choice(['avlas_graf', 'punkt_pa_linje', 'skarning_axel', 'k_och_punkt', 'tva_punkter'])

        if typ == 'avlas_graf':
            k = random.choice([-3, -2, -1, 1, 2, 3])
            m = random.randint(-4, 4)
            x_vals = np.linspace(-5, 5, 100)
            y_vals = k * x_vals + m

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
            fig.update_layout(
                xaxis=dict(title="x", range=[-5, 5], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                yaxis=dict(title="y", range=[-6, 6], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                height=340, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
            )
            return Uppgift(
                info_text="Bestäm ekvationen för den räta linjen i diagrammet:",
                plotly_fig=fig,
                fraga="Skriv linjens ekvation på formen y = kx + m:",
                ratt_svar=f"y={k}x+{m}",
                input_typ="text",
                svarstyp="ekvation_linje",
                undertext="Bestäm linjens lutning (k) och skärning med y-axeln (m) ur grafen."
            )

        elif typ == 'punkt_pa_linje':
            k = random.choice([-4, -3, -2, 2, 3, 4])
            m = random.choice([x for x in range(-7, 8) if x != 0])
            x_val = random.choice([x for x in range(-5, 6) if x != 0])
            y_val = k * x_val + m
            linje_str = f"y = {formatera_polynom([(k, 'x'), (m, '')])}"

            if random.choice(['berakna_y', 'berakna_x']) == 'berakna_y':
                return Uppgift(
                    info_box_text=f"En rät linje har ekvationen {linje_str}. En punkt på linjen har x-koordinaten {x_val}.",
                    info_box_style="blue",
                    fraga="Beräkna punktens y-koordinat:",
                    ratt_svar=y_val,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Sätt in det givna x-värdet i linjens ekvation."
                )
            else:
                return Uppgift(
                    info_box_text=f"En rät linje har ekvationen {linje_str}. En punkt på linjen har y-koordinaten {y_val}.",
                    info_box_style="blue",
                    fraga="Beräkna punktens x-koordinat:",
                    ratt_svar=x_val,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Sätt in det givna y-värdet i linjens ekvation och lös ekvationen."
                )

        elif typ == 'skarning_axel':
            axel = random.choice(['x', 'y'])
            if axel == 'x':
                k = random.choice([-3, -2, -1, 1, 2, 3])
                x0 = random.choice([x for x in range(-5, 6) if x != 0])
                m = -k * x0
                linje_str = f"y = {formatera_polynom([(k, 'x'), (m, '')])}"
                return Uppgift(
                    info_box_text=f"En rät linje har ekvationen {linje_str}.",
                    info_box_style="blue",
                    fraga="Bestäm koordinaterna för linjens skärningspunkt med x-axeln:",
                    ratt_svar=[float(x0), 0.0],
                    input_typ="flera_text",
                    svarstyp="punkt",
                    flera_labels=["x =", "y ="],
                    undertext="Fundera på vilket y-värde alla punkter på x-axeln har."
                )
            else:
                k = random.choice([-4, -3, -2, 2, 3, 4])
                m = random.choice([x for x in range(-7, 8) if x != 0])
                linje_str = f"y = {formatera_polynom([(k, 'x'), (m, '')])}"
                return Uppgift(
                    info_box_text=f"En rät linje har ekvationen {linje_str}.",
                    info_box_style="blue",
                    fraga="Bestäm koordinaterna för linjens skärningspunkt med y-axeln:",
                    ratt_svar=[0.0, float(m)],
                    input_typ="flera_text",
                    svarstyp="punkt",
                    flera_labels=["x =", "y ="],
                    undertext="Fundera på vilket x-värde alla punkter på y-axeln har."
                )

        elif typ == 'k_och_punkt':
            k = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            m = random.randint(-6, 6)
            px = random.choice([x for x in range(-4, 5) if x != 0])
            py = k * px + m
            return Uppgift(
                info_box_text=f"En rät linje har riktningskoefficienten k = {k} och går genom punkten ({px}, {py}).",
                info_box_style="blue",
                fraga="Bestäm linjens ekvation på formen y = kx + m:",
                ratt_svar=f"y={k}x+{m}",
                input_typ="text",
                svarstyp="ekvation_linje",
                undertext="Sätt in k-värdet och punktens koordinater i räta linjens ekvation."
            )

        else:
            k = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            m = random.randint(-6, 6)
            x1 = random.randint(-3, 2)
            x2 = x1 + random.randint(1, 4)
            y1, y2 = k * x1 + m, k * x2 + m
            return Uppgift(
                info_box_text=f"En rät linje går genom punkterna ({x1}, {y1}) och ({x2}, {y2}).",
                info_box_style="blue",
                fraga="Bestäm linjens ekvation på formen y = kx + m:",
                ratt_svar=f"y={k}x+{m}",
                input_typ="text",
                svarstyp="ekvation_linje",
                undertext="Bestäm först riktningskoefficienten k och därefter m-värdet."
            )

    else:
        typ = random.choice([
            'tva_punkter_brak',
            'parallell',
            'skarning_allman_form',
            'k_och_punkt_brak',
            'vinkelrat_linje'
        ])

        if typ == 'tva_punkter_brak':
            k_num = random.choice([-5, -3, -1, 1, 3, 5])
            k_den = 2
            m = random.randint(-5, 5)
            x1 = random.choice([-4, -2, 0, 2])
            x2 = x1 + random.choice([2, 4])
            y1 = (k_num * x1) // k_den + m
            y2 = (k_num * x2) // k_den + m
            return Uppgift(
                info_box_text=f"En rät linje går genom punkterna ({x1}, {y1}) och ({x2}, {y2}).",
                info_box_style="blue",
                fraga="Bestäm linjens ekvation på formen y = kx + m:",
                ratt_svar=f"y=({k_num}/{k_den})x+{m}",
                input_typ="text",
                svarstyp="ekvation_linje",
                undertext="Bestäm först riktningskoefficienten k och därefter m-värdet."
            )

        elif typ == 'parallell':
            k = random.choice([-3, -2, 2, 3, 4])
            m1 = random.randint(-5, 5)
            m2 = random.choice([x for x in range(-6, 7) if x != m1])
            px = random.randint(-3, 3)
            py = k * px + m2
            linje1_str = f"y = {formatera_polynom([(k, 'x'), (m1, '')])}"
            return Uppgift(
                info_box_text=f"En rät linje L är parallell med linjen {linje1_str} och går genom punkten ({px}, {py}).",
                info_box_style="blue",
                fraga="Bestäm ekvationen för linjen L på formen y = kx + m:",
                ratt_svar=f"y={k}x+{m2}",
                input_typ="text",
                svarstyp="ekvation_linje",
                undertext="Jämför linjernas lutning."
            )

        elif typ == 'skarning_allman_form':
            a = random.choice([2, 3, 4])
            b = random.choice([-4, -3, -2, 2, 3, 4])
            mult = random.choice([-2, -1, 1, 2, 3])
            c = a * abs(b) * mult
            ekv_str = f"{formatera_polynom([(a, 'x'), (b, 'y')])} = {c}"
            axel = random.choice(['x', 'y'])
            if axel == 'x':
                x0 = c // a
                ratt = [float(x0), 0.0]
            else:
                y0 = c // b
                ratt = [0.0, float(y0)]
            return Uppgift(
                info_box_text=f"En rät linje beskrivs av ekvationen {ekv_str}.",
                info_box_style="blue",
                fraga=f"Bestäm koordinaterna för linjens skärningspunkt med {axel}-axeln:",
                ratt_svar=ratt,
                input_typ="flera_text",
                svarstyp="punkt",
                flera_labels=["x =", "y ="],
                undertext="Sätt in 0 för den variabel som är noll på axeln och lös ekvationen."
            )

        elif typ == 'vinkelrat_linje':
            k1 = random.choice([-2, 2])
            k2_num = 1 if k1 < 0 else -1
            k2_den = 2
            m1 = random.randint(-4, 4)
            m2 = random.randint(-4, 4)
            px = random.choice([-4, -2, 2, 4])
            py = (k2_num * px) // k2_den + m2
            linje1_str = f"y = {formatera_polynom([(k1, 'x'), (m1, '')])}"
            return Uppgift(
                info_box_text=f"En rät linje är vinkelrät mot linjen {linje1_str} och går genom punkten ({px}, {py}).",
                info_box_style="blue",
                fraga="Bestäm linjens ekvation på formen y = kx + m:",
                ratt_svar=f"y=({k2_num}/{k2_den})x+{m2}",
                input_typ="text",
                svarstyp="ekvation_linje",
                undertext="För vinkelräta linjer gäller k₁ · k₂ = −1."
            )

        else:
            k_num = random.choice([-3, -1, 1, 3])
            k_den = 2
            k_val = k_num / k_den
            m = random.randint(-5, 5)
            px = random.choice([-4, -2, 2, 4])
            py = int(k_val * px + m)
            k_str = f"{k_num}/{k_den}"
            return Uppgift(
                info_box_text=f"En rät linje har riktningskoefficienten k = {k_str} och går genom punkten ({px}, {py}).",
                info_box_style="blue",
                fraga="Bestäm linjens ekvation på formen y = kx + m:",
                ratt_svar=f"y=({k_num}/{k_den})x+{m}",
                input_typ="text",
                svarstyp="ekvation_linje",
                undertext="Sätt in k-värdet och punktens koordinater för att bestämma m."
            )


def skapa_andragradsfunktion_uppgift(niva: int) -> Uppgift:
    """Andragradsfunktioner, nollställen, symmetrilinje, extrempunkt, definitions-/värdemängd och grafer."""
    if niva == 1:
        r1 = random.randint(-4, 2)
        r2 = r1 + random.choice([2, 4, 6])
        a = random.choice([1, -1])
        sym = (r1 + r2) // 2
        b = -a * (r1 + r2)
        c = a * r1 * r2

        typ = random.choice(['symmetrilinje_nollstallen', 'avlas_c', 'symmetrilinje_graf', 'def_vardemangd_graf'])
        if typ == 'symmetrilinje_nollstallen':
            funk_str = f"f(x) = {formatera_polynom([(a, 'x^2'), (b, 'x'), (c, '')])}"
            return Uppgift(
                info_box_text=f"Andragradsfunktionen {funk_str} har nollställena x₁ = {r1} och x₂ = {r2}.",
                info_box_style="blue",
                fraga="Ange ekvationen för funktionens symmetrilinje:",
                ratt_svar=f"x={sym}",
                input_typ="text",
                svarstyp="ekvation_x",
                undertext="Utnyttja parabelns symmetri. Skriv svaret som en ekvation (t.ex. x = 2)."
            )
        elif typ == 'avlas_c':
            x_vals = np.linspace(sym - 4, sym + 4, 200)
            y_vals = a * x_vals**2 + b * x_vals + c
            y_min = min(-4, int(np.min(y_vals)) - 1)
            y_max = max(4, int(np.max(y_vals)) + 1)

            if abs(c) <= 10 and (y_max - y_min) <= 18:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
                fig.update_layout(
                    xaxis=dict(title="x", range=[sym - 4, sym + 4], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                    yaxis=dict(title="y", range=[y_min, y_max], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                    height=350, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
                )
                return Uppgift(
                    info_text="Bilden visar grafen till en andragradsfunktion på formen f(x) = ax² + bx + c:",
                    plotly_fig=fig,
                    fraga="Bestäm värdet på konstanten c:",
                    ratt_svar=c,
                    input_typ="text",
                    svarstyp="int",
                    undertext="Fundera på vad f(0) blir."
                )

        elif typ == 'def_vardemangd_graf':
            # Begränsad kurva med tydliga fyllda (sluten: ≤) och ofyllda (öppen: <) ändpunkter
            x_start = random.randint(1, 3)
            x_slut = x_start + random.randint(5, 8)
            x_sluten = random.choice([True, False])
            y_sluten = random.choice([True, False])

            # Väljer y-värden så att ändpunkterna direkt ger min- och maxvärde för y
            minskar = random.choice([True, False])
            if minskar:
                y_start = random.randint(7, 10)
                y_slut = random.randint(1, 4)
                # (x_start, y_start) är vänster/övre punkt, (x_slut, y_slut) är höger/undre punkt
                p1_sluten, p2_sluten = x_sluten, y_sluten
                y_low, y_high = y_slut, y_start
                y_low_sluten, y_high_sluten = p2_sluten, p1_sluten
            else:
                y_start = random.randint(1, 4)
                y_slut = random.randint(7, 10)
                p1_sluten, p2_sluten = y_sluten, x_sluten
                y_low, y_high = y_start, y_slut
                y_low_sluten, y_high_sluten = p1_sluten, p2_sluten

            # Mjuk kurva mellan (x_start, y_start) och (x_slut, y_slut)
            t = np.linspace(0, 1, 150)
            x_kurva = x_start + t * (x_slut - x_start)
            y_kurva = y_start + (y_slut - y_start) * (t ** 1.4)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_kurva, y=y_kurva, mode='lines',
                line=dict(color='#d9534f', width=3), hoverinfo='skip'
            ))

            # Första ändpunkten: fylld = ≤ (ingår), ofylld = < (ingår inte)
            fig.add_trace(go.Scatter(
                x=[x_start], y=[y_start], mode='markers',
                marker=dict(
                    size=10,
                    color='#d9534f' if p1_sluten else 'white',
                    line=dict(color='#d9534f', width=2.5)
                ),
                hoverinfo='skip'
            ))

            # Andra ändpunkten
            fig.add_trace(go.Scatter(
                x=[x_slut], y=[y_slut], mode='markers',
                marker=dict(
                    size=10,
                    color='#d9534f' if p2_sluten else 'white',
                    line=dict(color='#d9534f', width=2.5)
                ),
                hoverinfo='skip'
            ))

            fig.update_layout(
                xaxis=dict(title="x", range=[0, x_slut + 2], dtick=1, zeroline=True, zerolinewidth=1.5, zerolinecolor='black', showgrid=True, gridcolor='#e8e8e8'),
                yaxis=dict(title="y", range=[0, max(y_start, y_slut) + 2], dtick=1, zeroline=True, zerolinewidth=1.5, zerolinecolor='black', showgrid=True, gridcolor='#e8e8e8'),
                height=360, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
            )

            sok_def = random.choice([True, False])
            if sok_def:
                ratt_svar = _formatera_olikhet_intervall("x", x_start, x_sluten, x_slut, not x_sluten)
                alts = _bygg_olikhets_alternativ("x", x_start, x_sluten, x_slut, not x_sluten)
                fraga_txt = "Vilken är funktionens definitionsmängd?"
            else:
                ratt_svar = _formatera_olikhet_intervall("y", y_low, y_low_sluten, y_high, y_high_sluten)
                alts = _bygg_olikhets_alternativ("y", y_low, y_low_sluten, y_high, y_high_sluten)
                fraga_txt = "Vilken är funktionens värdemängd?"

            random.shuffle(alts)
            return Uppgift(
                info_text="Grafen visar en funktion med markerade ändpunkter. Fylld cirkel betyder att gränsen ingår (≤), ofylld cirkel att den inte ingår (<):",
                plotly_fig=fig,
                fraga=fraga_txt,
                ratt_svar=ratt_svar,
                alternativ=alts,
                input_typ="radio",
                svarstyp="string",
                undertext="Definitionsmängden avser tillåtna x-värden, värdemängden avser möjliga y-värden."
            )

        x_vals = np.linspace(sym - 4, sym + 4, 200)
        y_vals = a * x_vals**2 + b * x_vals + c
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
        fig.update_layout(
            xaxis=dict(title="x", range=[sym - 4, sym + 4], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
            yaxis=dict(title="y", dtick=2, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
            height=350, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
        )
        return Uppgift(
            info_text="Studera andragradskurvan nedan:",
            plotly_fig=fig,
            fraga="Ange ekvationen för kurvans symmetrilinje:",
            ratt_svar=f"x={sym}",
            input_typ="text",
            svarstyp="ekvation_x",
            undertext="Skriv svaret som en ekvation (t.ex. x = 2)."
        )

    else:
        typ = random.choice([
            'andra_nollstallet',
            'extrempunkt_koordinater',
            'extremvarde_algebraiskt',
            'faktorform_nollstallen',
            'parameter_genom_punkt',
            'skarning_linje_parabel',
            'graf_positiv_negativ'
        ])

        if typ == 'andra_nollstallet':
            sym = random.randint(-3, 4)
            avstand = random.randint(2, 5)
            r1 = sym - avstand
            r2 = sym + avstand
            if random.choice([True, False]):
                r1, r2 = r2, r1
            return Uppgift(
                info_box_text=f"En andragradsfunktion har symmetrilinjen x = {sym}. Ett av funktionens nollställen är x = {r1}.",
                info_box_style="blue",
                fraga="Bestäm funktionens andra nollställe:",
                ratt_svar=r2,
                input_typ="text",
                svarstyp="int",
                undertext="Utnyttja parabelns symmetri kring symmetrilinjen."
            )

        elif typ == 'extrempunkt_koordinater':
            # Bestäm extrempunktens koordinater (x, y)
            a = random.choice([1, -1])
            sym = random.randint(-4, 4)
            p = -2 * sym
            q = random.randint(-6, 6)
            funk_str = f"f(x) = {formatera_polynom([(a, 'x^2'), (a*p, 'x'), (q, '')])}"
            extrem_y = a * (sym**2) + a * p * sym + q
            punkt_typ = "minimipunktens" if a > 0 else "maximipunktens"
            return Uppgift(
                info_box_text=f"Givet andragradsfunktionen {funk_str}.",
                info_box_style="blue",
                fraga=f"Bestäm koordinaterna för {punkt_typ} (x och y):",
                ratt_svar=[float(sym), float(extrem_y)],
                input_typ="flera_text",
                svarstyp="punkt",
                flera_labels=["x =", "y ="],
                undertext="Börja med att bestämma x-koordinaten via symmetrilinjen och sätt sedan in i f(x)."
            )

        elif typ == 'extremvarde_algebraiskt':
            a = random.choice([1, -1])
            sym = random.randint(-4, 4)
            p = -2 * sym
            q = random.randint(-6, 6)
            funk_str = f"f(x) = {formatera_polynom([(a, 'x^2'), (a*p, 'x'), (q, '')])}"
            extrem_y = a * (sym**2) + a * p * sym + q
            typ_ord = "minimivärde" if a > 0 else "maximivärde"
            return Uppgift(
                info_box_text=f"Givet andragradsfunktionen {funk_str}.",
                info_box_style="blue",
                fraga=f"Beräkna funktionens {typ_ord} (y-värdet i extrempunkten):",
                ratt_svar=extrem_y,
                input_typ="text",
                svarstyp="int",
                undertext="Börja med att bestämma funktionens symmetrilinje."
            )

        elif typ == 'faktorform_nollstallen':
            a = random.choice([1, 2, -1, -2])
            r1 = random.choice([-4, -3, -2, -1, 1, 2, 3])
            r2 = random.choice([x for x in [-4, -3, -2, -1, 1, 2, 3, 4] if x != r1])
            f1 = f"(x - {r1})" if r1 > 0 else f"(x + {abs(r1)})"
            f2 = f"(x - {r2})" if r2 > 0 else f"(x + {abs(r2)})"
            a_str = "" if a == 1 else ("-" if a == -1 else str(a))
            funk_str = f"f(x) = {a_str}{f1}{f2}"
            return Uppgift(
                info_box_text=f"Givet andragradsfunktionen {funk_str}.",
                info_box_style="blue",
                fraga="Bestäm funktionens två nollställen:",
                ratt_svar=sorted([float(r1), float(r2)]),
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x₁ =", "x₂ ="],
                undertext="Nollställena fås där f(x) = 0, dvs. när minst en faktor är lika med 0."
            )

        elif typ == 'parameter_genom_punkt':
            c_val = random.choice([-6, -4, -2, 1, 3, 5])
            a_val = random.choice([-5, -3, -2, 2, 3, 5])
            px = random.choice([-3, -2, 2, 3])
            py = px**2 + a_val * px + c_val
            funk_str = f"f(x) = {formatera_polynom([(1, 'x^2'), (1, 'ax'), (c_val, '')])}"
            return Uppgift(
                info_box_text=f"Andragradsfunktionen {funk_str} går genom punkten ({px}, {py}).",
                info_box_style="blue",
                fraga="Bestäm värdet på konstanten a:",
                ratt_svar=a_val,
                input_typ="text",
                svarstyp="int",
                undertext="Sätt in f(px) = py i funktionsuttrycket och lös ut a."
            )

        elif typ == 'skarning_linje_parabel':
            x1 = random.choice([-3, -2, -1, 1])
            x2 = random.choice([x for x in [-1, 1, 2, 3, 4] if x != x1])
            k_lin = random.choice([-2, -1, 1, 2, 3])
            m_lin = random.choice([-3, -1, 1, 2, 4])
            b_par = k_lin - (x1 + x2)
            c_par = m_lin + x1 * x2
            f_str = f"f(x) = {formatera_polynom([(1, 'x^2'), (b_par, 'x'), (c_par, '')])}"
            g_str = f"g(x) = {formatera_polynom([(k_lin, 'x'), (m_lin, '')])}"
            return Uppgift(
                info_box_text=f"Två funktioner ges av {f_str} och {g_str}.",
                info_box_style="blue",
                fraga="Bestäm x-koordinaterna för de punkter där f(x) = g(x):",
                ratt_svar=sorted([float(x1), float(x2)]),
                input_typ="flera_text",
                svarstyp="array_float",
                flera_labels=["x₁ =", "x₂ ="],
                undertext="Sätt f(x) = g(x), samla allt i ett led och lös andragradsekvationen."
            )

        else:
            r1 = random.randint(-3, 0)
            r2 = r1 + random.choice([2, 3, 4])
            a = random.choice([1, -1])
            b = -a * (r1 + r2)
            c = a * r1 * r2
            sym = (r1 + r2) / 2.0

            x_vals = np.linspace(sym - 4, sym + 4, 200)
            y_vals = a * x_vals**2 + b * x_vals + c
            y_min = min(-5, int(np.min(y_vals)) - 1)
            y_max = max(5, int(np.max(y_vals)) + 1)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
            fig.update_layout(
                xaxis=dict(title="x", range=[sym - 4, sym + 4], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                yaxis=dict(title="y", range=[y_min, y_max], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                height=350, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
            )

            soker_positiv = a > 0
            if soker_positiv:
                fraga_text = "För vilka x-värden gäller att f(x) > 0?"
                ratt_val = f"x < {r1} eller x > {r2}"
                alts = [
                    f"x < {r1} eller x > {r2}",
                    f"{r1} < x < {r2}",
                    f"x > {r1}",
                    f"x < {r2}"
                ]
            else:
                fraga_text = "För vilka x-värden gäller att f(x) > 0?"
                ratt_val = f"{r1} < x < {r2}"
                alts = [
                    f"{r1} < x < {r2}",
                    f"x < {r1} eller x > {r2}",
                    f"x < {r1}",
                    f"x > {r2}"
                ]
            random.shuffle(alts)

            return Uppgift(
                info_text="Grafen visar funktionen y = f(x):",
                plotly_fig=fig,
                fraga=fraga_text,
                ratt_svar=ratt_val,
                alternativ=alts,
                input_typ="radio",
                svarstyp="string",
                undertext="Avgör var grafen ligger ovanför x-axeln (y > 0) i förhållande till nollställena."
            )


def skapa_exp_potens_uppgift(niva: int) -> Uppgift:
    """Exponentialfunktioner, byte av tidsenhet och potensekvationer."""
    if niva == 1:
        typ = random.choice(['exp_modell', 'tolka_procent'])
        if typ == 'exp_modell':
            start = random.choice([15000, 20000, 25000, 40000, 50000])
            p_var = random.choice([4, 5, 6, 8, 12])
            ar = random.randint(3, 6)
            typ_forandring = random.choice(['okar', 'minskar'])
            if typ_forandring == 'okar':
                ff = 1 + p_var / 100
                text = f"En population på {start} individer ökar med {p_var} % per år."
            else:
                ff = 1 - p_var / 100
                text = f"Värdet på en maskin som kostar {start} kr minskar med {p_var} % per år."
            ratt_svar = round(start * (ff ** ar), 2)
            return Uppgift(
                info_box_text=text,
                info_box_style="blue",
                fraga=f"Beräkna värdet efter {ar} år:",
                ratt_svar=ratt_svar,
                input_typ="text",
                svarstyp="float",
                tolerans=1.0,
                undertext="Avrunda till två decimaler."
            )
        else:
            start = random.choice([1200, 2500, 8000, 15000])
            procent = random.choice([3, 4, 7, 12, 15])
            okar = random.choice([True, False])
            if okar:
                ff = round(1 + procent / 100, 2)
                ratt = f"Ökar med {procent} % per år"
            else:
                ff = round(1 - procent / 100, 2)
                ratt = f"Minskar med {procent} % per år"

            alts = [
                f"Ökar med {procent} % per år",
                f"Minskar med {procent} % per år",
                f"Ökar med {int(round(ff * 100))} % per år",
                f"Minskar med {int(round(ff * 100))} % per år"
            ]
            random.shuffle(alts)
            return Uppgift(
                info_box_text=f"Värdet y (i kr) på en aktieportfölj efter x år beskrivs av modellen y = {start} · {ff}ˣ.",
                info_box_style="blue",
                fraga="Hur förändras portföljens värde varje år?",
                ratt_svar=ratt,
                alternativ=alts,
                input_typ="radio",
                svarstyp="string",
                undertext="Studera förändringsfaktorn i modellen."
            )
    else:
        typ = random.choice([
            'potens_koeff',
            'potens_brak_exp',
            'baklanges_startvarde',
            'forandring_ur_formel',
            'byte_tidsenhet'
        ])

        if typ == 'baklanges_startvarde':
            start = random.choice([2000, 4000, 5000, 8000, 10000])
            p_var = random.choice([5, 10, 20])
            ar = random.randint(2, 4)
            okar = random.choice([True, False])
            ff = (1 + p_var / 100) if okar else (1 - p_var / 100)
            slut = round(start * (ff ** ar), 2)
            verb = "ökat" if okar else "minskat"
            return Uppgift(
                info_box_text=f"Värdet på en fond har {verb} med {p_var} % per år i {ar} år. Idag är fonden värd {slut} kr.",
                info_box_style="blue",
                fraga="Hur mycket var fonden värd från början (för " + str(ar) + " år sedan)?",
                ratt_svar=float(start),
                input_typ="text",
                svarstyp="float",
                tolerans=1.0,
                suffix="kr",
                undertext="Ställ upp en ekvation med hjälp av förändringsfaktorn."
            )

        elif typ == 'potens_koeff':
            a = random.choice([2, 3, 4, 5])
            exp = random.choice([3, 4])
            x_sol = random.randint(2, 5)
            hl = a * (x_sol ** exp)
            return Uppgift(
                info_text="Lös potensekvationen:",
                latex_text=f"{a}x^{{{exp}}} = {hl}",
                fraga="Ange det positiva värdet på x:",
                ratt_svar=x_sol,
                input_typ="text",
                svarstyp="int",
                undertext="Isolera potensen innan du löser ekvationen."
            )

        elif typ == 'forandring_ur_formel':
            start = random.choice([500, 1200, 3500, 8000])
            procent = random.choice([6, 8, 12, 15, 25])
            okar = random.choice([True, False])
            if okar:
                ff = round(1 + procent / 100, 2)
                verb = "ökar"
            else:
                ff = round(1 - procent / 100, 2)
                verb = "minskar"
            ff_str = str(ff).replace('.', ',')
            return Uppgift(
                info_box_text=f"En storhet beskrivs av exponentialfunktionen y = {start} · {ff_str}ˣ, där x är tiden i år.",
                info_box_style="blue",
                fraga=f"Med hur många procent {verb} storheten varje år? (Ange ett positivt tal)",
                ratt_svar=float(procent),
                input_typ="text",
                svarstyp="float",
                tolerans=0.1,
                suffix="%",
                undertext=f"Förändringsfaktorn är {ff_str}. Jämför med 1."
            )

        elif typ == 'byte_tidsenhet':
            # Förändring per månad -> förändringsfaktor per år (12 månader)
            procent = random.choice([2, 3, 4, 5, 8, 10])
            minskar = random.choice([True, False])
            ff_manad = (1 - procent / 100) if minskar else (1 + procent / 100)
            ff_ar = round(ff_manad ** 12, 2)
            verb = "minskar" if minskar else "ökar"
            return Uppgift(
                info_box_text=f"En storhet {verb} med {procent} % varje månad.",
                info_box_style="blue",
                fraga="Bestäm förändringsfaktorn per år (avrunda till två decimaler):",
                ratt_svar=ff_ar,
                input_typ="text",
                svarstyp="float",
                tolerans=0.02,
                undertext=f"Månadsförändringsfaktorn är {str(round(ff_manad, 2)).replace('.', ',')}. På 1 år (12 månader) upphöjs den till 12."
            )

        else:
            namnare = random.choice([2, 3])
            bas = random.randint(2, 5)
            hl = bas
            x_sol = bas ** namnare
            return Uppgift(
                info_text="Lös potensekvationen:",
                latex_text=f"x^{{1/{namnare}}} = {hl}",
                fraga="Ange värdet på x:",
                ratt_svar=x_sol,
                input_typ="text",
                svarstyp="int",
                undertext="Använd potenslagarna för att få x ensamt."
            )
