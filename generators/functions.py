import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift
from utils import formatera_polynom

def skapa_rata_linjen_uppgift(niva: int) -> Uppgift:
    """Räta linjens ekvation y = kx + m."""
    if niva == 1:
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
    else:
        typ = random.choice(['tva_punkter', 'parallell'])
        if typ == 'tva_punkter':
            k = random.choice([-4, -3, -2, -1, 2, 3, 4])
            m = random.randint(-6, 6)
            x1 = random.randint(-3, 2)
            x2 = x1 + random.randint(2, 4)
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

def skapa_andragradsfunktion_uppgift(niva: int) -> Uppgift:
    """Andragradsfunktioner, nollställen, symmetrilinje och extremvärde."""
    if niva == 1:
        r1 = random.randint(-4, 2)
        r2 = r1 + random.choice([2, 4, 6])
        a = random.choice([1, -1])
        sym = (r1 + r2) // 2
        b = -a * (r1 + r2)
        c = a * r1 * r2
        
        typ = random.choice(['symmetrilinje_nollstallen', 'avlas_c', 'symmetrilinje_graf'])
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
        typ = random.choice(['andra_nollstallet', 'extremvarde_algebraiskt'])
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
        else:
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

def skapa_exp_potens_uppgift(niva: int) -> Uppgift:
    """Exponentialfunktioner och potensekvationer."""
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
        typ = random.choice(['potens_koeff', 'potens_brak_exp', 'baklanges_startvarde'])
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
