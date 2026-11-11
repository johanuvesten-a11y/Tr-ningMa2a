from dataclasses import dataclass, field
from typing import Optional, Any, Callable, List

@dataclass
class Uppgift:
    fraga: str
    ratt_svar: Any
    input_typ: str          # 'text', 'flera_text', 'radio', 'selectbox'
    svarstyp: str           # 'int', 'float', 'procent', 'array_float', 'string_math', 'string'
    visnings_kategori: str = ""
    
    # Text- & Layoutfält
    info_text: Optional[str] = None
    latex_text: Optional[str] = None
    info_box_text: Optional[str] = None
    info_box_style: Optional[str] = None  # 'blue', 'green', 'purple', 'pink'
    undertext: Optional[str] = None
    
    # Plotly-grafer & visualiseringar
    plotly_fig: Optional[Any] = None
    
    # Alternativ och extra visning
    alternativ: Optional[List[str]] = None
    suffix: Optional[str] = None
