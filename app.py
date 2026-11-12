import streamlit as st
import random
from models import Uppgift
from utils import ratta_svar, visa_infobox
from generators.algebra import (skapa_pq_uppgift, skapa_kvadrering_konjugat_uppgift,
                                skapa_ekvationssystem_uppgift, skapa_rationella_uttryck_uppgift)
from generators.functions import skapa_andragradsfunktion_uppgift, skapa_exp_potens_uppgift
from generators.geometry import skapa_geometri_uppgift
from generators.stats import skapa_normalfordelning_uppgift, skapa_laddiagram_uppgift

st.set_page_config(layout="wide", page_title="Matematik 2a Träning")

# CSS Formatering
st.markdown("""
<style>
input[type="text"] {
    font-size: 16px !important;
    font-weight: bold !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

KATEGORIER = {
    "Andragradsekvationer & PQ": skapa_pq_uppgift,
    "Kvadrerings- & Konjugatregler": skapa_kvadrering_konjugat_uppgift,
    "Rationella Uttryck": skapa_rationella_uttryck_uppgift,
    "Linjära Ekvationssystem": skapa_ekvationssystem_uppgift,
    "Andragradsfunktioner & Vertex": skapa_andragradsfunktion_uppgift,
    "Exponential- & Potensfunktioner": skapa_exp_potens_uppgift,
    "Avstånds- & Mittpunktsformeln": skapa_geometri_uppgift,
    "Normalfördelning": skapa_normalfordelning_uppgift,
    "Låddiagram & Kvartiler": skapa_laddiagram_uppgift
}

def generera_ny_uppgift():
    st.session_state.rattat = False
    st.session_state.svar_status = None
    st.session_state.uppgift_id = st.session_state.get('uppgift_id', 0) + 1
    
    kat = st.session_state.aktuell_kategori
    niva = st.session_state.niva
    
    if kat == "Blandat (Slumpas)":
        val_kat = random.choice(list(KATEGORIER.keys()))
        u = KATEGORIER[val_kat](niva)
        u.visnings_kategori = val_kat
    else:
        u = KATEGORIER[kat](niva)
        u.visnings_kategori = kat
        
    st.session_state.aktiv_uppgift = u

def hantera_svar():
    st.session_state.rattat = True
    u = st.session_state.aktiv_uppgift
    uid = st.session_state.uppgift_id
    
    if u.input_typ == 'flera_text':
        input_svar = [st.session_state.get(f"input_{uid}_{i}", "") for i in range(len(u.ratt_svar))]
    else:
        input_svar = st.session_state.get(f"input_single_{uid}")
        
    st.session_state.svar_status = ratta_svar(u, input_svar)

# Menystyrning
st.sidebar.title("Matematik 2a")
vald_kategori = st.sidebar.radio("Välj område:", list(KATEGORIER.keys()) + ["Blandat (Slumpas)"])

if 'aktuell_kategori' not in st.session_state or st.session_state.aktuell_kategori != vald_kategori:
    st.session_state.aktuell_kategori = vald_kategori
    st.session_state.niva = 1
    generera_ny_uppgift()
    st.rerun()

st.sidebar.divider()
ny_niva = st.sidebar.radio("Svårighetsgrad:", [1, 2], horizontal=True, index=st.session_state.get('niva', 1) - 1)
if ny_niva != st.session_state.niva:
    st.session_state.niva = ny_niva
    generera_ny_uppgift()
    st.rerun()

# Huvudgränssnitt
u = st.session_state.aktiv_uppgift
st.title(f"Träning: {st.session_state.aktuell_kategori}")

col_v, col_h = st.columns([1.2, 1], gap="large")

with col_v:
    if u.plotly_fig is not None:
        st.plotly_chart(u.plotly_fig, use_container_width=True, config={'displayModeBar': False})
    if u.info_text:
        st.markdown(f"<div style='font-size: 18px; color: #555;'>{u.info_text}</div>", unsafe_allow_html=True)
    if u.latex_text:
        st.latex(u.latex_text)
    if u.info_box_text and u.info_box_style:
        visa_infobox(u.info_box_text, u.info_box_style)

with col_h:
    st.subheader("Uppgift")
    if u.undertext:
        st.markdown(f"<p style='font-size: 14px; color: #666;'><i>{u.undertext}</i></p>", unsafe_allow_html=True)
        
    st.markdown(f"<div style='font-size: 22px; font-weight: bold; color: #0056b3; margin-bottom: 20px;'>{u.fraga}</div>", unsafe_allow_html=True)
    
    uid = st.session_state.uppgift_id
    rattat = st.session_state.get('rattat', False)
    status = st.session_state.get('svar_status', None)
    
    if rattat and status == 'ratt':
        st.success("✅ Helt rätt! Snyggt jobbat.")
        if st.button("Nästa uppgift", type="primary", use_container_width=True, key=f"next_{uid}"):
            generera_ny_uppgift()
            st.rerun()
    else:
        with st.form(key=f"form_{uid}"):
            if u.input_typ == 'flera_text':
                labels = ["x =", "y ="] if u.svarstyp == 'ekvationssystem' else [f"Svar {i+1}:" for i in range(len(u.ratt_svar))]
                for i in range(len(u.ratt_svar)):
                    st.text_input(labels[i], key=f"input_{uid}_{i}")
            elif u.input_typ == 'text':
                st.text_input("Ditt svar:", key=f"input_single_{uid}")
            elif u.input_typ == 'radio':
                st.radio("Alternativ:", u.alternativ, index=None, key=f"input_single_{uid}")
            
            st.form_submit_button("Rätta svar", use_container_width=True, on_click=hantera_svar)
            
        if rattat and status != 'ratt':
            if status == 'fel':
                if u.svarstyp == 'ekvationssystem':
                    ratt_txt = f"x = {int(u.ratt_svar[0])}, y = {int(u.ratt_svar[1])}"
                elif u.svarstyp == 'array_float':
                    ratt_txt = ' och '.join([f"{a:g}".replace('.', ',') for a in u.ratt_svar])
                else:
                    ratt_txt = str(u.ratt_svar)
                st.error(f"❌ Tyvärr fel. Rätt svar var: {ratt_txt}")
            elif status == 'format':
                st.warning("⚠️ Felaktigt format på svaret.")
            elif status == 'tom':
                st.warning("⚠️ Fyll i ett svar innan du rättar.")

            elif status == 'format_saknar_x':
                st.warning("⚠️ Symmetrilinjen är en linje och måste skrivas som en ekvation, t.ex. x = 2.")
                
            if st.button("Hoppa över / Nästa uppgift", use_container_width=True, key=f"skip_{uid}"):
                generera_ny_uppgift()
                st.rerun()
