import random
import math
import plotly.graph_objects as go
from models import Uppgift

def skapa_geometri_uppgift(niva: int) -> Uppgift:
    """Pythagoras sats, avståndsformeln och mittpunktsformeln."""
    if niva == 1:
        typ = random.choice(['pythagoras_hyp', 'pythagoras_katet', 'avstand', 'mittpunkt'])
        
        if typ in ['pythagoras_hyp', 'pythagoras_katet']:
            triplar = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)]
            a, b, c = random.choice(triplar)
            if random.choice([True, False]):
                a, b = b, a
                
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[0, a, 0, 0], y=[0, 0, b, 0], mode='lines', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
            sq = min(a, b) * 0.14
            fig.add_trace(go.Scatter(x=[0, sq, sq, 0], y=[sq, sq, 0, 0], mode='lines', line=dict(color='black', width=1.5), hoverinfo='skip'))
            
            if typ == 'pythagoras_hyp':
                lbl_a, lbl_b, lbl_c = f"{a} cm", f"{b} cm", "x"
                ratt = c
                fraga = "Beräkna hypotenusans längd x (i cm):"
                tips = "Använd Pythagoras sats."
            else:
                lbl_a, lbl_b, lbl_c = "x", f"{b} cm", f"{c} cm"
                ratt = a
                fraga = "Beräkna den okända katetens längd x (i cm):"
                tips = "Använd Pythagoras sats (tänk på vilken sida som är hypotenusa)."
                
            fig.add_annotation(x=a/2, y=-b*0.09, text=lbl_a, showarrow=False, font=dict(size=15, color='black'))
            fig.add_annotation(x=-a*0.11, y=b/2, text=lbl_b, showarrow=False, font=dict(size=15, color='black'))
            fig.add_annotation(x=a/2 + a*0.09, y=b/2 + b*0.09, text=lbl_c, showarrow=False, font=dict(size=15, color='#d9534f'))
            
            fig.update_layout(
                xaxis=dict(visible=False, range=[-a*0.25, a*1.25]),
                yaxis=dict(visible=False, range=[-b*0.25, b*1.25], scaleanchor="x", scaleratio=1),
                height=290, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', showlegend=False, hovermode=False
            )
            return Uppgift(
                info_text="Studera den rätvinkliga triangeln:",
                plotly_fig=fig,
                fraga=fraga,
                ratt_svar=ratt,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext=tips
            )
            
        elif typ == 'avstand':
            dx, dy, d = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
            if random.choice([True, False]):
                dx, dy = dy, dx
            dx *= random.choice([-1, 1])
            dy *= random.choice([-1, 1])
            x1, y1 = random.randint(-4, 4), random.randint(-4, 4)
            x2, y2 = x1 + dx, y1 + dy
            
            return Uppgift(
                info_box_text=f"Beräkna avståndet mellan punkterna A = ({x1}, {y1}) och B = ({x2}, {y2}) i ett koordinatsystem.",
                info_box_style="blue",
                fraga="Ange avståndet (i längdenheter):",
                ratt_svar=d,
                input_typ="text",
                svarstyp="int",
                suffix="l.e.",
                undertext="Använd avståndsformeln (se formelbladet vid behov)."
            )
        else:
            xm, ym = random.randint(-4, 4), random.randint(-4, 4)
            dx, dy = random.randint(1, 5), random.randint(1, 5)
            x1, y1 = xm - dx, ym - dy
            x2, y2 = xm + dx, ym + dy
            return Uppgift(
                info_box_text=f"En sträcka har ändpunkterna A = ({x1}, {y1}) och B = ({x2}, {y2}).",
                info_box_style="blue",
                fraga="Bestäm sträckans mittpunkt (x och y):",
                ratt_svar=[float(xm), float(ym)],
                input_typ="flera_text",
                svarstyp="punkt",
                flera_labels=["x =", "y ="],
                undertext="Använd mittpunktsformeln (se formelbladet vid behov)."
            )
    else:
        typ = random.choice(['pythagoras_likbent', 'omvand_mittpunkt', 'omvand_avstand'])
        if typ == 'pythagoras_likbent':
            halv_bas, hojd, sida = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
            bas = 2 * halv_bas
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[0, bas, halv_bas, 0], y=[0, 0, hojd, 0], mode='lines', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
            fig.add_trace(go.Scatter(x=[halv_bas, halv_bas], y=[0, hojd], mode='lines', line=dict(color='#666', width=1.5, dash='dash'), hoverinfo='skip'))
            
            fig.add_annotation(x=bas/2, y=-hojd*0.09, text=f"{bas} cm", showarrow=False, font=dict(size=14, color='black'))
            fig.add_annotation(x=halv_bas*0.35, y=hojd*0.55, text=f"{sida} cm", showarrow=False, font=dict(size=14, color='black'))
            fig.add_annotation(x=bas - halv_bas*0.35, y=hojd*0.55, text=f"{sida} cm", showarrow=False, font=dict(size=14, color='black'))
            fig.add_annotation(x=halv_bas + bas*0.05, y=hojd*0.45, text="h", showarrow=False, font=dict(size=14, color='#d9534f'))
            
            fig.update_layout(
                xaxis=dict(visible=False, range=[-bas*0.15, bas*1.15]),
                yaxis=dict(visible=False, range=[-hojd*0.2, hojd*1.15], scaleanchor="x", scaleratio=1),
                height=290, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', showlegend=False, hovermode=False
            )
            return Uppgift(
                info_text="Triangeln i figuren är likbent:",
                plotly_fig=fig,
                fraga="Beräkna triangelns höjd h (i cm):",
                ratt_svar=hojd,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext="Utnyttja att triangeln är likbent och dela upp den i rätvinkliga trianglar."
            )
        elif typ == 'omvand_mittpunkt':
            xm, ym = random.randint(-3, 4), random.randint(-3, 4)
            dx, dy = random.randint(2, 6), random.randint(2, 6)
            x1, y1 = xm - dx, ym - dy
            x2, y2 = xm + dx, ym + dy
            return Uppgift(
                info_box_text=f"En sträcka mellan punkterna A och B har mittpunkten M = ({xm}, {ym}). Den ena ändpunkten är A = ({x1}, {y1}).",
                info_box_style="blue",
                fraga="Bestäm koordinaterna för den andra ändpunkten B:",
                ratt_svar=[float(x2), float(y2)],
                input_typ="flera_text",
                svarstyp="punkt",
                flera_labels=["x =", "y ="],
                undertext="Utgå från mittpunktsformeln och ställ upp en ekvation för varje koordinat."
            )
        else:
            dx, dy, d = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13)])
            x1, y1 = random.randint(-3, 3), random.randint(-3, 3)
            x2 = x1 + dx
            y2 = y1 + dy
            return Uppgift(
                info_box_text=f"Avståndet mellan punkterna A = ({x1}, {y1}) och B = ({x2}, y) är {d} längdenheter, där y > {y1}.",
                info_box_style="blue",
                fraga="Bestäm y-koordinaten för punkten B:",
                ratt_svar=y2,
                input_typ="text",
                svarstyp="int",
                undertext="Sätt in punkterna i avståndsformeln och lös ekvationen."
            )
