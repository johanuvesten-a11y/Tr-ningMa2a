import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift
from utils import formatera_polynom

def skapa_andragradsfunktion_uppgift(niva: int) -> Uppgift:
    """Andragradsfunktioner, vertex och symmetrilinje."""
    a = random.choice([-1, 1])
    h = random.randint(-4, 4)  # Symmetrilinje x = h
    k = random.randint(-5, 5)  # Extremvärde y = k
    
    x_vals = np.linspace(h - 5, h + 5, 200)
    y_vals = a * (x_vals - h)**2 + k
    
    typ = random.choice(['symmetrilinje', 'extrempunkt_typ'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals, mode='lines',
        line=dict(color='blue', width=3), hoverinfo='skip'
    ))
    
    if typ == 'extrempunkt_typ':
        fig.add_trace(go.Scatter(
            x=[h], y=[k], mode='markers',
            marker=dict(size=10, color='red'), hoverinfo='skip'
        ))
        
    fig.update_layout(
        xaxis=dict(
            title="x", dtick=1, zeroline=True, zerolinewidth=2,
            zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'
        ),
        yaxis=dict(
            title="y", dtick=2, zeroline=True, zerolinewidth=2,
            zerolinecolor='black', showgrid=True, gridcolor='#e0e0e0'
        ),
        height=350, margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white', showlegend=False, hovermode=False
    )
    
    if typ == 'symmetrilinje':
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
        alts = ["Minimipunkt", "Maximipunkt"]
        return Uppgift(
            info_text=f"Funktionen f(x) har sin extrempunkt i ({h}, {k}).",
            plotly_fig=fig,
            fraga="Har parabeln en maximipunkt eller minimipunkt?",
            ratt_svar=svar_typ,
            alternativ=alts,
            input_typ="radio",
            svarstyp="string"
        )

def skapa_exp_potens_uppgift(niva: int) -> Uppgift:
    """Exponential- och potensfunktioner."""
    typ = random.choice(['exp_modell', 'potens_ekv'])
    
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
    else:
        x_val = random.randint(2, 6)
        n = random.choice([3, 4])
        rhs = x_val ** n
        
        return Uppgift(
            info_text="Lös potenssambandet:",
            latex_text=f"x^{n} = {rhs}",
            fraga="Bestäm det positiva värdet på x:",
            ratt_svar=x_val,
            input_typ="text",
            svarstyp="int"
        )
