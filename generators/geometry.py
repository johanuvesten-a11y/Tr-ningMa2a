import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift

TRIPPLER = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)]

# Kedjade tripplar: (a1, b1, c1, b2, c2) där a1² + b1² = c1² och c1² + b2² = c2²
KEDJADE_TRIPPLER = [
    (3, 4, 5, 12, 13),
    (4, 3, 5, 12, 13),
    (6, 8, 10, 24, 26),
    (8, 6, 10, 24, 26),
    (9, 12, 15, 8, 17),
    (12, 9, 15, 8, 17),
    (9, 12, 15, 20, 25),
    (12, 9, 15, 20, 25),
]


def _rita_ratvinklig_triangel(a_vis: float, b_vis: float, lbl_botten: str, lbl_hojd: str, lbl_hyp: str) -> go.Figure:
    """Hjälpfunktion som ritar en rätvinklig triangel med valfria algebraiska eller numeriska etiketter."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0, b_vis, 0, 0], y=[0, 0, a_vis, 0],
        mode='lines', line=dict(color='#0056b3', width=3),
        fill='toself', fillcolor='rgba(0, 86, 179, 0.08)', hoverinfo='skip'
    ))
    s = min(a_vis, b_vis) * 0.14
    fig.add_trace(go.Scatter(
        x=[0, s, s], y=[s, s, 0],
        mode='lines', line=dict(color='black', width=1.5), hoverinfo='skip'
    ))

    fig.add_annotation(x=b_vis / 2, y=-a_vis * 0.11, text=lbl_botten, showarrow=False, font=dict(size=14, color='black'))
    fig.add_annotation(x=-b_vis * 0.16, y=a_vis / 2, text=lbl_hojd, showarrow=False, font=dict(size=14, color='black'))
    fig.add_annotation(x=b_vis * 0.58, y=a_vis * 0.56, text=lbl_hyp, showarrow=False, font=dict(size=14, color='#d9534f'))

    fig.update_layout(
        xaxis=dict(range=[-b_vis * 0.35, b_vis * 1.2], visible=False),
        yaxis=dict(range=[-a_vis * 0.25, a_vis * 1.15], visible=False),
        height=300, margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor='white', showlegend=False, hovermode=False
    )
    return fig


def skapa_geometri_uppgift(niva: int) -> Uppgift:
    """Pythagoras sats (algebraiska och flerstegsuppgifter), avståndsformeln och mittpunktsformeln."""
    if niva == 1:
        typ = random.choice([
            'pythagoras_alg_andragrad',
            'pythagoras_alg_linjar',
            'pythagoras_rektangel_area',
            'avstand',
            'mittpunkt'
        ])

        if typ == 'pythagoras_alg_andragrad':
            # Kateterna är x och (x + d), hypotenusan är c -> andragradsekvation x² + (x + d)² = c²
            a, b, c = random.choice(TRIPPLER)
            d = b - a
            if random.choice([True, False]):
                fig = _rita_ratvinklig_triangel(a, b, f"(x + {d}) cm", "x cm", f"{c} cm")
            else:
                fig = _rita_ratvinklig_triangel(b, a, "x cm", f"(x + {d}) cm", f"{c} cm")

            return Uppgift(
                info_text="Studera den rätvinkliga triangeln där sidlängderna anges i cm:",
                plotly_fig=fig,
                fraga="Ställ upp en ekvation med Pythagoras sats och bestäm x (i cm):",
                ratt_svar=a,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext="Använd Pythagoras sats och första kvadreringsregeln. Tänk på att x > 0."
            )

        elif typ == 'pythagoras_alg_linjar':
            # Ena kateten är a, andra kateten är x, hypotenusan är (x + d) -> x²-termerna tar ut varandra
            a, b, c = random.choice(TRIPPLER)
            if random.choice([True, False]):
                a, b = b, a
            d = c - b
            if random.choice([True, False]):
                fig = _rita_ratvinklig_triangel(a, b, "x cm", f"{a} cm", f"(x + {d}) cm")
            else:
                fig = _rita_ratvinklig_triangel(b, a, f"{a} cm", "x cm", f"(x + {d}) cm")

            return Uppgift(
                info_text="Studera den rätvinkliga triangeln där sidlängderna anges i cm:",
                plotly_fig=fig,
                fraga="Bestäm längden x (i cm):",
                ratt_svar=b,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext="Använd Pythagoras sats och utveckla parentesen med första kvadreringsregeln."
            )

        elif typ == 'pythagoras_rektangel_area':
            # Rektangel med bredd x, längd (x + d) och diagonal c -> beräkna arean
            a, b, c = random.choice(TRIPPLER)
            d = b - a
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[0, b, b, 0, 0], y=[0, 0, a, a, 0],
                mode='lines', line=dict(color='#0056b3', width=3),
                fill='toself', fillcolor='rgba(0, 86, 179, 0.08)', hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[0, b], y=[0, a],
                mode='lines', line=dict(color='#d9534f', width=2, dash='dash'), hoverinfo='skip'
            ))
            s = min(a, b) * 0.14
            fig.add_trace(go.Scatter(
                x=[0, s, s], y=[s, s, 0],
                mode='lines', line=dict(color='black', width=1.5), hoverinfo='skip'
            ))

            fig.add_annotation(x=b / 2, y=-a * 0.12, text=f"(x + {d}) cm", showarrow=False, font=dict(size=14, color='black'))
            fig.add_annotation(x=-b * 0.13, y=a / 2, text="x cm", showarrow=False, font=dict(size=14, color='black'))
            fig.add_annotation(x=b * 0.52, y=a * 0.58, text=f"{c} cm", showarrow=False, font=dict(size=14, color='#d9534f'))

            fig.update_layout(
                xaxis=dict(range=[-b * 0.28, b * 1.15], visible=False),
                yaxis=dict(range=[-a * 0.25, a * 1.18], visible=False),
                height=300, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )

            return Uppgift(
                info_text=f"En rektangel har bredden x cm, längden (x + {d}) cm och diagonalen {c} cm.",
                plotly_fig=fig,
                fraga="Beräkna rektangelns area (i cm²):",
                ratt_svar=a * b,
                input_typ="text",
                svarstyp="int",
                suffix="cm²",
                undertext="Bestäm först x med hjälp av Pythagoras sats och räkna sedan ut arean."
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
        typ = random.choice([
            'pythagoras_likbent_area',
            'pythagoras_korda',
            'pythagoras_sammansatt',
            'pythagoras_romb',
            'omvand_mittpunkt',
            'omvand_avstand'
        ])

        if typ == 'pythagoras_likbent_area':
            # Likbent triangel med given bas och omkrets -> beräkna area
            halv_bas, hojd, ben = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
            bas = 2 * halv_bas
            omkrets = bas + 2 * ben

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
            fig.add_annotation(x=bas / 2, y=-hojd * 0.11, text=f"Bas = {bas} cm", showarrow=False, font=dict(size=14))
            fig.add_annotation(x=halv_bas + bas * 0.05, y=hojd * 0.45, text="h", showarrow=False, font=dict(size=15, color='#d9534f'))

            fig.update_layout(
                xaxis=dict(range=[-bas * 0.15, bas * 1.15], visible=False),
                yaxis=dict(range=[-hojd * 0.22, hojd * 1.15], visible=False),
                height=300, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )
            return Uppgift(
                info_text=f"En likbent triangel har basen {bas} cm och omkretsen {omkrets} cm.",
                plotly_fig=fig,
                fraga="Beräkna triangelns area (i cm²):",
                ratt_svar=halv_bas * hojd,
                input_typ="text",
                svarstyp="int",
                suffix="cm²",
                undertext="Bestäm först de två lika sidorna med hjälp av omkretsen, räkna sedan ut höjden h med Pythagoras sats."
            )

        elif typ == 'pythagoras_korda':
            # Korda i cirkel: radie r och vinkelrätt avstånd d från medelpunkten -> beräkna kordans längd
            d_avst, halv_korda, r = random.choice([(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13)])
            theta = np.linspace(0, 2 * np.pi, 200)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=r * np.cos(theta), y=r * np.sin(theta),
                mode='lines', line=dict(color='#0056b3', width=2.5), hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[-halv_korda, halv_korda], y=[-d_avst, -d_avst],
                mode='lines', line=dict(color='#28a745', width=3), hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[0, 0, halv_korda, 0], y=[0, -d_avst, -d_avst, 0],
                mode='lines', line=dict(color='#d9534f', width=2, dash='dash'), hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[0], y=[0], mode='markers', marker=dict(size=7, color='black'), hoverinfo='skip'
            ))
            s = min(d_avst, halv_korda) * 0.22
            fig.add_trace(go.Scatter(
                x=[0, s, s], y=[-d_avst + s, -d_avst + s, -d_avst],
                mode='lines', line=dict(color='black', width=1.2), hoverinfo='skip'
            ))

            fig.add_annotation(x=-r * 0.08, y=r * 0.08, text="M", showarrow=False, font=dict(size=14, color='black'))
            fig.add_annotation(x=-r * 0.18, y=-d_avst * 0.5, text=f"{d_avst} cm", showarrow=False, font=dict(size=13, color='#d9534f'))
            fig.add_annotation(x=halv_korda * 0.65, y=-d_avst * 0.35, text=f"{r} cm", showarrow=False, font=dict(size=13, color='#d9534f'))
            fig.add_annotation(x=0, y=-d_avst - r * 0.12, text="Korda", showarrow=False, font=dict(size=14, color='#28a745'))

            fig.update_layout(
                xaxis=dict(range=[-r * 1.25, r * 1.25], visible=False),
                yaxis=dict(range=[-r * 1.25, r * 1.25], scaleanchor="x", scaleratio=1, visible=False),
                height=310, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )

            return Uppgift(
                info_text=f"En cirkel med medelpunkt M har radien {r} cm. En korda ligger på det vinkelräta avståndet {d_avst} cm från M.",
                plotly_fig=fig,
                fraga="Beräkna hela kordans längd (i cm):",
                ratt_svar=2 * halv_korda,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext="Radien, avståndet från medelpunkten och halva kordan bildar en rätvinklig triangel."
            )

        elif typ == 'pythagoras_sammansatt':
            # Två sammansatta rätvinkliga trianglar med gemensam sida c1
            a1, b1, c1, b2, c2 = random.choice(KEDJADE_TRIPPLER)
            p1 = np.array([float(a1), 0.0])
            p2 = np.array([0.0, float(b1)])
            n_hat = np.array([b1 / c1, a1 / c1])
            p3 = p2 + b2 * n_hat

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[0, p1[0], p2[0], 0], y=[0, p1[1], p2[1], 0],
                mode='lines', line=dict(color='#0056b3', width=3),
                fill='toself', fillcolor='rgba(0, 86, 179, 0.08)', hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[p1[0], p2[0], p3[0], p1[0]], y=[p1[1], p2[1], p3[1], p1[1]],
                mode='lines', line=dict(color='#28a745', width=3),
                fill='toself', fillcolor='rgba(40, 167, 69, 0.08)', hoverinfo='skip'
            ))

            # Räta vinklar i (0,0) och p2
            s1 = min(a1, b1) * 0.16
            fig.add_trace(go.Scatter(
                x=[0, s1, s1], y=[s1, s1, 0],
                mode='lines', line=dict(color='black', width=1.4), hoverinfo='skip'
            ))
            u1 = (p1 - p2) / c1
            s2 = min(c1, b2) * 0.15
            rv1 = p2 + s2 * u1
            rv2 = p2 + s2 * u1 + s2 * n_hat
            rv3 = p2 + s2 * n_hat
            fig.add_trace(go.Scatter(
                x=[rv1[0], rv2[0], rv3[0]], y=[rv1[1], rv2[1], rv3[1]],
                mode='lines', line=dict(color='black', width=1.4), hoverinfo='skip'
            ))

            # Etiketter placerade längs utåtriktade normaler
            max_x = max(a1, p3[0])
            max_y = max(b1, p3[1])
            skala = max(max_x, max_y)

            fig.add_annotation(x=a1 / 2, y=-skala * 0.07, text=f"{a1} cm", showarrow=False, font=dict(size=13))
            fig.add_annotation(x=-skala * 0.11, y=b1 / 2, text=f"{b1} cm", showarrow=False, font=dict(size=13))

            u_out_23 = np.array([-a1 / c1, b1 / c1])
            pos_b2 = (p2 + p3) / 2 + 0.10 * skala * u_out_23
            fig.add_annotation(x=pos_b2[0], y=pos_b2[1], text=f"{b2} cm", showarrow=False, font=dict(size=13))

            v_13 = p3 - p1
            u_out_13 = np.array([v_13[1], -v_13[0]]) / c2
            pos_x = (p1 + p3) / 2 + 0.10 * skala * u_out_13
            fig.add_annotation(x=pos_x[0], y=pos_x[1], text="x cm", showarrow=False, font=dict(size=14, color='#d9534f'))

            fig.update_layout(
                xaxis=dict(range=[-max_x * 0.25, max_x * 1.25], visible=False),
                yaxis=dict(range=[-max_y * 0.18, max_y * 1.22], scaleanchor="x", scaleratio=1, visible=False),
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )

            return Uppgift(
                info_text="Figuren visar två sammansatta rätvinkliga trianglar med sidlängder i cm:",
                plotly_fig=fig,
                fraga="Beräkna sträckan x (i cm):",
                ratt_svar=c2,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext="Använd Pythagoras sats i två steg via den gemensamma sidan."
            )

        elif typ == 'pythagoras_romb':
            # Romb med givna diagonaler d1 och d2 -> beräkna rombens omkrets
            a, b, c = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17)])
            d1, d2 = 2 * a, 2 * b

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[-a, 0, a, 0, -a], y=[0, -b, 0, b, 0],
                mode='lines', line=dict(color='#0056b3', width=3),
                fill='toself', fillcolor='rgba(0, 86, 179, 0.08)', hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[-a, a], y=[0, 0],
                mode='lines', line=dict(color='#d9534f', width=1.8, dash='dash'), hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[0, 0], y=[-b, b],
                mode='lines', line=dict(color='#d9534f', width=1.8, dash='dash'), hoverinfo='skip'
            ))
            s = min(a, b) * 0.18
            fig.add_trace(go.Scatter(
                x=[0, s, s], y=[s, s, 0],
                mode='lines', line=dict(color='black', width=1.3), hoverinfo='skip'
            ))

            fig.add_annotation(x=a * 0.45, y=-b * 0.12, text=f"d₁ = {d1} cm", showarrow=False, font=dict(size=13, color='#d9534f'))
            fig.add_annotation(x=-a * 0.25, y=b * 0.45, text=f"d₂ = {d2} cm", showarrow=False, font=dict(size=13, color='#d9534f'))

            fig.update_layout(
                xaxis=dict(range=[-a * 1.25, a * 1.25], visible=False),
                yaxis=dict(range=[-b * 1.2, b * 1.2], scaleanchor="x", scaleratio=1, visible=False),
                height=300, margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )

            return Uppgift(
                info_text=f"En romb har diagonalerna d₁ = {d1} cm och d₂ = {d2} cm.",
                plotly_fig=fig,
                fraga="Beräkna rombens omkrets (i cm):",
                ratt_svar=4 * c,
                input_typ="text",
                svarstyp="int",
                suffix="cm",
                undertext="I en romb är alla fyra sidor lika långa och diagonalerna skär varandra vinkelrätt på mitten."
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
