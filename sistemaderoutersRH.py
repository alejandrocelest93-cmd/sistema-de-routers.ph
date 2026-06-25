# =========================================================
# ESTILO DASHBOARD TECNOLÓGICO
# =========================================================

st.markdown("""
<style>

/* Fondo principal */
.stApp {
    background: linear-gradient(135deg,#0a192f,#112240);
    color: white;
}

/* Títulos */
h1 {
    color: #64ffda;
    text-align: center;
    font-size: 42px;
    text-shadow: 0px 0px 15px #64ffda;
}

h2, h3 {
    color: #4fc3f7;
}

/* Paneles */
[data-testid="stDataFrame"] {
    background-color: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 10px;
}

/* Inputs */
div[data-baseweb="input"] {
    background-color: #1b2a41;
    border-radius: 10px;
}

/* Botón principal */
div.stButton > button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    border: none;
    border-radius: 15px;
    height: 3.5em;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    box-shadow: 0px 0px 15px #00c6ff;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 25px #00c6ff;
}

/* Métricas */
[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.08);
    border: 2px solid #64ffda;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 0px 15px rgba(100,255,218,0.3);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #08111f;
}

/* Tablas */
thead tr th {
    background-color: #00bcd4 !important;
    color: black !important;
}

tbody tr:nth-child(even) {
    background-color: rgba(255,255,255,0.05);
}

</style>
""", unsafe_allow_html=True)
