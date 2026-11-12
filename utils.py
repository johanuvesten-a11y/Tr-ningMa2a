import re
import streamlit as st
from sympy import parse_expr, simplify, symbols, fraction, together, Poly
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

def _rensa_enhet(s: str) -> str:
    s = s.replace(" ", "").replace("\xa0", "")
    s = re.sub(r'(kr|st|cm|mm|dm|m|g|kg|l\.e\.|a\.e\.|timmar|tim|poäng|p|%)$', '', s, flags=re.IGNORECASE)
    return s

def ratta_svar(u: Uppgift, input_svar) -> str:
    """Rättningslogik för alla uppgiftstyper."""
    if u.input_typ == 'flera_text':
        if all(str(s).strip() != "" for s in input_svar):
            try:
                anv_svar = [float(_rensa_enhet(str(s)).replace(',', '.')) for s in input_svar]
                ratt_svar_list = [float(x) for x in u.ratt_svar]
                
                if u.svarstyp in ['ekvationssystem', 'punkt', 'ordered_float']:
                    if len(anv_svar) != len(ratt_svar_list):
                        return 'format'
                    return 'ratt' if all(abs(a - r) <= u.tolerans for a, r in zip(anv_svar, ratt_svar_list)) else 'fel'
                else:
                    if len(anv_svar) != len(ratt_svar_list):
                        return 'format'
                    anv_sorted = sorted(anv_svar)
                    ratt_sorted = sorted(ratt_svar_list)
                    return 'ratt' if all(abs(a - r) <= u.tolerans for a, r in zip(anv_sorted, ratt_sorted)) else 'fel'
            except ValueError:
                return 'format'
        return 'tom'
        
    elif u.input_typ == 'text':
        svar_str = str(input_svar).strip()
        if not svar_str:
            return 'tom'
            
        try:
            if u.svarstyp == 'int':
                svar_clean = _rensa_enhet(svar_str).replace(",", ".")
                val = float(svar_clean)
                if not val.is_integer():
                    return 'fel'
                return 'ratt' if int(round(val)) == int(u.ratt_svar) else 'fel'
                
            elif u.svarstyp in ['float', 'procent']:
                svar_clean = _rensa_enhet(svar_str).replace(",", ".")
                return 'ratt' if abs(float(svar_clean) - float(u.ratt_svar)) <= u.tolerans else 'fel'

            elif u.svarstyp == 'ekvation_x':
                svar_clean = svar_str.replace(" ", "").replace("\xa0", "").replace(",", ".").lower()
                if not svar_clean.startswith("x="):
                    return 'format_saknar_x'
                elev_val = float(svar_clean[2:])
                facit_val = float(str(u.ratt_svar).replace(" ", "").lower()[2:])
                return 'ratt' if abs(elev_val - facit_val) <= u.tolerans else 'fel'

            elif u.svarstyp == 'ekvation_linje':
                svar_clean = svar_str.replace(" ", "").replace("\xa0", "").replace(",", ".").lower()
                if not svar_clean.startswith("y="):
                    return 'format_saknar_y'
                x = symbols('x')
                transformations = standard_transformations + (implicit_multiplication_application,)
                rhs_elev = parse_expr(svar_clean[2:].replace("^", "**"), transformations=transformations)
                facit_rhs_str = str(u.ratt_svar).replace(" ", "").lower()[2:].replace("^", "**")
                rhs_facit = parse_expr(facit_rhs_str, transformations=transformations)
                if not rhs_elev.free_symbols.issubset({x}):
                    return 'format'
                return 'ratt' if simplify(rhs_elev - rhs_facit) == 0 else 'fel'
                
            elif u.svarstyp == 'string_math':
                svar_clean = svar_str.replace(",", ".").replace(" ", "").replace("\xa0", "").replace("^", "**")
                transformations = standard_transformations + (implicit_multiplication_application,)
                expr_elev = parse_expr(svar_clean, transformations=transformations)
                ratt_str = str(u.ratt_svar).replace(" ", "").replace("^", "**")
                expr_facit = parse_expr(ratt_str, transformations=transformations)
                
                if simplify(expr_elev - expr_facit) != 0:
                    return 'fel'
                
                # Kontrollera att uttrycket faktiskt är utvecklat/förenklat
                if u.krav_inga_parenteser:
                    s_utan_neg_exp = re.sub(r'\*\*\(-\d+\)', '', svar_clean)
                    if '(' in s_utan_neg_exp or ')' in s_utan_neg_exp:
                        return 'ej_forenklad'
                
                # Kontrollera att gemensam faktor i nämnare är förkortad
                _, den_e = fraction(together(expr_elev))
                _, den_f = fraction(together(expr_facit))
                for sym in expr_facit.free_symbols.union(expr_elev.free_symbols):
                    deg_e = Poly(den_e, sym).degree() if sym in den_e.free_symbols else 0
                    deg_f = Poly(den_f, sym).degree() if sym in den_f.free_symbols else 0
                    if deg_e > deg_f:
                        return 'ej_forenklad'
                
                return 'ratt'
                
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
