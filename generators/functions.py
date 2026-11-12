import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift
from utils import formatera_polynom

def skapa_rata_linjen_uppgift(niva: int) -> Uppgift:
    """Räta linjens ekvation y = kx + m (grafiskt och algebraiskt)."""
    if niva == 1:
        k = random.choice([-3, -2, -1, 1, 2, 3])
        m = random.randint(-4, 4)
        
        x_vals = np.linspace(-6, 6, 200)
        y_vals = k * x_vals + m
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode='lines',
            line=dict(color='#0056b3', width=3), hoverinfo='skip'
        ))
        fig.update_layout(
            xaxis=dict(title="x", range=[-6, 6], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
            yaxis=dict(title="y", range=[-6, 6], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
            height=360, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
        )
        
        facit = f"y = {formatera_polynom([(k, 'x'), (m, '')])}"
        return Uppgift(
            info_text="Studera den räta linjen i koordinatsystemet:",
            plotly_fig=fig,
            fraga="Bestäm linjens ekvation på formen y = kx + m:",
            ratt_svar=facit,
            input_typ="text",
            svarstyp="ekvation_linje",
            undertext="Avläs m-värdet (skärningen med y-axeln) och lutningen k (Δy / Δx)."
        )
    else:
        typ = random.choices(['tva_punkter', 'parallell'], weights=[0.7, 0.3], k=1)[0]
        k = random.choice([-3, -2, -1, 1, 2, 3])
        m = random.randint(-6, 6)
        x1 = random.randint(-4, 1)
        x2 = x1 + random.randint(2, 4)
        y1 = k * x1 + m
        y2 = k * x2 + m
        
        if typ == 'tva_punkter':
            facit = f"y = {formatera_polynom([(k, 'x'), (m, '')])}"
            return Uppgift(
                info_box_text=f"En rät linje går genom punkterna A({x1}, {y1}) och B({x2}, {y2}).",
                info_box_style="blue",
                fraga="Bestäm linjens ekvation på formen y = kx + m:",
                ratt_svar=facit,
                input_typ="text",
                svarstyp="ekvation_linje",
                undertext="Beräkna först lutningen k = (y₂ - y₁) / (x₂ - x₁) och bestäm sedan m."
            )
        else:
            ar_parallell = random.choice([True, False])
            k_given = k if ar_parallell else random.choice([v for v in [-3, -2, -1, 1, 2, 3] if v != k])
            m_given = m + random.choice([-4, -2, 2, 4])
            linje_str = f"y = {formatera_polynom([(k_given, 'x'), (m_given, '')])}"
            return Uppgift(
                info_box_text=f"Linje L₁ har ekvationen {linje_str}.<br>Linje L₂ går genom punkterna ({x1}, {y1}) och ({x2}, {y2}).",
                info_box_style="blue",
                fraga="Är linjerna L₁ och L₂ parallella?",
                ratt_svar="Ja" if ar_parallell else "Nej",
                alternativ=["Ja", "Nej"],
                input_typ="radio",
                svarstyp="string",
                undertext="Två linjer är parallella om de har samma riktningskoefficient (k-värde)."
            )

def skapa_andragradsfunktion_uppgift(niva: int) -> Uppgift:
    """Andragradsfunktioner, vertex, symmetrilinje och extremvärde."""
    if niva == 1:
        typ = random.choices(
            ['symmetrilinje_graf', 'symmetrilinje_nollstallen', 'extrempunkt_typ', 'avlas_c'],
            weights=[0.50, 0.20, 0.15, 0.15],
            k=1
        )[0]
        
        if typ == 'symmetrilinje_nollstallen':
            h = random.randint(-4, 4)
            avstand = random.randint(2, 6)
            x1 = h - avstand
            x2 = h + avstand
            return Uppgift(
                info_box_text=f"En andragradsfunktion har nollställena x₁ = {x1} och x₂ = {x2}.",
                info_box_style="green",
                fraga="Ange symmetrilinjens ekvation:",
                ratt_svar=f"x = {h}",
                input_typ="text",
                svarstyp="ekvation_x",
                undertext="Symmetrilinjen ligger mitt emellan nollställena. Skriv svaret som en ekvation (t.ex. x = 2)."
            )
            
        a = random.choice([-1, 1])
        h = random.randint(-3, 3)
        k = random.randint(-4, 4)
        c = a * (h ** 2) + k
        
        if typ == 'avlas_c':
            while abs(c) > 6:
                h = random.randint(-2, 2)
                k = random.randint(-4, 4)
                c = a * (h ** 2) + k
            x_min = min(-2, h - 4)
            x_max = max(2, h + 4)
            y_min = min(k - 2, c - 2, -1)
            y_max = max(k + 2, c + 2, 1)
            
            x_vals = np.linspace(x_min - 1, x_max + 1, 300)
            y_vals = a * (x_vals - h)**2 + k
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='blue', width=3), hoverinfo='skip'))
            fig.update_layout(
                xaxis=dict(title="x", range=[x_min, x_max], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                yaxis=dict(title="y", range=[y_min, y_max], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
                height=350, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
            )
            return Uppgift(
                info_text="Grafen visar andragradsfunktionen f(x) = ax² + bx + c:",
                plotly_fig=fig,
                fraga="Bestäm värdet på konstanten c med hjälp av grafen:",
                ratt_svar=c,
                input_typ="text",
                svarstyp="int",
                undertext="Konstanten c motsvarar funktionens skärning med y-axeln (där x = 0)."
            )
            
        # Förskjut visningsfönstret i sidled så att symmetrilinjen inte hamnar i mitten
        left_span = random.choice([2, 3, 4, 6, 7, 8])
        right_span = 10 - left_span
        x_min = h - left_span
        x_max = h + right_span
        if a > 0:
            y_min = min(k - 2, -1)
            y_max = y_min + 10
        else:
            y_max = max(k + 2, 1)
            y_min = y_max - 10
            
        x_vals = np.linspace(x_min - 1, x_max + 1, 300)
        y_vals = a * (x_vals - h)**2 + k
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='blue', width=3), hoverinfo='skip'))
        
        if typ == 'extrempunkt_typ':
            fig.add_trace(go.Scatter(x=[h], y=[k], mode='markers', marker=dict(size=10, color='red'), hoverinfo='skip'))
            
        fig.update_layout(
            xaxis=dict(title="x", range=[x_min, x_max], dtick=1, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
            yaxis=dict(title="y", range=[y_min, y_max], dtick=2, zeroline=True, zerolinewidth=2, zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'),
            height=350, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
        )
        
        if typ == 'symmetrilinje_graf':
            return Uppgift(
                info_text="Studera andragradsfunktionen i grafen:",
                plotly_fig=fig,
                fraga="Ange symmetrilinjens ekvation:",
                ratt_svar=f"x = {h}",
                input_typ="text",
                svarstyp="ekvation_x",
                undertext="Skriv svaret som en ekvation (t.ex. x = 2)."
            )
        else:
            svar_typ = "Minimipunkt" if a > 0 else "Maximipunkt"
            return Uppgift(
                info_text=f"Funktionen f(x) har sin extrempunkt i ({h}, {k}).",
                plotly_fig=fig,
                fraga="Har parabeln en maximipunkt eller minimipunkt?",
                ratt_svar=svar_typ,
                alternativ=["Minimipunkt", "Maximipunkt"],
                input_typ="radio",
                svarstyp="string"
            )
    else:
        typ = random.choice(['andra_nollstallet', 'extremvarde_algebraiskt'])
        if typ == 'andra_nollstallet':
            h = random.randint(-4, 5)
            avstand = random.randint(2, 6)
            x1 = h - avstand if random.choice([True, False]) else h + avstand
            x2 = 2 * h - x1
            return Uppgift(
                info_box_text=f"En andragradsfunktion har symmetrilinjen x = {h}.<br>Ett av funktionens nollställen är x₁ = {x1}.",
                info_box_style="green",
                fraga="Bestäm funktionens andra nollställe x₂:",
                ratt_svar=x2,
                input_typ="text",
                svarstyp="int",
                undertext="Nollställena ligger lika långt från symmetrilinjen på varsin sida."
            )
        else:
            a = random.choice([-1, 1])
            h = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            k = random.randint(-6, 6)
            b = -2 * a * h
            c = a * (h ** 2) + k
            uttryck = formatera_polynom([(a, 'x^2'), (b, 'x'), (c, '')])
            ord_typ = "minsta" if a > 0 else "största"
            return Uppgift(
                info_text="En andragradsfunktion ges av:",
                latex_text=f"f(x) = {uttryck}",
                fraga=f"Beräkna funktionens {ord_typ} värde algebraiskt:",
                ratt_svar=k,
                input_typ="text",
                svarstyp="int",
                undertext="Bestäm först symmetrilinjen x = -p/2 och sätt sedan in x-värdet i f(x)."
            )

def skapa_exp_potens_uppgift(niva: int) -> Uppgift:
    """Exponential- och potensfunktioner."""
    if niva == 1:
        typ = random.choice(['exp_modell', 'tolka_procent', 'potens_ekv'])
        if typ == 'exp_modell':
            start = random.choice([1000, 2000, 5000, 10000])
            procent = random.choice([3, 5, 8, 12])
            ar = random.randint(2, 5)
            ff = 1 + (procent / 100.0)
            svar = round(start * (ff ** ar), 2)
            info = f"Ett belopp på {start} kr sätts in på ett konto med en årlig ränta på {procent} %."
            return Uppgift(
                info_box_text=info,
                info_box_style="blue",
                fraga=f"Hur mycket pengar finns på kontot efter {ar} år?",
                ratt_svar=svar,
                input_typ="text",
                svarstyp="float",
                suffix="kr",
                undertext="Avrunda till två decimaler."
            )
        elif typ == 'tolka_procent':
            start = random.choice([15000, 25000, 40000, 80000])
            ar_minskning = random.choice([True, False])
            procent = random.choice([4, 6, 8, 12, 15, 18])
            ff = round(1 - procent / 100.0, 2) if ar_minskning else round(1 + procent / 100.0, 2)
            ff_str = f"{ff:g}".replace('.', ',')
            ord_str = "minskar" if ar_minskning else "ökar"
            return Uppgift(
                info_text="Värdet y (i kr) på ett föremål efter x år beskrivs av modellen:",
                latex_text=f"y = {start} \\cdot {ff_str}^x",
                fraga=f"Med hur många procent {ord_str} värdet per år?",
                ratt_svar=procent,
                input_typ="text",
                svarstyp="procent",
                suffix="%",
                undertext="Jämför förändringsfaktorn med 1 (100 %)."
            )
        else:
            n = random.choice([2, 3, 4])
            x_val = random.randint(2, 8) if n == 2 else random.randint(2, 5)
            rhs = x_val ** n
            fraga_txt = "Bestäm det positiva värdet på x:" if n % 2 == 0 else "Lös ekvationen:"
            return Uppgift(
                info_text="Lös potensekvationen:",
                latex_text=f"x^{n} = {rhs}",
                fraga=fraga_txt,
                ratt_svar=x_val,
                input_typ="text",
                svarstyp="int"
            )
    else:
        typ = random.choice(['baklanges_startvarde', 'potens_koeff', 'potens_brak_exp'])
        if typ == 'baklanges_startvarde':
            ar_minskning = random.choice([True, False])
            procent = random.choice([10, 20])
            ar = random.choice([2, 3])
            start = random.choice([10000, 20000, 30000])
            ff = round(1 - procent / 100.0, 2) if ar_minskning else round(1 + procent / 100.0, 2)
            slutvarde = int(round(start * (ff ** ar)))
            ord_str = "minskat" if ar_minskning else "ökat"
            return Uppgift(
                info_box_text=f"Värdet på en maskin har {ord_str} med {procent} % per år i {ar} år och är nu {slutvarde} kr.",
                info_box_style="blue",
                fraga="Beräkna maskinens ursprungliga värde:",
                ratt_svar=start,
                input_typ="text",
                svarstyp="int",
                suffix="kr",
                undertext="Ställ upp ekvationen C · aˣ = slutvärde och lös ut startvärdet C."
            )
        elif typ == 'potens_koeff':
            a = random.choice([2, 3, 4, 5])
            n = random.choice([2, 3, 4])
            x_val = random.randint(2, 6) if n == 2 else random.randint(2, 4)
            rhs = a * (x_val ** n)
            fraga_txt = "Bestäm det positiva värdet på x:" if n % 2 == 0 else "Lös ekvationen:"
            return Uppgift(
                info_text="Lös potensekvationen:",
                latex_text=f"{a}x^{n} = {rhs}",
                fraga=fraga_txt,
                ratt_svar=x_val,
                input_typ="text",
                svarstyp="int",
                undertext=f"Dividera först båda leden med {a}."
            )
        else:
            rot_typ = random.choice([2, 3])
            if rot_typ == 2:
                k = random.randint(3, 9)
                ratt = k ** 2
                exp_latex = "x^{1/2}"
            else:
                k = random.randint(2, 5)
                ratt = k ** 3
                exp_latex = "x^{1/3}"
            return Uppgift(
                info_text="Lös potensekvationen:",
                latex_text=f"{exp_latex} = {k}",
                fraga="Bestäm värdet på x:",
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="int",
                undertext=f"Upphöj båda leden till {rot_typ}."
            )
