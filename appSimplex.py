# -*- coding: utf-8 -*-
"""
🏭 EA Simplex Production Optimizer v1.0
Motor de Optimización de Producción Industrial basado en el Método Simplex.
Desarrollado en Python por el Ingeniero Maestro Erik Armenta.
EA Innovation & Solutions — Ciudad Juárez, MX.

"La exactitud es nuestra firma e innovar es nuestra naturaleza"
"""

# ============================================================
# IMPORTACIONES
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from scipy.optimize import linprog
from PIL import Image
from datetime import datetime
import io
import os
import tempfile
import json

# Importación opcional: PDF
try:
    from fpdf import FPDF
    PDF_ENABLED = True
except ImportError:
    PDF_ENABLED = False

# Importación opcional: Excel
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    EXCEL_ENABLED = True
except ImportError:
    EXCEL_ENABLED = False

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="EA Simplex Optimizer",
    layout="wide",
    page_icon="🏭",
    initial_sidebar_state="expanded"
)

# ============================================================
# PALETA DE COLORES CORPORATIVOS (Basada en el logo EA)
# ============================================================
COLORS = {
    "bg_dark": "#0D0D0D",
    "bg_card": "#1A1A1A",
    "bg_card_hover": "#242424",
    "red_primary": "#C62828",
    "red_light": "#EF5350",
    "red_gradient": "linear-gradient(135deg, #C62828, #E53935)",
    "gold_primary": "#F9A825",
    "gold_light": "#FDD835",
    "gold_gradient": "linear-gradient(135deg, #F9A825, #FDD835)",
    "white": "#FFFFFF",
    "text_primary": "#F5F5F5",
    "text_secondary": "#B0B0B0",
    "text_muted": "#707070",
    "border": "#333333",
    "success": "#00E676",
    "error": "#FF1744",
    "accent_blue": "#42A5F5",
}

# ============================================================
# INYECCIÓN CSS PREMIUM
# ============================================================
st.markdown(f"""
<style>
    /* ===== TIPOGRAFÍA PREMIUM ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* ===== RESET GLOBAL ===== */
    html {{
        overflow-y: scroll;
        scroll-behavior: smooth;
    }}

    .main {{
        background-color: {COLORS["bg_dark"]};
        font-family: 'Inter', sans-serif;
    }}

    /* ===== SIDEBAR PREMIUM ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #111111 0%, #1A1A1A 40%, #0D0D0D 100%);
        border-right: 1px solid {COLORS["border"]};
    }}

    [data-testid="stSidebar"] .stMarkdown h3 {{
        color: {COLORS["gold_primary"]} !important;
        font-weight: 700;
        letter-spacing: 1px;
        font-size: 14px;
        text-transform: uppercase;
    }}

    /* ===== ENCABEZADOS ===== */
    h1, h2, h3 {{
        font-family: 'Inter', sans-serif !important;
        color: {COLORS["text_primary"]} !important;
    }}

    /* ===== TARJETAS GLASSMORPHISM ===== */
    .glass-card {{
        background: rgba(26, 26, 26, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }}

    .glass-card:hover {{
        border-color: rgba(249, 168, 37, 0.2);
        box-shadow: 0 12px 48px rgba(249, 168, 37, 0.08);
        transform: translateY(-2px);
    }}

    /* ===== HEADER HERO ===== */
    .hero-header {{
        background: linear-gradient(135deg, #0D0D0D 0%, #1A1A1A 50%, #0D0D0D 100%);
        border: 1px solid {COLORS["border"]};
        border-radius: 20px;
        padding: 30px 40px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }}

    .hero-header::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {COLORS["red_primary"]}, {COLORS["gold_primary"]}, {COLORS["red_primary"]});
        animation: shimmer 3s ease-in-out infinite;
    }}

    @keyframes shimmer {{
        0%, 100% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
    }}

    .hero-title {{
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, {COLORS["white"]} 0%, {COLORS["gold_primary"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.2;
    }}

    .hero-subtitle {{
        color: {COLORS["text_secondary"]};
        font-size: 1rem;
        font-weight: 400;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 6px;
    }}

    .hero-slogan {{
        color: {COLORS["gold_primary"]};
        font-size: 0.85rem;
        font-style: italic;
        font-weight: 500;
        margin-top: 10px;
        opacity: 0.85;
    }}

    /* ===== MÉTRICAS KPI ===== */
    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin: 20px 0;
    }}

    .kpi-card {{
        background: linear-gradient(145deg, #1A1A1A, #222222);
        border: 1px solid {COLORS["border"]};
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }}

    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }}

    .kpi-card::after {{
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 3px;
    }}

    .kpi-card.red::after {{ background: {COLORS["red_primary"]}; }}
    .kpi-card.gold::after {{ background: {COLORS["gold_primary"]}; }}
    .kpi-card.success::after {{ background: {COLORS["success"]}; }}
    .kpi-card.blue::after {{ background: {COLORS["accent_blue"]}; }}

    .kpi-label {{
        font-size: 0.78rem;
        color: {COLORS["text_secondary"]};
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 8px;
    }}

    .kpi-value {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {COLORS["white"]};
        font-family: 'JetBrains Mono', monospace;
    }}

    .kpi-unit {{
        font-size: 0.8rem;
        color: {COLORS["text_muted"]};
        margin-top: 4px;
    }}

    /* ===== TABLAS PREMIUM ===== */
    .sensitivity-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
        margin: 16px 0;
        font-family: 'Inter', sans-serif;
    }}

    .sensitivity-table thead th {{
        background: linear-gradient(135deg, {COLORS["red_primary"]}, #D32F2F);
        color: white;
        padding: 14px 18px;
        text-align: left;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}

    .sensitivity-table tbody td {{
        padding: 12px 18px;
        border-bottom: 1px solid {COLORS["border"]};
        color: {COLORS["text_primary"]};
        font-size: 0.92rem;
        background: {COLORS["bg_card"]};
    }}

    .sensitivity-table tbody tr:hover td {{
        background: {COLORS["bg_card_hover"]};
    }}

    .sensitivity-table tbody tr:last-child td {{
        border-bottom: none;
    }}

    /* ===== BADGES / TAGS ===== */
    .status-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .badge-holgura {{ background: rgba(0, 230, 118, 0.15); color: {COLORS["success"]}; }}
    .badge-activa {{ background: rgba(198, 40, 40, 0.15); color: {COLORS["red_light"]}; }}
    .badge-max {{ background: rgba(249, 168, 37, 0.15); color: {COLORS["gold_primary"]}; }}
    .badge-min {{ background: rgba(66, 165, 245, 0.15); color: {COLORS["accent_blue"]}; }}

    /* ===== BOTONES PERSONALIZADOS ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS["red_primary"]}, #D32F2F) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-family: 'Inter', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(198, 40, 40, 0.3) !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(198, 40, 40, 0.45) !important;
    }}

    /* ===== DOWNLOAD BUTTONS ===== */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {COLORS["gold_primary"]}, #F9A825) !important;
        color: #0D0D0D !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        box-shadow: 0 4px 15px rgba(249, 168, 37, 0.3) !important;
    }}

    .stDownloadButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(249, 168, 37, 0.45) !important;
    }}

    /* ===== INPUTS ESTILIZADOS ===== */
    .stNumberInput input, .stTextInput input {{
        background-color: #1A1A1A !important;
        border: 1px solid {COLORS["border"]} !important;
        border-radius: 8px !important;
        color: {COLORS["text_primary"]} !important;
        font-family: 'JetBrains Mono', monospace !important;
    }}

    .stNumberInput input:focus, .stTextInput input:focus {{
        border-color: {COLORS["gold_primary"]} !important;
        box-shadow: 0 0 0 2px rgba(249, 168, 37, 0.2) !important;
    }}

    .stSelectbox > div > div {{
        background-color: #1A1A1A !important;
        border: 1px solid {COLORS["border"]} !important;
        border-radius: 8px !important;
    }}

    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {{
        background-color: {COLORS["bg_card"]} !important;
        border-radius: 10px !important;
        border: 1px solid {COLORS["border"]} !important;
        color: {COLORS["text_primary"]} !important;
        font-weight: 600 !important;
    }}

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: {COLORS["bg_card"]} !important;
        border-radius: 10px 10px 0 0 !important;
        border: 1px solid {COLORS["border"]} !important;
        color: {COLORS["text_secondary"]} !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS["red_primary"]}, #D32F2F) !important;
        color: white !important;
        border-color: {COLORS["red_primary"]} !important;
    }}

    /* ===== FOOTER ===== */
    .footer-premium {{
        background: linear-gradient(135deg, #111111, #1A1A1A);
        border-top: 1px solid {COLORS["border"]};
        border-radius: 16px;
        padding: 24px 32px;
        margin-top: 40px;
        text-align: center;
    }}

    .footer-slogan {{
        color: {COLORS["gold_primary"]};
        font-size: 0.95rem;
        font-weight: 600;
        font-style: italic;
        letter-spacing: 1.5px;
    }}

    .footer-credits {{
        color: {COLORS["text_muted"]};
        font-size: 0.78rem;
        margin-top: 8px;
    }}

    /* ===== SCROLL BAR PERSONALIZADO ===== */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: {COLORS["bg_dark"]}; }}
    ::-webkit-scrollbar-thumb {{ background: {COLORS["border"]}; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {COLORS["text_muted"]}; }}

    /* ===== ANIMACIÓN DE ENTRADA ===== */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .animate-in {{
        animation: fadeInUp 0.6s ease-out forwards;
    }}

    /* ===== SECCIÓN SEPARADOR ===== */
    .section-divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS["border"]}, transparent);
        margin: 30px 0;
    }}

    /* ===== PULSE ICON ===== */
    .pulse-icon {{
        display: inline-block;
        animation: pulse 2s ease-in-out infinite;
    }}

    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.15); }}
    }}

    /* Ocultar branding Streamlit */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}

</style>
""", unsafe_allow_html=True)

# ============================================================
# JAVASCRIPT PARA INTERACTIVIDAD AVANZADA
# ============================================================
st.markdown("""
<script>
    // Efecto ripple en botones
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'BUTTON') {
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255,255,255,0.3)';
            ripple.style.width = '100px';
            ripple.style.height = '100px';
            ripple.style.transform = 'translate(-50%, -50%)';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple-anim 0.6s ease-out forwards';
            e.target.style.position = 'relative';
            e.target.style.overflow = 'hidden';
            ripple.style.left = (e.clientX - e.target.getBoundingClientRect().left) + 'px';
            ripple.style.top = (e.clientY - e.target.getBoundingClientRect().top) + 'px';
            e.target.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        }
    });
</script>
<style>
    @keyframes ripple-anim {
        to { transform: translate(-50%, -50%) scale(4); opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def sanitize_text(text: str) -> str:
    """Sanitiza texto para compatibilidad PDF (latin-1)."""
    replacements = {
        '\u2014': ' - ', '\u2013': ' - ', '\u2022': '*', '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2018': "'", '\u2026': '...',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', '¿': '?', '¡': '!',
    }
    for uni, asc in replacements.items():
        text = text.replace(uni, asc)
    return text.encode('latin-1', errors='replace').decode('latin-1')


def resolver_simplex(c, A_ub, b_ub, objetivo="Maximizar"):
    """
    Resuelve el problema de programación lineal usando scipy.optimize.linprog.
    
    Parámetros:
    - c: vector de coeficientes de la función objetivo
    - A_ub: matriz de coeficientes de las restricciones (desigualdades <=)
    - b_ub: vector de límites de las restricciones
    - objetivo: "Maximizar" o "Minimizar"
    
    Retorna:
    - resultado: objeto OptimizeResult de scipy
    - variables_decision: valores óptimos de las variables de decisión
    - valor_objetivo: valor óptimo de la función objetivo
    - holguras: holguras de cada restricción (recurso sobrante)
    """
    # Si es maximización, negamos c (linprog siempre minimiza)
    c_interno = [-ci for ci in c] if objetivo == "Maximizar" else list(c)

    # Asegurar que no haya valores None o NaN
    A_ub = np.array(A_ub, dtype=float)
    b_ub = np.array(b_ub, dtype=float)
    c_interno = np.array(c_interno, dtype=float)

    # Restricciones de no-negatividad
    bounds = [(0, None) for _ in range(len(c_interno))]

    # Resolver con el método HiGHS (motor de alto rendimiento)
    resultado = linprog(
        c=c_interno,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=bounds,
        method='highs'
    )

    if resultado.success:
        variables_decision = resultado.x
        # Valor objetivo real (si maximizamos, revertimos el signo)
        valor_objetivo = -resultado.fun if objetivo == "Maximizar" else resultado.fun
        # Cálculo de holguras: b - A*x
        consumo = A_ub @ variables_decision
        holguras = b_ub - consumo
        return resultado, variables_decision, valor_objetivo, holguras, consumo
    else:
        return resultado, None, None, None, None


def generar_pdf_reporte(datos_reporte: dict) -> bytes:
    """
    Genera un PDF ejecutivo estilizado con los resultados de la optimización.
    Colores corporativos: Rojo (#C62828), Dorado (#F9A825), Negro (#0D0D0D).
    """
    if not PDF_ENABLED:
        return None

    class SimplexPDF(FPDF):
        def header(self):
            # Barra superior roja
            self.set_fill_color(198, 40, 40)  # Rojo corporativo
            self.rect(0, 0, 210, 8, 'F')
            # Barra dorada delgada
            self.set_fill_color(249, 168, 37)  # Dorado corporativo
            self.rect(0, 8, 210, 2, 'F')

            self.set_y(15)
            self.set_font('Helvetica', 'B', 20)
            self.set_text_color(198, 40, 40)
            self.cell(0, 10, 'EA SIMPLEX OPTIMIZER', align='C', new_x="LMARGIN", new_y="NEXT")

            self.set_font('Helvetica', '', 10)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, 'Reporte Ejecutivo de Optimizacion de Produccion', align='C', new_x="LMARGIN", new_y="NEXT")
            self.ln(4)

            # Línea separadora
            self.set_draw_color(198, 40, 40)
            self.set_line_width(0.5)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(6)

        def footer(self):
            self.set_y(-20)
            # Línea
            self.set_draw_color(249, 168, 37)
            self.set_line_width(0.3)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(3)
            self.set_font('Helvetica', 'I', 7)
            self.set_text_color(150, 150, 150)
            self.cell(0, 5, sanitize_text('"La exactitud es nuestra firma e innovar es nuestra naturaleza"'), align='C', new_x="LMARGIN", new_y="NEXT")
            self.cell(0, 5, f'Pagina {self.page_no()} | EA Innovation & Solutions | {datetime.now().strftime("%d/%m/%Y %H:%M")}', align='C')

    pdf = SimplexPDF()
    pdf.add_page()

    # === SECCIÓN 1: INFORMACIÓN GENERAL ===
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(198, 40, 40)
    pdf.cell(0, 8, '1. INFORMACION GENERAL', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    info_lines = [
        f"Objetivo: {datos_reporte['objetivo']}",
        f"Numero de Productos: {datos_reporte['num_productos']}",
        f"Numero de Restricciones: {datos_reporte['num_restricciones']}",
        f"Fecha de Generacion: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"Motor de Calculo: SciPy HiGHS (Metodo Simplex)",
    ]
    for line in info_lines:
        pdf.cell(0, 6, sanitize_text(line), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # === SECCIÓN 2: RESULTADO ÓPTIMO ===
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(198, 40, 40)
    pdf.cell(0, 8, '2. RESULTADO OPTIMO', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Gran número objetivo
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(249, 168, 37)  # Dorado
    valor_str = f"${datos_reporte['valor_objetivo']:,.2f}" if datos_reporte['objetivo'] == "Maximizar Utilidades" else f"${datos_reporte['valor_objetivo']:,.2f}"
    pdf.cell(0, 14, sanitize_text(valor_str), align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(120, 120, 120)
    label_obj = "Utilidad Maxima" if datos_reporte['objetivo'] == "Maximizar Utilidades" else "Costo Minimo"
    pdf.cell(0, 6, sanitize_text(label_obj), align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Tabla de producción óptima
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, 'Plan de Produccion Optimo:', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Encabezado de tabla
    pdf.set_fill_color(198, 40, 40)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    col_w = [70, 50, 50]
    headers = ['Producto', 'Cantidad Optima', 'Contribucion ($)']
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 8, sanitize_text(h), border=1, fill=True, align='C')
    pdf.ln()

    # Filas de datos
    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Helvetica', '', 9)
    for prod in datos_reporte['productos']:
        pdf.set_fill_color(240, 240, 240) if datos_reporte['productos'].index(prod) % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        fill = datos_reporte['productos'].index(prod) % 2 == 0
        pdf.cell(col_w[0], 7, sanitize_text(prod['nombre']), border=1, fill=fill, align='L')
        pdf.cell(col_w[1], 7, f"{prod['cantidad']:.2f}", border=1, fill=fill, align='C')
        pdf.cell(col_w[2], 7, f"${prod['contribucion']:,.2f}", border=1, fill=fill, align='C')
        pdf.ln()
    pdf.ln(6)

    # === SECCIÓN 3: ANÁLISIS DE SENSIBILIDAD ===
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(198, 40, 40)
    pdf.cell(0, 8, '3. ANALISIS DE SENSIBILIDAD DE RECURSOS', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Tabla de recursos
    pdf.set_fill_color(198, 40, 40)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    r_col_w = [50, 35, 35, 35, 30]
    r_headers = ['Recurso', 'Disponible', 'Consumido', 'Holgura', 'Estado']
    for i, h in enumerate(r_headers):
        pdf.cell(r_col_w[i], 8, sanitize_text(h), border=1, fill=True, align='C')
    pdf.ln()

    pdf.set_text_color(50, 50, 50)
    pdf.set_font('Helvetica', '', 9)
    for rec in datos_reporte['recursos']:
        idx = datos_reporte['recursos'].index(rec)
        pdf.set_fill_color(240, 240, 240) if idx % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        fill = idx % 2 == 0
        pdf.cell(r_col_w[0], 7, sanitize_text(rec['nombre']), border=1, fill=fill, align='L')
        pdf.cell(r_col_w[1], 7, f"{rec['disponible']:,.2f}", border=1, fill=fill, align='C')
        pdf.cell(r_col_w[2], 7, f"{rec['consumido']:,.2f}", border=1, fill=fill, align='C')
        pdf.cell(r_col_w[3], 7, f"{rec['holgura']:,.2f}", border=1, fill=fill, align='C')
        estado = "ACTIVA" if rec['holgura'] < 0.01 else "HOLGURA"
        pdf.cell(r_col_w[4], 7, estado, border=1, fill=fill, align='C')
        pdf.ln()

    pdf.ln(8)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(0, 5, sanitize_text(
        "Nota: Las restricciones con estado 'ACTIVA' (holgura = 0) son los cuellos de botella. "
        "Incrementar su disponibilidad mejoraria directamente el valor del objetivo. "
        "Las restricciones con 'HOLGURA' tienen recurso sobrante."
    ))

    return bytes(pdf.output())


def generar_excel_reporte(datos_reporte: dict) -> bytes:
    """
    Genera un archivo Excel estilizado con los resultados de la optimización.
    Usa colores corporativos: Rojo, Dorado, Negro.
    """
    if not EXCEL_ENABLED:
        return None

    wb = openpyxl.Workbook()

    # Estilos corporativos
    rojo_fill = PatternFill(start_color="C62828", end_color="C62828", fill_type="solid")
    dorado_fill = PatternFill(start_color="F9A825", end_color="F9A825", fill_type="solid")
    negro_fill = PatternFill(start_color="1A1A1A", end_color="1A1A1A", fill_type="solid")
    gris_claro = PatternFill(start_color="F5F5F5", end_color="F5F5F5", fill_type="solid")
    blanco_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    fuente_titulo = Font(name='Arial', bold=True, size=14, color="C62828")
    fuente_header = Font(name='Arial', bold=True, size=10, color="FFFFFF")
    fuente_datos = Font(name='Arial', size=10, color="333333")
    fuente_kpi = Font(name='Arial', bold=True, size=18, color="F9A825")
    fuente_subtitulo = Font(name='Arial', bold=True, size=11, color="C62828")

    alineacion_centro = Alignment(horizontal='center', vertical='center')
    alineacion_izq = Alignment(horizontal='left', vertical='center')

    borde_fino = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD')
    )

    # ===== HOJA 1: RESUMEN EJECUTIVO =====
    ws1 = wb.active
    ws1.title = "Resumen Ejecutivo"
    ws1.sheet_properties.tabColor = "C62828"

    # Ancho de columnas
    ws1.column_dimensions['A'].width = 5
    ws1.column_dimensions['B'].width = 30
    ws1.column_dimensions['C'].width = 25
    ws1.column_dimensions['D'].width = 25
    ws1.column_dimensions['E'].width = 20

    # Título
    ws1.merge_cells('B2:E2')
    cell = ws1['B2']
    cell.value = "EA SIMPLEX OPTIMIZER — Reporte Ejecutivo"
    cell.font = fuente_titulo
    cell.alignment = alineacion_centro

    # Subtítulo
    ws1.merge_cells('B3:E3')
    cell = ws1['B3']
    cell.value = f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Motor: SciPy HiGHS"
    cell.font = Font(name='Arial', size=9, color="999999", italic=True)
    cell.alignment = alineacion_centro

    # KPI Principal
    ws1.merge_cells('B5:E5')
    cell = ws1['B5']
    label_obj = "UTILIDAD MÁXIMA" if datos_reporte['objetivo'] == "Maximizar Utilidades" else "COSTO MÍNIMO"
    cell.value = label_obj
    cell.font = fuente_subtitulo
    cell.alignment = alineacion_centro

    ws1.merge_cells('B6:E6')
    cell = ws1['B6']
    cell.value = f"${datos_reporte['valor_objetivo']:,.2f}"
    cell.font = fuente_kpi
    cell.alignment = alineacion_centro
    cell.fill = negro_fill

    # Tabla Producción
    row = 9
    ws1.cell(row=row, column=2, value="PLAN DE PRODUCCIÓN ÓPTIMO").font = fuente_subtitulo
    row += 1

    headers_prod = ["Producto", "Cantidad Óptima", "Contribución ($)"]
    for j, h in enumerate(headers_prod):
        cell = ws1.cell(row=row, column=j+2, value=h)
        cell.font = fuente_header
        cell.fill = rojo_fill
        cell.alignment = alineacion_centro
        cell.border = borde_fino
    row += 1

    for i, prod in enumerate(datos_reporte['productos']):
        fill = gris_claro if i % 2 == 0 else blanco_fill
        ws1.cell(row=row, column=2, value=prod['nombre']).font = fuente_datos
        ws1.cell(row=row, column=2).fill = fill
        ws1.cell(row=row, column=2).border = borde_fino

        ws1.cell(row=row, column=3, value=round(prod['cantidad'], 2)).font = fuente_datos
        ws1.cell(row=row, column=3).fill = fill
        ws1.cell(row=row, column=3).alignment = alineacion_centro
        ws1.cell(row=row, column=3).border = borde_fino

        ws1.cell(row=row, column=4, value=round(prod['contribucion'], 2)).font = fuente_datos
        ws1.cell(row=row, column=4).fill = fill
        ws1.cell(row=row, column=4).alignment = alineacion_centro
        ws1.cell(row=row, column=4).border = borde_fino
        ws1.cell(row=row, column=4).number_format = '$#,##0.00'
        row += 1

    # ===== HOJA 2: ANÁLISIS DE SENSIBILIDAD =====
    ws2 = wb.create_sheet("Analisis de Sensibilidad")
    ws2.sheet_properties.tabColor = "F9A825"

    ws2.column_dimensions['A'].width = 5
    ws2.column_dimensions['B'].width = 28
    ws2.column_dimensions['C'].width = 18
    ws2.column_dimensions['D'].width = 18
    ws2.column_dimensions['E'].width = 18
    ws2.column_dimensions['F'].width = 18
    ws2.column_dimensions['G'].width = 15

    ws2.merge_cells('B2:G2')
    cell = ws2['B2']
    cell.value = "ANÁLISIS DE SENSIBILIDAD DE RECURSOS"
    cell.font = fuente_titulo
    cell.alignment = alineacion_centro

    row = 4
    headers_rec = ["Recurso", "Disponible", "Consumido", "Holgura", "% Utilización", "Estado"]
    for j, h in enumerate(headers_rec):
        cell = ws2.cell(row=row, column=j+2, value=h)
        cell.font = fuente_header
        cell.fill = rojo_fill
        cell.alignment = alineacion_centro
        cell.border = borde_fino
    row += 1

    for i, rec in enumerate(datos_reporte['recursos']):
        fill = gris_claro if i % 2 == 0 else blanco_fill
        pct_uso = (rec['consumido'] / rec['disponible'] * 100) if rec['disponible'] > 0 else 0
        estado = "ACTIVA" if rec['holgura'] < 0.01 else "HOLGURA"

        ws2.cell(row=row, column=2, value=rec['nombre']).font = fuente_datos
        ws2.cell(row=row, column=2).fill = fill
        ws2.cell(row=row, column=2).border = borde_fino

        ws2.cell(row=row, column=3, value=round(rec['disponible'], 2)).font = fuente_datos
        ws2.cell(row=row, column=3).fill = fill
        ws2.cell(row=row, column=3).alignment = alineacion_centro
        ws2.cell(row=row, column=3).border = borde_fino

        ws2.cell(row=row, column=4, value=round(rec['consumido'], 2)).font = fuente_datos
        ws2.cell(row=row, column=4).fill = fill
        ws2.cell(row=row, column=4).alignment = alineacion_centro
        ws2.cell(row=row, column=4).border = borde_fino

        ws2.cell(row=row, column=5, value=round(rec['holgura'], 2)).font = fuente_datos
        ws2.cell(row=row, column=5).fill = fill
        ws2.cell(row=row, column=5).alignment = alineacion_centro
        ws2.cell(row=row, column=5).border = borde_fino

        ws2.cell(row=row, column=6, value=round(pct_uso, 1)).font = fuente_datos
        ws2.cell(row=row, column=6).fill = fill
        ws2.cell(row=row, column=6).alignment = alineacion_centro
        ws2.cell(row=row, column=6).border = borde_fino
        ws2.cell(row=row, column=6).number_format = '0.0"%"'

        cell_estado = ws2.cell(row=row, column=7, value=estado)
        cell_estado.font = Font(name='Arial', bold=True, size=10, color="C62828" if estado == "ACTIVA" else "388E3C")
        cell_estado.fill = PatternFill(start_color="FFEBEE" if estado == "ACTIVA" else "E8F5E9", end_color="FFEBEE" if estado == "ACTIVA" else "E8F5E9", fill_type="solid")
        cell_estado.alignment = alineacion_centro
        cell_estado.border = borde_fino
        row += 1

    # Slogan al final
    row += 2
    ws2.merge_cells(f'B{row}:G{row}')
    cell = ws2.cell(row=row, column=2, value='"La exactitud es nuestra firma e innovar es nuestra naturaleza"')
    cell.font = Font(name='Arial', size=9, color="F9A825", italic=True)
    cell.alignment = alineacion_centro

    # Guardar en buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


# ============================================================
# HEADER PRINCIPAL CON LOGO
# ============================================================
with st.container():
    col_logo, col_titulo = st.columns([1, 7])
    with col_logo:
        try:
            logo = Image.open("EA_2.png")
            st.image(logo, use_container_width=True)
        except Exception:
            st.markdown("<div style='font-size:50px; text-align:center;'>🏭</div>", unsafe_allow_html=True)
    with col_titulo:
        st.markdown("""
        <div class="hero-header">
            <p class="hero-title">🏭 Simplex Production Optimizer</p>
            <p class="hero-subtitle">Motor de Optimización Industrial • Método Simplex HiGHS</p>
            <p class="hero-slogan">"La exactitud es nuestra firma e innovar es nuestra naturaleza"</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR — CONFIGURACIÓN DEL PROBLEMA
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ CONFIGURACIÓN DEL PROBLEMA")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Tipo de objetivo
    tipo_objetivo = st.selectbox(
        "🎯 Tipo de Objetivo",
        ["Maximizar Utilidades", "Minimizar Costos"],
        index=0,
        help="Selecciona si deseas maximizar ganancias o minimizar costos de producción."
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Número de productos
    num_productos = st.slider(
        "📦 Número de Productos",
        min_value=2, max_value=10, value=3,
        help="Cantidad de productos o artículos a optimizar en la línea de producción."
    )

    # Número de restricciones
    num_restricciones = st.slider(
        "🔗 Número de Restricciones",
        min_value=1, max_value=10, value=3,
        help="Cantidad de restricciones (recursos, horas máquina, materia prima, etc.)."
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Info del motor
    st.markdown("""
    <div style="background: rgba(249,168,37,0.08); border: 1px solid rgba(249,168,37,0.2); 
                border-radius: 10px; padding: 14px; margin-top: 10px;">
        <p style="color: #F9A825; font-weight: 700; font-size: 0.8rem; margin: 0;">
            ⚡ MOTOR DE CÁLCULO
        </p>
        <p style="color: #B0B0B0; font-size: 0.75rem; margin: 5px 0 0 0;">
            SciPy • linprog • HiGHS<br>
            Optimización de Alta Precisión
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <p style="color: #707070; font-size: 0.7rem;">
            EA Innovation & Solutions<br>
            Cd. Juárez, MX
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SECCIÓN PRINCIPAL — ENTRADA DE DATOS
# ============================================================

# --- TABS PRINCIPALES ---
tab_datos, tab_resultados, tab_sensibilidad, tab_exportar = st.tabs([
    "📋 Datos del Problema",
    "📊 Resultados Óptimos",
    "🔬 Análisis de Sensibilidad",
    "📥 Exportar Reportes"
])

# ============================================================
# TAB 1: ENTRADA DE DATOS
# ============================================================
with tab_datos:
    st.markdown("""
    <div class="glass-card animate-in">
        <h3 style="color: #F9A825; margin-top: 0;">📦 Configuración de Productos</h3>
        <p style="color: #B0B0B0; font-size: 0.9rem;">
            Define los productos de tu línea de manufactura y su margen de utilidad (o costo) por unidad.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Nombres y Márgenes de Productos ---
    nombres_productos = []
    margenes = []

    cols_prod = st.columns(min(num_productos, 5))  # Máximo 5 columnas por fila
    for i in range(num_productos):
        col_idx = i % min(num_productos, 5)
        with cols_prod[col_idx]:
            nombre = st.text_input(
                f"Producto {i+1}",
                value=f"Producto {i+1}",
                key=f"nombre_prod_{i}",
                help=f"Nombre identificador del producto {i+1}"
            )
            label_margen = "💰 Utilidad/unidad ($)" if tipo_objetivo == "Maximizar Utilidades" else "💲 Costo/unidad ($)"
            margen = st.number_input(
                label_margen,
                min_value=0.0,
                value=float((i + 1) * 10),
                step=0.5,
                key=f"margen_prod_{i}",
                format="%.2f"
            )
            nombres_productos.append(nombre)
            margenes.append(margen)

    # Indicador visual de la función objetivo
    if tipo_objetivo == "Maximizar Utilidades":
        emoji_obj = "📈"
        color_obj = COLORS["gold_primary"]
        label_tipo = "MAX"
    else:
        emoji_obj = "📉"
        color_obj = COLORS["accent_blue"]
        label_tipo = "MIN"

    # Construcción de la función objetivo en formato legible
    terminos = [f"{margenes[i]:.0f}·{nombres_productos[i]}" for i in range(num_productos)]
    funcion_str = " + ".join(terminos)

    st.markdown(f"""
    <div class="glass-card" style="border-left: 3px solid {color_obj};">
        <p style="color: {COLORS['text_secondary']}; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px;">
            {emoji_obj} Función Objetivo
        </p>
        <p style="color: {COLORS['white']}; font-size: 1.1rem; font-family: 'JetBrains Mono', monospace;">
            <span class="status-badge badge-{'max' if label_tipo == 'MAX' else 'min'}">{label_tipo}</span>
            &nbsp; Z = {funcion_str}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # --- RESTRICCIONES ---
    st.markdown("""
    <div class="glass-card animate-in">
        <h3 style="color: #C62828; margin-top: 0;">🔗 Restricciones de Recursos</h3>
        <p style="color: #B0B0B0; font-size: 0.9rem;">
            Ingresa los coeficientes técnicos (consumo por unidad de cada producto) y el límite disponible para cada recurso.
        </p>
    </div>
    """, unsafe_allow_html=True)

    nombres_restricciones = []
    coeficientes_restricciones = []
    limites = []

    nombres_default_restricciones = [
        "Horas Máquina", "Materia Prima (kg)", "Mano de Obra (hrs)",
        "Energía (kWh)", "Espacio Almacén (m²)", "Transporte (km)",
        "Presupuesto ($)", "Agua (L)", "Tiempo Horno (min)", "Empaque (unid)"
    ]

    for j in range(num_restricciones):
        st.markdown(f"""
        <div style="background: rgba(198,40,40,0.05); border: 1px solid rgba(198,40,40,0.15);
                    border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <p style="color: #C62828; font-weight: 700; font-size: 0.85rem; margin: 0 0 8px 0;">
                🔗 Restricción {j+1}
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_name, col_limit = st.columns([2, 1])
        with col_name:
            nombre_rest = st.text_input(
                f"Nombre del recurso",
                value=nombres_default_restricciones[j] if j < len(nombres_default_restricciones) else f"Recurso {j+1}",
                key=f"nombre_rest_{j}"
            )
            nombres_restricciones.append(nombre_rest)
        with col_limit:
            limite = st.number_input(
                f"Límite disponible",
                min_value=0.0,
                value=100.0,
                step=1.0,
                key=f"limite_rest_{j}",
                format="%.2f"
            )
            limites.append(limite)

        # Coeficientes de la restricción (consumo por producto)
        cols_coef = st.columns(num_productos)
        coefs_fila = []
        for i in range(num_productos):
            with cols_coef[i]:
                coef = st.number_input(
                    f"{nombres_productos[i]}",
                    min_value=0.0,
                    value=1.0,
                    step=0.1,
                    key=f"coef_{j}_{i}",
                    format="%.2f",
                    help=f"Consumo de '{nombre_rest}' por cada unidad de '{nombres_productos[i]}'"
                )
                coefs_fila.append(coef)
        coeficientes_restricciones.append(coefs_fila)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Mostrar resumen del modelo en una tabla
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #F9A825; margin-top: 0;">📋 Resumen del Modelo</h3>
    </div>
    """, unsafe_allow_html=True)

    # Construir dataframe del modelo
    df_modelo = pd.DataFrame(
        coeficientes_restricciones,
        columns=nombres_productos,
        index=nombres_restricciones
    )
    df_modelo["Límite"] = limites
    st.dataframe(df_modelo, use_container_width=True)

    # --- BOTÓN RESOLVER ---
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
    with col_btn2:
        resolver = st.button("⚡ OPTIMIZAR", use_container_width=True, type="primary")


# ============================================================
# LÓGICA DE RESOLUCIÓN
# ============================================================
if resolver:
    with st.spinner("🔄 Ejecutando motor Simplex HiGHS..."):
        try:
            # Preparar datos para linprog
            c = margenes
            A_ub = coeficientes_restricciones
            b_ub = limites

            resultado, variables, valor_obj, holguras, consumo = resolver_simplex(
                c, A_ub, b_ub, 
                "Maximizar" if tipo_objetivo == "Maximizar Utilidades" else "Minimizar"
            )

            if resultado.success:
                # Guardar resultados en session_state para las otras tabs
                st.session_state['resultado_simplex'] = {
                    'success': True,
                    'variables': variables.tolist(),
                    'valor_objetivo': float(valor_obj),
                    'holguras': holguras.tolist(),
                    'consumo': consumo.tolist(),
                    'nombres_productos': nombres_productos,
                    'margenes': margenes,
                    'nombres_restricciones': nombres_restricciones,
                    'limites': limites,
                    'coeficientes': coeficientes_restricciones,
                    'tipo_objetivo': tipo_objetivo,
                    'mensaje': resultado.message,
                    'iteraciones': resultado.nit if hasattr(resultado, 'nit') else 0,
                    'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                }
                st.success("✅ ¡Solución óptima encontrada! Navega a las pestañas de resultados.")
                st.balloons()
            else:
                st.session_state['resultado_simplex'] = {
                    'success': False,
                    'mensaje': resultado.message
                }
                st.error(f"❌ No se encontró solución factible: {resultado.message}")

        except Exception as e:
            st.error(f"⚠️ Error en el motor de cálculo: {str(e)}")
            st.session_state['resultado_simplex'] = {
                'success': False,
                'mensaje': str(e)
            }


# ============================================================
# TAB 2: RESULTADOS ÓPTIMOS
# ============================================================
with tab_resultados:
    if 'resultado_simplex' not in st.session_state or not st.session_state['resultado_simplex'].get('success'):
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 60px;">
            <p class="pulse-icon" style="font-size: 60px;">⏳</p>
            <h2 style="color: #F5F5F5;">Esperando Optimización</h2>
            <p style="color: #B0B0B0;">
                Configura los datos del problema en la pestaña "Datos del Problema" y presiona 
                <strong style="color: #C62828;">⚡ OPTIMIZAR</strong> para ver los resultados.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        res = st.session_state['resultado_simplex']

        # --- KPI PRINCIPAL ---
        label_valor = "Utilidad Máxima" if res['tipo_objetivo'] == "Maximizar Utilidades" else "Costo Mínimo"
        color_kpi = COLORS["gold_primary"] if res['tipo_objetivo'] == "Maximizar Utilidades" else COLORS["accent_blue"]

        st.markdown(f"""
        <div class="glass-card animate-in" style="text-align: center; border-top: 3px solid {color_kpi};">
            <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; text-transform: uppercase; 
                      letter-spacing: 3px; margin-bottom: 8px;">
                {'📈' if 'Maximizar' in res['tipo_objetivo'] else '📉'} {label_valor}
            </p>
            <p style="font-size: 3.2rem; font-weight: 900; color: {color_kpi}; 
                      font-family: 'JetBrains Mono', monospace; margin: 0; line-height: 1;">
                ${res['valor_objetivo']:,.2f}
            </p>
            <p style="color: {COLORS['text_muted']}; font-size: 0.8rem; margin-top: 10px;">
                Motor: SciPy HiGHS • Ejecutado: {res['timestamp']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # --- KPI Cards por producto (componentes nativos de Streamlit) ---
        contribuciones = [res['variables'][i] * res['margenes'][i] for i in range(len(res['variables']))]

        cols_kpi = st.columns(len(res['nombres_productos']))
        for i, (nombre, cantidad) in enumerate(zip(res['nombres_productos'], res['variables'])):
            with cols_kpi[i]:
                st.metric(
                    label=f"📦 {nombre}",
                    value=f"{cantidad:,.2f} uds",
                    delta=f"${contribuciones[i]:,.2f}",
                    delta_color="normal"
                )

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # --- GRÁFICO PLOTLY: Plan de Producción ---
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #F9A825; margin-top: 0;">📊 Plan de Producción Óptimo</h3>
        </div>
        """, unsafe_allow_html=True)

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            # Gráfico de barras con Plotly
            df_prod = pd.DataFrame({
                'Producto': res['nombres_productos'],
                'Cantidad': res['variables'],
                'Contribución': contribuciones
            })

            fig_barras = go.Figure()
            fig_barras.add_trace(go.Bar(
                x=df_prod['Producto'],
                y=df_prod['Cantidad'],
                name='Cantidad Óptima',
                marker=dict(
                    color=df_prod['Cantidad'],
                    colorscale=[[0, '#C62828'], [0.5, '#E53935'], [1, '#F9A825']],
                    line=dict(color='rgba(255,255,255,0.15)', width=1.5)
                ),
                text=[f"{v:,.1f}" for v in df_prod['Cantidad']],
                textposition='outside',
                textfont=dict(color='#F5F5F5', size=15, family='Inter')
            ))
            fig_barras.update_layout(
                title=dict(text="Unidades Óptimas por Producto", font=dict(color='#FFFFFF', size=18, family='Inter')),
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(26,26,26,0.8)',
                font=dict(family='Inter', color='#E0E0E0', size=13),
                xaxis=dict(gridcolor='rgba(255,255,255,0.06)', tickfont=dict(size=13, color='#E0E0E0')),
                yaxis=dict(gridcolor='rgba(255,255,255,0.06)', title='Unidades', title_font=dict(size=14, color='#F9A825'), tickfont=dict(size=12, color='#E0E0E0')),
                showlegend=False,
                height=420,
                margin=dict(t=70, b=50)
            )
            st.plotly_chart(fig_barras, use_container_width=True)

        with col_chart2:
            # Gráfico de dona Plotly — Contribución al objetivo
            colors_pie = ['#C62828', '#F9A825', '#E53935', '#FDD835', '#42A5F5',
                          '#EF5350', '#FFB74D', '#66BB6A', '#AB47BC', '#26A69A']
            fig_dona = go.Figure(data=[go.Pie(
                labels=df_prod['Producto'],
                values=df_prod['Contribución'],
                hole=0.55,
                marker=dict(colors=colors_pie[:len(df_prod)], line=dict(color='#0D0D0D', width=2)),
                textinfo='label+percent',
                textfont=dict(size=14, color='#FFFFFF', family='Inter'),
                insidetextfont=dict(size=13, color='#FFFFFF'),
                outsidetextfont=dict(size=13, color='#E0E0E0'),
                hovertemplate='<b>%{label}</b><br>Contribución: $%{value:,.2f}<br>Porcentaje: %{percent}<extra></extra>'
            )])
            fig_dona.update_layout(
                title=dict(text="Distribución de Contribución", font=dict(color='#FFFFFF', size=18, family='Inter')),
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(26,26,26,0.8)',
                font=dict(family='Inter', color='#E0E0E0', size=13),
                showlegend=True,
                legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5, font=dict(size=12, color='#E0E0E0')),
                height=420,
                margin=dict(t=70, b=60),
                annotations=[dict(
                    text=f"<b>${res['valor_objetivo']:,.0f}</b>",
                    x=0.5, y=0.5, font_size=22, font_color=COLORS['gold_primary'],
                    showarrow=False, font_family='Inter'
                )]
            )
            st.plotly_chart(fig_dona, use_container_width=True)

        # --- GRÁFICO ALTAIR: Comparativa de Contribuciones ---
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #C62828; margin-top: 0;">📈 Análisis Comparativo — Altair</h3>
        </div>
        """, unsafe_allow_html=True)

        df_altair = pd.DataFrame({
            'Producto': res['nombres_productos'],
            'Cantidad Producida': res['variables'],
            'Margen Unitario ($)': res['margenes'],
            'Contribución Total ($)': contribuciones
        })

        # Gráfico de barras horizontales Altair
        chart_altair = alt.Chart(df_altair).mark_bar(
            cornerRadiusTopRight=8,
            cornerRadiusBottomRight=8,
        ).encode(
            x=alt.X('Contribución Total ($):Q', title='Contribución Total ($)'),
            y=alt.Y('Producto:N', sort='-x', title=''),
            color=alt.Color('Contribución Total ($):Q',
                            scale=alt.Scale(scheme='redyellowgreen'),
                            legend=None),
            tooltip=[
                alt.Tooltip('Producto:N'),
                alt.Tooltip('Cantidad Producida:Q', format=',.2f'),
                alt.Tooltip('Margen Unitario ($):Q', format='$,.2f'),
                alt.Tooltip('Contribución Total ($):Q', format='$,.2f'),
            ]
        ).properties(
            height=max(200, len(df_altair) * 60),
            title=alt.Title(
                text='Contribución por Producto al Objetivo',
                subtitle='Ordenado de mayor a menor impacto',
                color='#FFFFFF',
                subtitleColor='#CCCCCC',
                fontSize=16,
                subtitleFontSize=12
            )
        ).configure(
            background='rgba(26,26,26,0.8)',
        ).configure_axis(
            labelColor='#E0E0E0',
            labelFontSize=13,
            titleColor='#F9A825',
            titleFontSize=14,
            gridColor='rgba(255,255,255,0.06)',
        ).configure_title(
            color='#FFFFFF',
            fontSize=16
        )

        st.altair_chart(chart_altair, use_container_width=True)


# ============================================================
# TAB 3: ANÁLISIS DE SENSIBILIDAD
# ============================================================
with tab_sensibilidad:
    if 'resultado_simplex' not in st.session_state or not st.session_state['resultado_simplex'].get('success'):
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 60px;">
            <p class="pulse-icon" style="font-size: 60px;">🔬</p>
            <h2 style="color: #F5F5F5;">Análisis Pendiente</h2>
            <p style="color: #B0B0B0;">
                Primero ejecuta la optimización para visualizar el análisis de sensibilidad de recursos.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        res = st.session_state['resultado_simplex']

        st.markdown("""
        <div class="glass-card animate-in">
            <h3 style="color: #C62828; margin-top: 0;">🔬 Análisis de Sensibilidad de Recursos</h3>
            <p style="color: #B0B0B0; font-size: 0.9rem;">
                Este análisis muestra el estado de cada restricción: cuánto recurso se consumió, 
                cuánto sobró (holgura) y qué restricciones son cuellos de botella (activas).
            </p>
        </div>
        """, unsafe_allow_html=True)

        # --- Tabla de sensibilidad con st.columns (Streamlit nativo) ---
        restricciones_activas = 0

        # Encabezados de la tabla usando columnas de Streamlit
        col_h1, col_h2, col_h3, col_h4, col_h5, col_h6 = st.columns([2, 1.2, 1.2, 1.2, 1.5, 1.2])
        col_h1.markdown("**🔗 Recurso**")
        col_h2.markdown("**📦 Disponible**")
        col_h3.markdown("**⚙️ Consumido**")
        col_h4.markdown("**📐 Holgura**")
        col_h5.markdown("**📊 % Utilización**")
        col_h6.markdown("**🏷️ Estado**")
        st.markdown("---")

        for j in range(len(res['nombres_restricciones'])):
            disponible = res['limites'][j]
            consumido = res['consumo'][j]
            holgura = res['holguras'][j]
            pct = (consumido / disponible * 100) if disponible > 0 else 0
            es_activa = holgura < 0.01

            if es_activa:
                restricciones_activas += 1

            c1, c2, c3, c4, c5, c6 = st.columns([2, 1.2, 1.2, 1.2, 1.5, 1.2])
            c1.markdown(f"**{res['nombres_restricciones'][j]}**")
            c2.markdown(f"`{disponible:,.2f}`")
            c3.markdown(f"`{consumido:,.2f}`")
            color_hol = "🔴" if es_activa else "🟢"
            c4.markdown(f"{color_hol} `{holgura:,.2f}`")
            c5.progress(min(pct / 100.0, 1.0), text=f"{pct:.1f}%")
            if es_activa:
                c6.error("⛔ ACTIVA")
            else:
                c6.success("✅ HOLGURA")

        # --- KPIs de sensibilidad ---
        total_restricciones = len(res['nombres_restricciones'])
        pct_cuellos = (restricciones_activas / total_restricciones * 100) if total_restricciones > 0 else 0

        st.markdown(f"""
        <div class="kpi-container" style="margin-top: 24px;">
            <div class="kpi-card red">
                <p class="kpi-label">⛔ Cuellos de Botella</p>
                <p class="kpi-value">{restricciones_activas}</p>
                <p class="kpi-unit">restricción(es) activa(s)</p>
            </div>
            <div class="kpi-card gold">
                <p class="kpi-label">✅ Con Holgura</p>
                <p class="kpi-value">{total_restricciones - restricciones_activas}</p>
                <p class="kpi-unit">recurso(s) disponible(s)</p>
            </div>
            <div class="kpi-card blue">
                <p class="kpi-label">📊 Saturación Promedio</p>
                <p class="kpi-value">{np.mean([(res['consumo'][j] / res['limites'][j] * 100) if res['limites'][j] > 0 else 0 for j in range(len(res['limites']))]):.1f}%</p>
                <p class="kpi-unit">utilización media</p>
            </div>
            <div class="kpi-card success">
                <p class="kpi-label">🏭 Presión de Planta</p>
                <p class="kpi-value">{pct_cuellos:.0f}%</p>
                <p class="kpi-unit">de restricciones saturadas</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # --- GRÁFICO PLOTLY: Consumo vs Límite ---
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #F9A825; margin-top: 0;">📊 Consumo vs. Disponibilidad de Recursos</h3>
        </div>
        """, unsafe_allow_html=True)

        df_recursos = pd.DataFrame({
            'Recurso': res['nombres_restricciones'],
            'Disponible': res['limites'],
            'Consumido': res['consumo'],
            'Holgura': res['holguras']
        })

        fig_recursos = go.Figure()
        fig_recursos.add_trace(go.Bar(
            name='Consumido',
            x=df_recursos['Recurso'],
            y=df_recursos['Consumido'],
            marker_color='#C62828',
            text=[f"{v:,.1f}" for v in df_recursos['Consumido']],
            textposition='inside',
            textfont=dict(color='#FFFFFF', size=14, family='Inter')
        ))
        fig_recursos.add_trace(go.Bar(
            name='Holgura (sobrante)',
            x=df_recursos['Recurso'],
            y=df_recursos['Holgura'],
            marker_color='#F9A825',
            text=[f"{v:,.1f}" for v in df_recursos['Holgura']],
            textposition='inside',
            textfont=dict(color='#0D0D0D', size=14, family='Inter')
        ))
        fig_recursos.add_trace(go.Scatter(
            name='Límite Disponible',
            x=df_recursos['Recurso'],
            y=df_recursos['Disponible'],
            mode='markers+lines+text',
            marker=dict(color='#FFFFFF', size=10, symbol='diamond'),
            line=dict(color='rgba(255,255,255,0.4)', width=2, dash='dot'),
            text=[f"{v:,.0f}" for v in df_recursos['Disponible']],
            textposition='top center',
            textfont=dict(color='#FFFFFF', size=12, family='Inter')
        ))
        fig_recursos.update_layout(
            barmode='stack',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26,26,26,0.8)',
            font=dict(family='Inter', color='#E0E0E0', size=13),
            xaxis=dict(gridcolor='rgba(255,255,255,0.06)', title='', tickfont=dict(size=13, color='#E0E0E0')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.06)', title='Cantidad', title_font=dict(size=14, color='#F9A825'), tickfont=dict(size=12, color='#E0E0E0')),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5, font=dict(size=13, color='#E0E0E0')),
            height=470,
            margin=dict(t=70, b=50)
        )
        st.plotly_chart(fig_recursos, use_container_width=True)

        # --- GRÁFICO ALTAIR: Gauge de utilización ---
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #C62828; margin-top: 0;">📈 Porcentaje de Utilización por Recurso — Altair</h3>
        </div>
        """, unsafe_allow_html=True)

        # Calcular nivel de utilización para colorear las barras
        pct_list = [(res['consumo'][j] / res['limites'][j] * 100) if res['limites'][j] > 0 else 0 for j in range(len(res['limites']))]
        nivel_list = []
        for p in pct_list:
            if p > 95:
                nivel_list.append('Crítico (>95%)')
            elif p > 70:
                nivel_list.append('Presión (>70%)')
            else:
                nivel_list.append('Óptimo (≤70%)')

        df_uso = pd.DataFrame({
            'Recurso': res['nombres_restricciones'],
            'Pct_Utilizacion': pct_list,
            'Nivel': nivel_list,
            'Estado': ['Cuello de Botella' if res['holguras'][j] < 0.01 else 'Disponible' for j in range(len(res['holguras']))]
        })

        # Gráfico de barras - colores basados en columna 'Nivel'
        barras_uso = alt.Chart(df_uso).mark_bar(
            cornerRadiusTopRight=10,
            cornerRadiusBottomRight=10,
            height=28
        ).encode(
            x=alt.X('Pct_Utilizacion:Q', scale=alt.Scale(domain=[0, 110]), title='% Utilización del Recurso'),
            y=alt.Y('Recurso:N', sort='-x', title=''),
            color=alt.Color('Nivel:N',
                scale=alt.Scale(
                    domain=['Crítico (>95%)', 'Presión (>70%)', 'Óptimo (≤70%)'],
                    range=['#C62828', '#F9A825', '#00E676']
                ),
                legend=alt.Legend(title='Nivel de Uso', orient='bottom', labelFontSize=12, titleFontSize=13, labelColor='#E0E0E0', titleColor='#F9A825')
            ),
            tooltip=[
                alt.Tooltip('Recurso:N'),
                alt.Tooltip('Pct_Utilizacion:Q', format='.1f', title='% Utilización'),
                alt.Tooltip('Estado:N'),
                alt.Tooltip('Nivel:N')
            ]
        ).properties(
            height=max(220, len(df_uso) * 60),
            title=alt.Title(
                text='Mapa de Calor de Utilización de Recursos',
                subtitle='Rojo: Cuello de botella (>95%) | Dorado: Presión (>70%) | Verde: Óptimo',
                color='#FFFFFF',
                subtitleColor='#CCCCCC',
                fontSize=16,
                subtitleFontSize=12
            )
        )

        # Línea de referencia al 100%
        regla = alt.Chart(pd.DataFrame({'x': [100]})).mark_rule(
            color='#FF1744', strokeWidth=2, strokeDash=[4, 4]
        ).encode(x='x:Q')

        # Componer gráfico y luego aplicar configuración visual
        chart_compuesto = (barras_uso + regla).configure(
            background='rgba(26,26,26,0.8)',
        ).configure_axis(
            labelColor='#E0E0E0',
            labelFontSize=13,
            titleColor='#F9A825',
            titleFontSize=14,
            gridColor='rgba(255,255,255,0.06)',
        ).configure_title(
            color='#FFFFFF',
            fontSize=16
        )

        st.altair_chart(chart_compuesto, use_container_width=True)

        # --- INTERPRETACIÓN INTELIGENTE ---
        st.markdown("""
        <div class="glass-card" style="border-left: 3px solid #F9A825;">
            <h3 style="color: #F9A825; margin-top: 0;">💡 Interpretación Ejecutiva</h3>
        </div>
        """, unsafe_allow_html=True)

        # Generar interpretación dinámica
        activas = [res['nombres_restricciones'][j] for j in range(len(res['holguras'])) if res['holguras'][j] < 0.01]
        holgadas = [res['nombres_restricciones'][j] for j in range(len(res['holguras'])) if res['holguras'][j] >= 0.01]

        if activas:
            st.warning(f"⚠️ **Cuellos de Botella Identificados:** {', '.join(activas)}. "
                       f"Estos recursos se utilizan al 100%. Incrementar su capacidad mejoraría directamente el valor objetivo.")
        if holgadas:
            max_holgura_idx = np.argmax(res['holguras'])
            st.success(f"✅ **Recursos con Excedente:** {', '.join(holgadas)}. "
                       f"El recurso con mayor holgura es **{res['nombres_restricciones'][max_holgura_idx]}** "
                       f"({res['holguras'][max_holgura_idx]:,.2f} unidades sobrantes). "
                       f"Considere reasignar o reducir este recurso para ahorrar costos.")


# ============================================================
# TAB 4: EXPORTAR REPORTES
# ============================================================
with tab_exportar:
    if 'resultado_simplex' not in st.session_state or not st.session_state['resultado_simplex'].get('success'):
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 60px;">
            <p class="pulse-icon" style="font-size: 60px;">📥</p>
            <h2 style="color: #F5F5F5;">Sin Datos para Exportar</h2>
            <p style="color: #B0B0B0;">
                Ejecuta la optimización primero para habilitar la descarga de reportes.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        res = st.session_state['resultado_simplex']

        st.markdown("""
        <div class="glass-card animate-in">
            <h3 style="color: #F9A825; margin-top: 0;">📥 Centro de Exportación de Reportes</h3>
            <p style="color: #B0B0B0; font-size: 0.9rem;">
                Descarga reportes ejecutivos estilizados con los colores corporativos de EA Innovation & Solutions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Preparar datos del reporte
        contribuciones_exp = [res['variables'][i] * res['margenes'][i] for i in range(len(res['variables']))]
        datos_reporte = {
            'objetivo': res['tipo_objetivo'],
            'num_productos': len(res['nombres_productos']),
            'num_restricciones': len(res['nombres_restricciones']),
            'valor_objetivo': res['valor_objetivo'],
            'productos': [
                {
                    'nombre': res['nombres_productos'][i],
                    'cantidad': res['variables'][i],
                    'contribucion': contribuciones_exp[i]
                }
                for i in range(len(res['variables']))
            ],
            'recursos': [
                {
                    'nombre': res['nombres_restricciones'][j],
                    'disponible': res['limites'][j],
                    'consumido': res['consumo'][j],
                    'holgura': res['holguras'][j]
                }
                for j in range(len(res['limites']))
            ]
        }

        col_pdf, col_excel = st.columns(2)

        with col_pdf:
            st.markdown("""
            <div class="glass-card" style="text-align: center; border-top: 3px solid #C62828;">
                <p style="font-size: 48px; margin-bottom: 8px;">📄</p>
                <h3 style="color: #C62828; margin: 0;">Reporte PDF Ejecutivo</h3>
                <p style="color: #B0B0B0; font-size: 0.85rem; margin-top: 8px;">
                    Documento profesional con tablas, KPIs y análisis de sensibilidad.<br>
                    Estilizado con paleta corporativa EA.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if PDF_ENABLED:
                pdf_bytes = generar_pdf_reporte(datos_reporte)
                if pdf_bytes:
                    st.download_button(
                        label="📄 DESCARGAR PDF",
                        data=pdf_bytes,
                        file_name=f"EA_Simplex_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ Instala `fpdf2` para habilitar la exportación PDF.")

        with col_excel:
            st.markdown("""
            <div class="glass-card" style="text-align: center; border-top: 3px solid #F9A825;">
                <p style="font-size: 48px; margin-bottom: 8px;">📊</p>
                <h3 style="color: #F9A825; margin: 0;">Reporte Excel Analítico</h3>
                <p style="color: #B0B0B0; font-size: 0.85rem; margin-top: 8px;">
                    Hojas de cálculo con datos de producción y sensibilidad.<br>
                    Formatos, colores y fórmulas listas para análisis.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if EXCEL_ENABLED:
                excel_bytes = generar_excel_reporte(datos_reporte)
                if excel_bytes:
                    st.download_button(
                        label="📊 DESCARGAR EXCEL",
                        data=excel_bytes,
                        file_name=f"EA_Simplex_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ Instala `openpyxl` para habilitar la exportación Excel.")


# ============================================================
# FOOTER PREMIUM
# ============================================================
st.markdown(f"""
<div class="footer-premium">
    <p class="footer-slogan">
        "La exactitud es nuestra firma e innovar es nuestra naturaleza"
    </p>
    <p class="footer-credits">
        🏭 EA Simplex Production Optimizer v1.0 &nbsp;|&nbsp; 
        🐍 Desarrollado en Python por el Ing. Maestro Erik Armenta &nbsp;|&nbsp;
        ⚡ Motor: SciPy HiGHS &nbsp;|&nbsp;
        📍 EA Innovation & Solutions — Cd. Juárez, MX
    </p>
</div>
""", unsafe_allow_html=True)
