import random
import numpy as np
import plotly.graph_objects as go
from models import Uppgift

def skapa_normalfordelning_uppgift(niva: int) -> Uppgift:
    """Normalfördelning med full täckning för intervall upp till ±2σ."""
    scenarier = [
        {"namn": "längden på vuxna män", "enhet": "cm", "mu": random.choice([175, 180]), "sigma": random.choice([5, 10])},
        {"namn": "vikten på nyfödda bebisar", "enhet": "g", "mu": random.choice([3500, 3600]), "sigma": random.choice([400, 500])},
        {"namn": "livslängden för en glödlampa", "enhet": "timmar", "mu": random.choice([1000, 1200]), "sigma": random.choice([100, 200])},
        {"namn": "resultatet på ett prov", "enhet": "poäng", "mu": random.choice([50, 60]), "sigma": random.choice([5, 10])}
    ]
    sc = random.choice(scenarier)
    mu, sigma = sc["mu"], sc["sigma"]
    
    if niva == 1:
        fraga_typ = random.choice(['mellersta_95', 'procent_over_2sigma', 'hitta_grans_2sigma', 'mellersta_68'])
        
        if fraga_typ == 'mellersta_95':
            v_low = mu - 2 * sigma
            v_high = mu + 2 * sigma
            ratt_svar = 95
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas ligga mellan {v_low} {sc['enhet']} och {v_high} {sc['enhet']}?"
            sub_text = "Använd 68–95–99,7-regeln (intervallet motsvarar μ ± 2σ)."
            fill_range = (v_low, v_high)

        elif fraga_typ == 'mellersta_68':
            v_low = mu - sigma
            v_high = mu + sigma
            ratt_svar = 68
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas ligga mellan {v_low} {sc['enhet']} och {v_high} {sc['enhet']}?"
            sub_text = "Använd 68–95–99,7-regeln (intervallet motsvarar μ ± 1σ)."
            fill_range = (v_low, v_high)

        elif fraga_typ == 'procent_over_2sigma':
            v_high = mu + 2 * sigma
            ratt_svar = 2.5
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas vara större än {v_high} {sc['enhet']}?"
            sub_text = "Tips: 95 % ligger inom μ ± 2σ. Hur mycket hamnar i den övre svansen?"
            fill_range = (v_high, mu + 4 * sigma)

        else:  # hitta_grans_2sigma
            ratt_svar = mu + 2 * sigma
            fraga = f"Bestäm det värde (i {sc['enhet']}) som motsvarar μ + 2σ när medelvärdet μ = {mu} {sc['enhet']} och standardavvikelsen σ = {sigma} {sc['enhet']}."
            sub_text = "Beräkna μ + 2σ."
            fill_range = None

    else:  # Nivå 2
        fraga_typ = random.choice(['mellan_1_och_2_sigma', 'under_plus_2sigma', 'mellan_minus1_och_plus2', 'antal_personer'])
        
        if fraga_typ == 'mellan_1_och_2_sigma':
            v_low = mu + sigma
            v_high = mu + 2 * sigma
            ratt_svar = 13.5
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas ligga i intervallet från {v_low} {sc['enhet']} till {v_high} {sc['enhet']}?"
            sub_text = "Tips: Mellan μ och μ + 2σ ligger 47,5 %. Mellan μ och μ + 1σ ligger 34 %."
            fill_range = (v_low, v_high)

        elif fraga_typ == 'under_plus_2sigma':
            v_high = mu + 2 * sigma
            ratt_svar = 97.5
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas vara MINDRE än {v_high} {sc['enhet']}?"
            sub_text = "Tips: Räkna med att 50 % ligger under medelvärdet samt 47,5 % mellan μ och μ + 2σ."
            fill_range = (mu - 4 * sigma, v_high)

        elif fraga_typ == 'mellan_minus1_och_plus2':
            v_low = mu - sigma
            v_high = mu + 2 * sigma
            ratt_svar = 81.5
            fraga = f"Hur stor andel (i %) av {sc['namn']} förväntas ligga mellan {v_low} {sc['enhet']} och {v_high} {sc['enhet']}?"
            sub_text = "Tips: Addera andelen mellan μ - 1σ och μ (34 %) samt mellan μ och μ + 2σ (47,5 %)."
            fill_range = (v_low, v_high)

        else:  # antal_personer
            n_tot = random.choice([500, 1000, 2000, 4000])
            v_high = mu + 2 * sigma
            ratt_svar = int(n_tot * 0.025)
            fraga = f"I en undersökning ingår {n_tot} personer där {sc['namn']} är normalfördelad med μ = {mu} {sc['enhet']} och σ = {sigma} {sc['enhet']}.\n\nHur många personer förväntas ha ett värde större än {v_high} {sc['enhet']}?"
            sub_text = "Beräkna först procentandelen (2,5 %) och räkna sedan ut antalet personer."
            fill_range = (v_high, mu + 4 * sigma)

    # Skapa Plotly-graf med skuggat intervall
    x_vals = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 300)
    y_vals = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_vals - mu) / sigma) ** 2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='purple', width=2)))

    if fill_range:
        x_fill = np.linspace(fill_range[0], fill_range[1], 100)
        y_fill = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_fill - mu) / sigma) ** 2)
        fig.add_trace(go.Scatter(
            x=np.concatenate([[fill_range[0]], x_fill, [fill_range[1]]]),
            y=np.concatenate([[0], y_fill, [0]]),
            fill='toself', fillcolor='rgba(139, 0, 139, 0.3)',
            line=dict(color='rgba(255,255,255,0)')
        ))

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[mu - 2*sigma, mu - sigma, mu, mu + sigma, mu + 2*sigma],
            ticktext=[f"{mu - 2*sigma}", f"{mu - sigma}", f"μ={mu}", f"{mu + sigma}", f"{mu + 2*sigma}"]
        ),
        height=300, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor='white', showlegend=False
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
        suffix="%" if ("andel" in fraga) else ("st" if "antal" in fraga.lower() else sc['enhet']),
        undertext=sub_text
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
