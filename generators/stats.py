import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift

def skapa_normalfordelning_uppgift(niva: int) -> Uppgift:
    """Normalfördelning och 68-95-99.7-regeln."""
    mu = random.choice([160, 170, 180, 1000])
    sigma = random.choice([5, 10, 15, 50])
    
    # Skapa klockkurva
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 300)
    y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='purple', width=2)))
    
    # Skugga ±1 sigma (68%)
    x_fill = np.linspace(mu - sigma, mu + sigma, 100)
    y_fill = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_fill - mu) / sigma)**2)
    fig.add_trace(go.Scatter(x=np.concatenate([[mu - sigma], x_fill, [mu + sigma]]),
                             y=np.concatenate([[0], y_fill, [0]]),
                             fill='toself', fillcolor='rgba(139, 0, 139, 0.3)', line=dict(color='rgba(255,255,255,0)')))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False)
    
    fraga_typ = random.choice(['68_percent', 'above_mu'])
    if fraga_typ == '68_percent':
        info = f"En observation är normalfördelad med medelvärde μ = {mu} och standardavvikelse σ = {sigma}."
        return Uppgift(
            info_box_text=info,
            info_box_style="purple",
            plotly_fig=fig,
            fraga=f"Hur stor andel (i %) av observationerna ligger i intervallet {mu - sigma} till {mu + sigma}?",
            ratt_svar=68,
            input_typ="text",
            svarstyp="int",
            suffix="%",
            undertext="Använd 68–95–99,7-regeln för normalfördelning."
        )
    else:
        info = f"En variabel är normalfördelad med medelvärde μ = {mu}."
        return Uppgift(
            info_box_text=info,
            info_box_style="purple",
            plotly_fig=fig,
            fraga="Hur stor andel (i %) av observationerna förväntas vara större än medelvärdet μ?",
            ratt_svar=50,
            input_typ="text",
            svarstyp="int",
            suffix="%"
        )

def skapa_laddiagram_uppgift(niva: int) -> Uppgift:
    """Låddiagram (Boxplots), kvartiler och median."""
    q1 = random.randint(15, 25)
    median = q1 + random.randint(5, 10)
    q3 = median + random.randint(5, 10)
    min_v = q1 - random.randint(5, 10)
    max_v = q3 + random.randint(5, 10)
    
    fig = go.Figure()
    fig.add_trace(go.Box(q1=[q1], median=[median], q3=[q3], lowerfence=[min_v], upperfence=[max_v], fillcolor='lightpink', line=dict(color='purple')))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False)
    
    typ = random.choice(['kvartilavstand', 'median'])
    if typ == 'kvartilavstand':
        iqr = q3 - q1
        return Uppgift(
            info_text="Studera låddiagrammet nedan:",
            plotly_fig=fig,
            fraga="Bestäm kvartilavståndet (IQR):",
            ratt_svar=iqr,
            input_typ="text",
            svarstyp="int",
            undertext="Kvartilavståndet beräknas som Q₃ - Q₁."
        )
    else:
        return Uppgift(
            info_text="Studera låddiagrammet nedan:",
            plotly_fig=fig,
            fraga="Vilket värde har medianen?",
            ratt_svar=median,
            input_typ="text",
            svarstyp="int"
        )
