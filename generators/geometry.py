import random
import math
import plotly.graph_objects as go
from models import Uppgift

def skapa_geometri_uppgift(niva: int) -> Uppgift:
    """Avståndsformeln och mittpunktsformeln i koordinatsystemet."""
    typ = random.choice(['avstand', 'mittpunkt'])
    
    # Använd pythagoreiska tripplar för exakta heltal i avståndet
    tripplar = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)]
    dx, dy, dist = random.choice(tripplar)
    
    x1 = random.randint(-5, 5)
    y1 = random.randint(-5, 5)
    x2 = x1 + dx
    y2 = y1 + dy
    
    # Plotly-graf för linjesegmentet
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[x1, x2], y=[y1, y2], mode='lines+markers',
                             marker=dict(size=10, color='purple'),
                             line=dict(color='purple', width=2)))
    fig.update_layout(
        xaxis=dict(range=[-10, 20], zeroline=True),
        yaxis=dict(range=[-10, 20], zeroline=True),
        height=350, margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white', showlegend=False
    )
    
    if typ == 'avstand':
        return Uppgift(
            info_text=f"Två punkter i ett koordinatsystem anges till P₁({x1}, {y1}) och P₂({x2}, {y2}).",
            plotly_fig=fig,
            fraga="Beräkna avståndet d mellan punkterna:",
            ratt_svar=dist,
            input_typ="text",
            svarstyp="int",
            undertext="Använd avståndsformeln: d = √((x₂ - x₁)² + (y₂ - y₁)²)"
        )
    else:
        mx = (x1 + x2) / 2.0
        my = (y1 + y2) / 2.0
        ratt_str = f"({mx:g}, {my:g})".replace('.', ',')
        
        return Uppgift(
            info_text=f"Bestäm mittpunkten M för linjesträckan mellan P₁({x1}, {y1}) och P₂({x2}, {y2}).",
            plotly_fig=fig,
            fraga="Ange mittpunktens koordinater x:",
            ratt_svar=mx,
            input_typ="text",
            svarstyp="float",
            undertext="Ange x-koordinaten för mittpunkten."
        )
