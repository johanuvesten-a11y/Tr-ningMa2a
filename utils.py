import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import parse_expr, simplify
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
from models import Uppgift

def formatera_polynom(termer):
    """Formaterar en lista av (koefficient, variabel_str) till fint polynom."""
    res = ""
    for koeff, var in termer:
        if koeff == 0:
            continue
        if var == "":
            term_str = str(abs(koeff))
        else:
            term_str = var if abs(koeff) == 1 else f"{abs(koeff)}{var}"
        
        if res == "":
            res = f"-{term_str}" if koeff < 0 else term_str
        else:
            res += f" - {term_str}" if koeff < 0 else f" + {term_str}"
    return res if res != "" else "0"

def ratta_svar(u: Uppgift, input_svar: Any) -> str:
    """Rättningslogik för alla uppgiftstyper."""
    if u.input_typ == 'flera_text':
        if all(str(s).strip() != "" for s in input_svar):
            try:
                anv_svar = [round(float(str(s).strip().replace(',', '.')), 4) for s in input_svar]
                ratt_svar_list = [round(float(x), 4) for x in u.ratt_svar]
                
                # Om svarstyp är 'ekvationssystem' krävs exakt ordning (x först, y sedan)
                if u.svarstyp == 'ekvationssystem':
                    return 'ratt' if anv_svar == ratt_svar_list else 'fel'
                else:
                    return 'ratt' if sorted(anv_svar) == sorted(ratt_svar_list) else 'fel'
            except ValueError:
                return 'format'
        return 'tom'
        
    elif u.input_typ == 'text':
        svar_str = str(input_svar).strip()
        if not svar_str:
            return 'tom'
            
        try:
            if u.svarstyp == 'int':
                svar_clean = svar_str.replace(" ", "").replace("\xa0", "")
                return 'ratt' if int(svar_clean) == int(u.ratt_svar) else 'fel'
                
            elif u.svarstyp in ['float', 'procent']:
                svar_clean = svar_str.replace(",", ".").replace(" ", "").replace("%", "")
                return 'ratt' if abs(float(svar_clean) - float(u.ratt_svar)) < 0.01 else 'fel'
                
            elif u.svarstyp == 'string_math':
                svar_clean = svar_str.replace(",", ".").replace(" ", "").replace("^", "**")
                transformations = standard_transformations + (implicit_multiplication_application,)
                expr_elev = parse_expr(svar_clean, transformations=transformations)
                ratt_str = str(u.ratt_svar).replace(" ", "").replace("^", "**")
                expr_facit = parse_expr(ratt_str, transformations=transformations)
                return 'ratt' if simplify(expr_elev - expr_facit) == 0 else 'fel'
                
            elif u.svarstyp == 'string':
                return 'ratt' if svar_str.lower() == str(u.ratt_svar).strip().lower() else 'fel'
        except Exception:
            return 'format'
            
    elif u.input_typ in ['radio', 'selectbox']:
        if input_svar and input_svar != 'Välj svar...':
            return 'ratt' if str(input_svar).strip() == str(u.ratt_svar).strip() else 'fel'
        return 'tom'
        
    return 'fel'

def visa_infobox(text: str, style: str):
    colors = {
        'blue': ('#0056b3', '#f8f9fa'),
        'green': ('#28a745', '#e9ecef'),
        'purple': ('#8B008B', '#f3e5f5'),
        'pink': ('#e83e8c', '#fce4ec')
    }
    border_color, bg_color = colors.get(style, ('#333', '#f4f4f4'))
    st.markdown(
        f"<div style='font-size: 20px; font-weight: bold; color: #333; margin-top: 20px; "
        f"background-color: {bg_color}; padding: 20px; border-radius: 10px; border-left: 6px solid {border_color};'>"
        f"{text}</div>", unsafe_allow_html=True
    )
