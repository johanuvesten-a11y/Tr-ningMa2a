import math
import re
import streamlit as st
from sympy import Integer, Float, Rational, Symbol, parse_expr, simplify, symbols, fraction, together, Poly
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


def _tolka_tal(s: str) -> float:
    """Tolkar decimaltal, heltal och bråk (t.ex. 3/2) till float."""
    s_clean = _rensa_enhet(str(s)).replace(",", ".")
    if not s_clean or len(s_clean) > 40:
        raise ValueError("Ogiltigt tal")

    if re.fullmatch(r'[+-]?\d+/\d+', s_clean):
        talj, namn = s_clean.split("/")
        namn_int = int(namn)
        if namn_int == 0:
            raise ValueError("Division med noll")
        val = int(talj) / namn_int
    else:
        val = float(s_clean)

    if not math.isfinite(val):
        raise ValueError("Icke-ändligt tal")
    return val


def _forbered_matte_strang(s: str) -> str:
    """Normaliserar elevens inmatning och tolkar 1/2x som (1/2)*x."""
    s_clean = str(s).replace(",", ".").replace(" ", "").replace("\xa0", "").replace("^", "**")
    s_clean = re.sub(r'(?<![\w\)])(\d+/\d+)([a-zA-Z\(])', r'(\1)*\2', s_clean)
    return s_clean


def _saker_parse_expr(expr_str: str):
    """Parsar matematiska uttryck säkert med skydd mot tunga exponenter och okända symboler."""
    if not expr_str or len(expr_str) > 120:
        raise ValueError("Uttrycket är tomt eller för långt")
    if not re.fullmatch(r'[0-9a-zA-Z+\-*/().\s]+', expr_str):
        raise ValueError("Otillåtna tecken i uttrycket")
    if re.search(r'\*\*[^+\-*/()]*\*\*', expr_str):
        raise ValueError("Nästlade exponenter tillåts inte")
    for match in re.finditer(r'\*\*\s*\(?\s*[+-]?\s*(\d+)', expr_str):
        if int(match.group(1)) > 100:
            raise ValueError("För stor exponent")

    tillatna_vars = {name: symbols(name) for name in ['x', 'y', 'z', 'a', 'b', 'c', 'k', 'm', 'n', 't']}
    safe_globals = {'Integer': Integer, 'Float': Float, 'Rational': Rational, 'Symbol': Symbol}
    transformations = standard_transformations + (implicit_multiplication_application,)

    expr = parse_expr(
        expr_str,
        local_dict=tillatna_vars,
        global_dict=safe_globals,
        transformations=transformations
    )
    if not expr.free_symbols.issubset(set(tillatna_vars.values())):
        raise ValueError("Otillåten variabel")
    return expr


def check_faktoriserad(svar_str: str, ratt_str: str) -> str:
    """Kontrollerar att svaret är algebraiskt lika och uppdelat i faktorer."""
    svar_clean = _forbered_matte_strang(svar_str)
    ratt_clean = _forbered_matte_strang(ratt_str)
    try:
        expr_elev = _saker_parse_expr(svar_clean)
        expr_facit = _saker_parse_expr(ratt_clean)
    except Exception:
        return 'format'

    if simplify(expr_elev - expr_facit) != 0:
        return 'fel'

    if '**2' in ratt_clean or '^2' in ratt_str:
        if '(' not in svar_clean or ')' not in svar_clean:
            return 'ej_faktoriserad'
        if '**2' not in svar_clean and svar_clean.count('(') < 2:
            return 'ej_faktoriserad'
    else:
        if svar_clean.count('(') < ratt_clean.count('('):
            return 'ej_faktoriserad'

    return 'ratt'


def formatera_facit_text(u: Uppgift) -> str:
    """Formaterar facit snyggt utan rå Python-syntax (* eller **)."""
    if u.svarstyp in ['ekvationssystem', 'punkt']:
        return f"x = {u.ratt_svar[0]:g}, y = {u.ratt_svar[1]:g}".replace('.', ',')
    elif u.svarstyp == 'ordered_float':
        return f"μ = {u.ratt_svar[0]:g}, σ = {u.ratt_svar[1]:g}".replace('.', ',')
    elif u.svarstyp == 'array_float':
        return ' och '.join([f"{a:g}".replace('.', ',') for a in u.ratt_svar])
    elif isinstance(u.ratt_svar, float):
        return f"{u.ratt_svar:g}".replace('.', ',')

    txt = str(u.ratt_svar).strip()
    if u.svarstyp in ['string_math', 'faktoriserad', 'potensform', 'ekvation_linje', 'ekvation_x']:
        txt = txt.replace("**", "^")
        txt = re.sub(r'(\d)\*([a-zA-Z\(])', r'\1\2', txt)
        txt = re.sub(r'\)\*\(', r')(', txt)
        txt = re.sub(r'\s*\+\s*-\s*', ' - ', txt)
        txt = re.sub(r'(?<=[a-zA-Z0-9\)])\+(?=[a-zA-Z0-9\(])', ' + ', txt)
        txt = re.sub(r'(?<=[a-zA-Z0-9\)])-(?=[a-zA-Z0-9\(])', ' - ', txt)
        txt = re.sub(r'\s*=\s*', ' = ', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()
    return txt


def ratta_svar(u: Uppgift, input_svar) -> str:
    """Rättningslogik för alla uppgiftstyper."""
    if u.input_typ == 'flera_text':
        if all(str(s).strip() != "" for s in input_svar):
            try:
                anv_svar = [_tolka_tal(s) for s in input_svar]
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
                val = _tolka_tal(svar_str)
                if not val.is_integer():
                    return 'fel'
                return 'ratt' if int(round(val)) == int(u.ratt_svar) else 'fel'

            elif u.svarstyp in ['float', 'procent']:
                val = _tolka_tal(svar_str)
                return 'ratt' if abs(val - float(u.ratt_svar)) <= u.tolerans else 'fel'

            elif u.svarstyp == 'ekvation_x':
                svar_clean = svar_str.replace(" ", "").replace("\xa0", "").replace(",", ".").lower()
                if not svar_clean.startswith("x="):
                    return 'format_saknar_x'
                elev_val = _tolka_tal(svar_clean[2:])
                facit_val = _tolka_tal(str(u.ratt_svar).replace(" ", "").lower()[2:])
                return 'ratt' if abs(elev_val - facit_val) <= u.tolerans else 'fel'

            elif u.svarstyp == 'ekvation_linje':
                svar_clean = svar_str.replace(" ", "").replace("\xa0", "").replace(",", ".").lower()
                if not svar_clean.startswith("y="):
                    return 'format_saknar_y'
                x = symbols('x')
                rhs_elev = _saker_parse_expr(_forbered_matte_strang(svar_clean[2:]))
                facit_rhs_str = _forbered_matte_strang(str(u.ratt_svar).replace(" ", "").lower()[2:])
                rhs_facit = _saker_parse_expr(facit_rhs_str)
                if not rhs_elev.free_symbols.issubset({x}):
                    return 'format'
                return 'ratt' if simplify(rhs_elev - rhs_facit) == 0 else 'fel'

            elif u.svarstyp == 'potensform':
                svar_clean = _forbered_matte_strang(svar_str)
                ratt_clean = _forbered_matte_strang(str(u.ratt_svar))
                if svar_clean == ratt_clean:
                    return 'ratt'
                svar_no_paren = re.sub(r'\*\*\((\-?\d+)\)', r'**\1', svar_clean)
                if svar_no_paren == ratt_clean:
                    return 'ratt'
                expr_elev = _saker_parse_expr(svar_clean)
                expr_facit = _saker_parse_expr(ratt_clean)
                if simplify(expr_elev - expr_facit) == 0:
                    return 'ej_forenklad'
                return 'fel'

            elif u.svarstyp == 'faktoriserad':
                return check_faktoriserad(svar_str, str(u.ratt_svar))

            elif u.svarstyp == 'string_math':
                svar_clean = _forbered_matte_strang(svar_str)
                expr_elev = _saker_parse_expr(svar_clean)
                ratt_str = _forbered_matte_strang(str(u.ratt_svar))
                expr_facit = _saker_parse_expr(ratt_str)

                if simplify(expr_elev - expr_facit) != 0:
                    return 'fel'

                if u.krav_inga_parenteser:
                    s_utan_neg_exp = re.sub(r'\*\*\(-\d+\)', '', svar_clean)
                    if '(' in s_utan_neg_exp or ')' in s_utan_neg_exp:
                        return 'ej_forenklad'

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
