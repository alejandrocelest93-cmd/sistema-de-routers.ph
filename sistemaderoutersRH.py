# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Electronic Engineering Optimization System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ESTILO CSS - INGENIERÍA ELECTRÓNICA
# =========================================================

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #08111f 0%, #111827 100%);
    color: #e5e7eb;
}

/* Títulos */
h1 {
    color: #00e5ff;
    text-align: center;
    font-size: 3rem;
    border-bottom: 3px solid #00e5ff;
    padding-bottom: 10px;
    text-shadow: 0px 0px 20px #00e5ff;
}

h2, h3 {
    color: #4ade80;
}

/* Texto */
p, label, div {
    color: #d1d5db;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0b1220;
}

/* Inputs */
.stNumberInput input {
    background-color: #1e293b;
    color: white;
    border: 1px solid #00e5ff;
    border-radius: 8px;
}

/* Select */
div[data-baseweb="select"] {
    background-color: #1e293b;
    border-radius: 8px;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #00e5ff;
    border-radius: 10px;
}

/* Botón */
div.stButton > button {
    background: linear-gradient(90deg, #00e5ff, #0066ff);
    color: white;
    border: none;
    border-radius: 15px;
    height: 3.5em;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    box-shadow: 0px 0px 20px #00e5ff;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 35px #00e5ff;
}

/* Métricas */
[data-testid="metric-container"] {
    background-color: #111827;
    border: 2px solid #4ade80;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(74,222,128,0.4);
}

/* Alertas */
.stSuccess {
    border-left: 5px solid #4ade80;
}

.stError {
    border-left: 5px solid red;
}

/* Tarjetas */
.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #00e5ff;
    box-shadow: 0px 0px 15px rgba(0,229,255,0.2);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# ENCABEZADO PRINCIPAL
# =========================================================

st.markdown("""
<h1>⚡ Electronic Engineering Optimization System ⚡</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h3>📡 Optimización Inteligente de Infraestructura de Routers</h3>

Sistema basado en Programación Lineal Entera Mixta (MILP)
para el diseño y optimización de redes de telecomunicaciones.

✔ Maximización de cobertura.

✔ Optimización energética.

✔ Restricciones térmicas.

✔ Planificación de infraestructura.

✔ Ingeniería electrónica aplicada.
</div>
""", unsafe_allow_html=True)

st.write("")

col1, col2, col3 = st.columns(3)

col1.metric("Modelo", "MILP")
col2.metric("Área", "Telecom")
col3.metric("Variables", "4")

st.divider()
