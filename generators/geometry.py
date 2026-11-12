import random
import plotly.graph_objects as go
from models import Uppgift

TRIPPLER = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)]

def skapa_geometri_uppgift(niva: int) -> Uppgift:
    """Pythagoras sats, avståndsformeln och mittpunktsformeln."""
    if niva == 1:
        typ = random.choice(['pythagoras_hyp', 'pythagoras_katet', 'avstand', 'mittpunkt'])
        
        if typ in ['pythagoras_hyp', 'pythagoras_katet']:
            a, b, c = random.choice(TRIPPLER)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[0, b, 0, 0], y=[0, 0, a, 0],
                mode='lines', line=dict(color='#0056b3', width=3),
                fill='toself', fillcolor='rgba(0, 86, 179, 0.08)', hoverinfo='skip'
            ))
            s = min(a, b) * 0.14
            fig.add_trace(go.Scatter(
                x=[0, s, s], y=[s, s, 0],
                mode='lines', line=dict(color='black', width=1.5), hoverinfo='skip'
            ))
            
            label_b = f"{b} cm"
            label_a = f"{a} cm" if typ == 'pythagoras_hyp' else "x cm"
            label_c = "x cm" if typ == 'pythagoras_hyp' else f"{c} cm"
            
            fig.add_annotation(x=b/2, y=-a*0.09, text=label_b, showarrow=False, font=dict(size=15, color='black'))
            fig.add_annotation(x=-b*0.11, y=a/2, text=label_a, showarrow=False, font=dict(size=15, color='black'))
            fig.add_annotation(x=b*0.56, y=a*0.56, text=label_c, showarrow=False, font=dict(size=15, color='#d9534f'))
            
            fig.update_layout(
                xaxis=dict(range=[-b*0.25, b*1.15], visible=False),
                yaxis=dict(range=[-a*0.2, a*1.15], visible=False),
                height=300, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )
            
            if typ == 'pythagoras_hyp':
                return Uppgift(
                    info_text="Studera den rätvinkliga triangeln:",
                    plotly_fig=fig,
                    fraga="Beräkna längden av hypotenusan x (i cm):",
                    ratt_svar=c,
                    input_typ="text",
                    svarstyp="int",
                    suffix="cm",
                    undertext="Använd Pythagoras sats: a² + b² = c²."
                )
            else:
                return Uppgift(
                    info_text="Studera den rätvinkliga triangeln:",
                    plotly_fig=fig,
                    fraga="Beräkna längden av kateten x (i cm):",
                    ratt_svar=a,
                    input_typ="text",
                    svarstyp="int",
                    suffix="cm",
                    undertext="Använd Pythagoras sats: x² + b² = c²."
                )
                
        elif typ == 'avstand':
            dx, dy, dist = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
            if random.choice([True, False]):
                dx, dy = dy, dx
            x1 = random.randint(-4, 4)
            y1 = random.randint(-4, 4)
            x2 = x1 + dx * random.choice([-1, 1])
            y2 = y1 + dy * random.choice([-1, 1])
            
            return Uppgift(
                info_box_text=f"Två punkter har koordinaterna A({x1}, {y1}) och B({x2}, {y2}).",
                info_box_style="green",
                fraga="Beräkna avståndet mellan punkterna A och B (i l.e.):",
                ratt_svar=dist,
                input_typ="text",
                svarstyp="int",
                suffix="l.e.",
                undertext="Använd avståndsformeln: d = √((x₂ - x₁)² + (y₂ - y₁)²)."
            )
        else:
            x1 = random.randint(-6, 6)
            y1 = random.randint(-6, 6)
            x2 = x1 + 2 * random.randint(-5, 5)
            y2 = y1 + 2 * random.randint(-5, 5)
            xm = (x1 + x2) // 2
            ym = (y1 + y2) // 2
            
            return Uppgift(
                info_box_text=f"Sträckan AB har ändpunkterna A({x1}, {y1}) och B({x2}, {y2}).",
                info_box_style="green",
                fraga="Bestäm mittpunktens koordinater (x och y):",
                ratt_svar=[float(xm), float(ym)],
                input_typ="flera_text",
                svarstyp="punkt",
                flera_labels=["x =", "y ="],
                undertext="Använd mittpunktsformeln: xₘ = (x₁ + x₂)/2 och yₘ = (y₁ + y₂)/2."
            )
    else:
        typ = random.choice(['pythagoras_likbent', 'omvand_mittpunkt', 'omvand_avstand'])
        if typ == 'pythagoras_likbent':
            halv_bas, hojd, ben = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
            bas = 2 * halv_bas
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[0, bas, halv_bas, 0], y=[0, 0, hojd, 0],
                mode='lines', line=dict(color='#0056b3', width=3),
                fill='toself', fillcolor='rgba(0, 86, 179, 0.08)', hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[halv_bas, halv_bas], y=[0, hojd],
                mode='lines', line=dict(color='#d9534f', width=2, dash='dash'), hoverinfo='skip'
            ))
            fig.add_annotation(x=bas/2, y=-hojd*0.1, text=f"Bas = {bas} cm", showarrow=False, font=dict(size=14))
            fig.add_annotation(x=halv_bas*0.35, y=hojd*0.55, text=f"{ben} cm", showarrow=False, font=dict(size=14))
            fig.add_annotation(x=bas - halv_bas*0.35, y=hojd*0.55, text=f"{ben} cm", showarrow=False, font=dict(size=14))
            fig.add_annotation(x=halv_bas + bas*0.05, y=hojd*0.45, text="h", showarrow=False, font=dict(size=15, color='#d9534f'))
            
            fig.update_layout(
                xaxis=dict(range=[-bas*0.15, bas*1.15], visible=False),
                yaxis=dict(range=[-hojd*0.2, hojd*1.15], visible=False),
                height=300, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )
            return Uppgift(
                info_text=f"En likbent triangel har basen {bas} cm och de två lika sidorna är {ben} cm vardera.",
                plotly_fig=fig,
                fraga="Beräkna triangelns höjd h (i cm):",
                ratt_svar=hojd,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext="Höjden delar basen i två lika stora delar och bildar två rätvinkliga trianglar."
            )
        elif typ == 'omvand_mittpunkt':
            x1 = random.randint(-5, 5)
            y1 = random.randint(-5, 5)
            xm = random.randint(-4, 6)
            ym = random.randint(-4, 6)
            x2 = 2 * xm - x1
            y2 = 2 * ym - y1
            return Uppgift(
                info_box_text=f"Sträckan AB har ena ändpunkten i A({x1}, {y1}) och mittpunkten i M({xm}, {ym}).",
                info_box_style="green",
                fraga="Bestäm koordinaterna för den andra ändpunkten B (x och y):",
                ratt_svar=[float(x2), float(y2)],
                input_typ="flera_text",
                svarstyp="punkt",
                flera_labels=["x =", "y ="],
                undertext="Ställ upp ekvationer med mittpunktsformeln: (x₁ + x₂)/2 = xₘ."
            )
        else:
            dx, dy, dist = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
            x1 = random.randint(-3, 4)
            x2 = x1 + dx * random.choice([-1, 1])
            y1 = random.randint(1, dy - 1)
            y_ratt = y1 + dy
            return Uppgift(
                info_box_text=f"Avståndet mellan punkterna A({x1}, {y1}) och B({x2}, y) är {dist} l.e.",
                info_box_style="green",
                fraga="Bestäm det positiva värdet på koordinaten y:",
                ratt_svar=y_ratt,
                input_typ="text",
                svarstyp="int",
                undertext="Sätt in punkterna i avståndsformeln och lös ekvationen."
            )
