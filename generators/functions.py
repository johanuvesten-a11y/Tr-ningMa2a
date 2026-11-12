def skapa_andragradsfunktion_uppgift(niva: int) -> Uppgift:
    """Andragradsfunktioner, vertex och symmetrilinje."""
    a = random.choice([-1, 1])
    h = random.randint(-4, 4)  # Symmetrilinje x = h
    k = random.randint(-5, 5)  # Extremvärde y = k
    
    x_vals = np.linspace(h - 5, h + 5, 200)
    y_vals = a * (x_vals - h)**2 + k
    
    # 75 % chans för symmetrilinje, 25 % chans för max/min
    typ = random.choices(['symmetrilinje', 'extrempunkt_typ'], weights=[0.75, 0.25], k=1)[0]
    
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
