# EA Simplex Production Optimizer — Guía de desarrollo

**Cliente:** Ing. Maestro Erik Armenta — EA Innovation & Solutions, Cd. Juárez MX
**Repo:** https://github.com/ErikArmenta/Optimizador_EA
**Stack:** Python 3.12 · Streamlit · SciPy MILP/HiGHS · Plotly · Altair · fpdf2 · openpyxl

---

## Comandos

```bash
# Instalar dependencias
pip install streamlit scipy pandas numpy plotly altair openpyxl fpdf2 Pillow

# Correr local
streamlit run appSimplex.py --server.port 8501
# → http://localhost:8501

# Si el puerto está ocupado
netstat -ano | findstr 8501       # obtener PID
taskkill //F //PID <pid>          # matar proceso
```

## Estructura

```
appSimplex.py          # app principal (único archivo)
EA_2.png               # logo corporativo
requirements.txt       # dependencias
```

## Funciones clave

| Función | Descripción |
|---|---|
| `resolver_problema()` | Solver MILP/LP con `@st.cache_data`, args como tuplas |
| `validar_inputs()` | Validación antes de optimizar |
| `generar_plantilla_excel()` | Plantilla descargable de 2 hojas |
| `leer_excel_importado()` | Parser del Excel importado |
| `generar_pdf_reporte()` | PDF ejecutivo con fpdf2 |
| `generar_excel_reporte()` | Excel con múltiples hojas |

## Diseño — reglas a mantener

- **Colores EA:** Rojo `#C62828` · Dorado `#F9A825` · Negro `#0D0D0D`
- Mantener efecto **ripple JS** en botones (bloque `<script>` después del CSS)
- Mantener comentarios de sección CSS (`/* ===== ... ===== */`)
- No condensar propiedades CSS en una sola línea
- Badge `v2-badge` en header para versión actual

## Reglas de commits

- Un solo commit por feature/fix
- Mensaje en español técnico, sin `Co-Authored-By`
- Formato: `feat:` / `fix:` / `refactor:` + descripción corta
- Verificar `git status` limpio antes de push

## Features v2.0 (implementados)

- [x] MILP — variables enteras por producto
- [x] Restricciones mixtas ≤ / ≥ / =
- [x] Importación Excel/CSV con plantilla
- [x] Precios sombra vía relajación LP
- [x] Comparador de escenarios (hasta 5)
- [x] Análisis What-If con sliders
- [x] Persistencia JSON
- [x] Validación de inputs
- [x] Manejo de infactibles / no acotados

## Próximas mejoras (v3.0)

- [ ] Docker / Railway (salir de Streamlit Cloud free tier)
- [ ] Log de auditoría por corrida
- [ ] RHS Ranging (rangos de factibilidad)
- [ ] Multi-objetivo (goal programming)
