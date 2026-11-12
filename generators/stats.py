import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift

def skapa_normalfordelning_uppgift(niva: int) -> Uppgift:
    """Normalfördelning enligt Skolverkets formelblad."""
    scenarier = [
        {"namn": "längden på vuxna män", "enhet": "cm", "mu": random.choice([175, 180]), "sigma": random.choice([5, 10])},
        {"namn": "vikten på nyfödda bebisar", "enhet": "g", "mu": random.choice([3500, 3600]), "sigma": random.choice([400, 500])},
        {"namn": "livslängden för en glödlampa", "enhet": "timmar", "mu": random.choice([1000, 1200]), "sigma": random.choice([100, 200])},
        {"namn": "resultatet på ett prov", "enhet": "poäng", "mu": random.choice([50, 60]), "sigma": random.choice([5, 10])}
    ]
    sc = random.choice(scenarier)
    mu, sigma = sc["mu"], sc["sigma"]
    
    if niva == 1:
        fraga_typ = random.choice(['mellersta_68', 'mellersta_95', 'procent_over_2sigma', 'jamfor_kurvor'])
        
        if fraga_typ == 'jamfor_kurvor':
            aspekt = random.choice(['mu', 'sigma'])
            if aspekt == 'mu':
                mu_a, sig_a = 40, 8
                mu_b, sig_b = 60, 8
                if random.choice([True, False]):
                    mu_a, mu_b = mu_b, mu_a
                ratt = "Kurva A" if mu_a > mu_b else "Kurva B"
                fraga = "Vilken normalfördelning har störst medelvärde (μ)?"
                tips = "Fundera på var i kurvan medelvärdet (μ) avläses."
            else:
                mu_a, sig_a = 50, 5
                mu_b, sig_b = 50, 12
                if random.choice([True, False]):
                    sig_a, sig_b = sig_b, sig_a
                ratt = "Kurva A" if sig_a > sig_b else "Kurva B"
                fraga = "Vilken normalfördelning har störst standardavvikelse (σ)?"
                tips = "Standardavvikelsen (σ) är ett spridningsmått."
                
            x_vals = np.linspace(10, 90, 400)
            y_a = (1 / (sig_a * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_vals - mu_a) / sig_a) ** 2)
            y_b = (1 / (sig_b * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_vals - mu_b) / sig_b) ** 2)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_a, mode='lines', name='Kurva A', line=dict(color='#0056b3', width=3), hoverinfo='skip'))
            fig.add_trace(go.Scatter(x=x_vals, y=y_b, mode='lines', name='Kurva B', line=dict(color='#8B008B', width=3, dash='dash'), hoverinfo='skip'))
            fig.update_layout(
                xaxis=dict(showgrid=True, gridcolor='#e0e0e0', dtick=10),
                yaxis=dict(showticklabels=False),
                height=300, margin=dict(l=20, r=20, t=30, b=20), plot_bgcolor='white', hovermode=False,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            return Uppgift(
                info_text="Jämför de två normalfördelningskurvorna i diagrammet:",
                plotly_fig=fig,
                fraga=fraga,
                ratt_svar=ratt,
                alternativ=["Kurva A", "Kurva B"],
                input_typ="radio",
                svarstyp="string",
                undertext=tips
            )
            
        if fraga_typ == 'mellersta_68':
            v_low, v_high = mu - sigma, mu + sigma
            ratt_svar = 68.2
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas ligga mellan {v_low} {sc['enhet']} och {v_high} {sc['enhet']}?"
            sub_text = "Avgör hur många standardavvikelser intervallet sträcker sig och ta hjälp av formelbladet."
            fill_range = (v_low, v_high)
        elif fraga_typ == 'mellersta_95':
            v_low, v_high = mu - 2 * sigma, mu + 2 * sigma
            ratt_svar = 95.4
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas ligga mellan {v_low} {sc['enhet']} och {v_high} {sc['enhet']}?"
            sub_text = "Avgör hur många standardavvikelser från medelvärdet intervallet omfattar och se formelbladet."
            fill_range = (v_low, v_high)
        else:
            v_high = mu + 2 * sigma
            ratt_svar = 2.3
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas vara större än {v_high} {sc['enhet']}?"
            sub_text = "Ta hjälp av normalfördelningskurvan på formelbladet."
            fill_range = (v_high, mu + 4 * sigma)
            
    else:  # Nivå 2
        fraga_typ = random.choice(['mellan_1_och_2_sigma', 'under_plus_2sigma', 'mellan_minus1_och_plus2', 'antal_personer', 'baklanges_mu_sigma'])
        
        if fraga_typ == 'baklanges_mu_sigma':
            typ_int = random.choice([1, 2])
            v_low = mu - typ_int * sigma
            v_high = mu + typ_int * sigma
            pct_str = "68,2 %" if typ_int == 1 else "95,4 %"
            return Uppgift(
                info_box_text=f"I en normalfördelad undersökning av {sc['namn']} ligger {pct_str} av värdena i intervallet från {v_low} {sc['enhet']} till {v_high} {sc['enhet']}.",
                info_box_style="purple",
                fraga=f"Bestäm medelvärdet (μ) och standardavvikelsen (σ) i {sc['enhet']}:",
                ratt_svar=[float(mu), float(sigma)],
                input_typ="flera_text",
                svarstyp="ordered_float",
                flera_labels=[f"Medelvärde μ ({sc['enhet']}) =", f"Standardavvikelse σ ({sc['enhet']}) ="],
                undertext="Utgå från normalfördelningskurvans symmetri och formelbladets procentsatser."
            )
            
        if fraga_typ == 'mellan_1_och_2_sigma':
            v_low, v_high = mu + sigma, mu + 2 * sigma
            ratt_svar = 13.6
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas ligga i intervallet från {v_low} {sc['enhet']} till {v_high} {sc['enhet']}?"
            sub_text = "Bestäm hur många standardavvikelser från medelvärdet gränserna ligger och läs av på formelbladet."
            fill_range = (v_low, v_high)
        elif fraga_typ == 'under_plus_2sigma':
            v_high = mu + 2 * sigma
            ratt_svar = 97.7
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas vara MINDRE än {v_high} {sc['enhet']}?"
            sub_text = "Utnyttja att kurvan är symmetrisk kring medelvärdet μ och läs av delområdena på formelbladet."
            fill_range = (mu - 4 * sigma, v_high)
        elif fraga_typ == 'mellan_minus1_och_plus2':
            v_low, v_high = mu - sigma, mu + 2 * sigma
            ratt_svar = 81.8
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas ligga mellan {v_low} {sc['enhet']} och {v_high} {sc['enhet']}?"
            sub_text = "Dela upp intervallet vid medelvärdet μ och läs av delområdena på formelbladet."
            fill_range = (v_low, v_high)
        else:
            n_tot = random.choice([1000, 2000, 3000, 5000])
            v_high = mu + 2 * sigma
            ratt_svar = int(round(n_tot * 0.023))
            fraga = f"I en undersökning ingår {n_tot} observationer där {sc['namn']} är normalfördelad med μ = {mu} {sc['enhet']} och σ = {sigma} {sc['enhet']}.\n\nHur många observationer förväntas ha ett värde större än {v_high} {sc['enhet']}?"
            sub_text = "Bestäm först hur många procent som ligger i det markerade området med hjälp av formelbladet."
            fill_range = (v_high, mu + 4 * sigma)

    x_vals = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 300)
    y_vals = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_vals - mu) / sigma) ** 2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='purple', width=2), hoverinfo='skip'))

    if fill_range:
        x_fill = np.linspace(fill_range[0], fill_range[1], 100)
        y_fill = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_fill - mu) / sigma) ** 2)
        fig.add_trace(go.Scatter(
            x=np.concatenate([[fill_range[0]], x_fill, [fill_range[1]]]),
            y=np.concatenate([[0], y_fill, [0]]),
            fill='toself', fillcolor='rgba(139, 0, 139, 0.3)',
            line=dict(color='rgba(255,255,255,0)'), hoverinfo='skip'
        ))

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[mu - 2*sigma, mu - sigma, mu, mu + sigma, mu + 2*sigma],
            ticktext=[f"{mu - 2*sigma}", f"{mu - sigma}", f"μ={mu}", f"{mu + sigma}", f"{mu + 2*sigma}"]
        ),
        yaxis=dict(showticklabels=False),
        height=300, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False, hovermode=False
    )

    info_box = f"Medelvärde (μ) = {mu} {sc['enhet']}<br>Standardavvikelse (σ) = {sigma} {sc['enhet']}"

    return Uppgift(
        info_box_text=info_box,
        info_box_style="purple",
        plotly_fig=fig,
        fraga=fraga,
        ratt_svar=ratt_svar,
        input_typ="text",
        svarstyp="float" if isinstance(ratt_svar, float) else "int",
        suffix="%" if ("andel" in fraga) else "st",
        undertext=sub_text
    )

def skapa_laddiagram_uppgift(niva: int) -> Uppgift:
    """Låddiagram (Boxplots) i liggande format med finare delstreck."""
    if niva == 1:
        q1 = random.randint(15, 25)
        median = q1 + random.randint(4, 9)
        q3 = median + random.randint(4, 9)
        min_v = q1 - random.randint(4, 9)
        max_v = q3 + random.randint(4, 9)
        
        fig = go.Figure()
        fig.add_trace(go.Box(
            q1=[q1], median=[median], q3=[q3],
            lowerfence=[min_v], upperfence=[max_v],
            orientation='h', hoverinfo='skip',
            fillcolor='lightpink', line=dict(color='purple')
        ))
        fig.update_layout(
            xaxis=dict(
                showgrid=True, gridcolor='#d0d0d0', zeroline=False, dtick=5,
                ticks='outside', ticklen=8, tickwidth=1.5,
                minor=dict(dtick=1, ticks='outside', ticklen=4, tickcolor='#666', showgrid=True, gridcolor='#f2f2f2')
            ),
            yaxis=dict(showticklabels=False),
            height=230, margin=dict(l=20, r=20, t=20, b=35),
            plot_bgcolor='white', showlegend=False, hovermode=False
        )
        
        typ = random.choice(['kvartilavstand', 'variationsbredd', 'median', 'q1', 'q3'])
        if typ == 'kvartilavstand':
            return Uppgift(
                info_text="Studera låddiagrammet nedan:",
                plotly_fig=fig,
                fraga="Bestäm kvartilavståndet (IQR):",
                ratt_svar=q3 - q1,
                input_typ="text",
                svarstyp="int",
                undertext="Kvartilavståndet är ett spridningsmått kopplat till lådan."
            )
        elif typ == 'variationsbredd':
            return Uppgift(
                info_text="Studera låddiagrammet nedan:",
                plotly_fig=fig,
                fraga="Bestäm variationsbredden:",
                ratt_svar=max_v - min_v,
                input_typ="text",
                svarstyp="int",
                undertext="Variationsbredden anger skillnaden mellan datamaterialets yttervärden."
            )
        elif typ == 'median':
            return Uppgift(
                info_text="Studera låddiagrammet nedan:",
                plotly_fig=fig,
                fraga="Vilket värde har medianen?",
                ratt_svar=median,
                input_typ="text",
                svarstyp="int"
            )
        elif typ == 'q1':
            return Uppgift(
                info_text="Studera låddiagrammet nedan:",
                plotly_fig=fig,
                fraga="Bestäm den undre kvartilen (Q₁):",
                ratt_svar=q1,
                input_typ="text",
                svarstyp="int"
            )
        else:
            return Uppgift(
                info_text="Studera låddiagrammet nedan:",
                plotly_fig=fig,
                fraga="Bestäm den övre kvartilen (Q₃):",
                ratt_svar=q3,
                input_typ="text",
                svarstyp="int"
            )
    else:
        typ = random.choice(['procent_andel', 'jamfor_tva'])
        if typ == 'procent_andel':
            q1 = random.randint(15, 25)
            median = q1 + random.randint(4, 9)
            q3 = median + random.randint(4, 9)
            min_v = q1 - random.randint(4, 9)
            max_v = q3 + random.randint(4, 9)
            
            fig = go.Figure()
            fig.add_trace(go.Box(
                q1=[q1], median=[median], q3=[q3],
                lowerfence=[min_v], upperfence=[max_v],
                orientation='h', hoverinfo='skip',
                fillcolor='lightpink', line=dict(color='purple')
            ))
            fig.update_layout(
                xaxis=dict(
                    showgrid=True, gridcolor='#d0d0d0', zeroline=False, dtick=5,
                    ticks='outside', ticklen=8, tickwidth=1.5,
                    minor=dict(dtick=1, ticks='outside', ticklen=4, tickcolor='#666', showgrid=True, gridcolor='#f2f2f2')
                ),
                yaxis=dict(showticklabels=False),
                height=230, margin=dict(l=20, r=20, t=20, b=35),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )
            
            fall = random.choice([
                (f"Hur stor andel (i %) av observationerna har ett värde som är minst {q1}?", 75),
                (f"Hur stor andel (i %) av observationerna har ett värde som är högst {q3}?", 75),
                (f"Hur stor andel (i %) av observationerna ligger mellan {q1} och {q3}?", 50),
                (f"Hur stor andel (i %) av observationerna har ett värde som är minst {q3}?", 25)
            ])
            return Uppgift(
                info_text="Studera låddiagrammet nedan:",
                plotly_fig=fig,
                fraga=fall[0],
                ratt_svar=fall[1],
                input_typ="text",
                svarstyp="procent",
                suffix="%",
                undertext="Tänk på hur stor andel av mätvärdena som ryms i varje del av låddiagrammet."
            )
        else:
            med_a, iqr_a, vb_a = 30, 10, 26
            med_b, iqr_b, vb_b = 35, 16, 20
            if random.choice([True, False]):
                med_a, iqr_a, vb_a, med_b, iqr_b, vb_b = med_b, iqr_b, vb_b, med_a, iqr_a, vb_a
                
            q1_a, q3_a = med_a - iqr_a // 2, med_a + iqr_a // 2
            min_a = q1_a - (vb_a - iqr_a) // 2
            max_a = min_a + vb_a
            
            q1_b, q3_b = med_b - iqr_b // 2, med_b + iqr_b // 2
            min_b = q1_b - (vb_b - iqr_b) // 2
            max_b = min_b + vb_b
            
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=["Grupp B"], q1=[q1_b], median=[med_b], q3=[q3_b],
                lowerfence=[min_b], upperfence=[max_b],
                orientation='h', hoverinfo='skip',
                fillcolor='rgba(0, 86, 179, 0.25)', line=dict(color='#0056b3')
            ))
            fig.add_trace(go.Box(
                y=["Grupp A"], q1=[q1_a], median=[med_a], q3=[q3_a],
                lowerfence=[min_a], upperfence=[max_a],
                orientation='h', hoverinfo='skip',
                fillcolor='lightpink', line=dict(color='purple')
            ))
            fig.update_layout(
                xaxis=dict(
                    showgrid=True, gridcolor='#d0d0d0', zeroline=False, dtick=5,
                    ticks='outside', ticklen=8, tickwidth=1.5,
                    minor=dict(dtick=1, ticks='outside', ticklen=4, tickcolor='#666', showgrid=True, gridcolor='#f2f2f2')
                ),
                height=290, margin=dict(l=20, r=20, t=20, b=35),
                plot_bgcolor='white', showlegend=False, hovermode=False
            )
            
            fraga_val = random.choice([
                ("Vilken grupp har störst median?", "Grupp A" if med_a > med_b else "Grupp B"),
                ("Vilken grupp har störst kvartilavstånd (IQR)?", "Grupp A" if iqr_a > iqr_b else "Grupp B"),
                ("Vilken grupp har störst variationsbredd?", "Grupp A" if vb_a > vb_b else "Grupp B")
            ])
            return Uppgift(
                info_text="Jämför de två låddiagrammen:",
                plotly_fig=fig,
                fraga=fraga
