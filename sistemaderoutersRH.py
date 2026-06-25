import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILO HARDCORE
# =========================================================

st.set_page_config(
    page_title="RouterOptima | CYBER_EDITION",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# ESTILO CSS - INTERFAZ NEÓN CYBERPUNK
# =========================================================

st.markdown("""
<style>
/* Fondo Galáctico / Futurista Animado */
@keyframes gradientBg {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e1b4b, #311042, #000c1e);
    background-size: 400% 400%;
    animation: gradientBg 15s ease infinite;
}

/* Título Principal con Efecto Glitch y Neón */
@keyframes neonPulse {
    from { text-shadow: 0 0 10px rgba(0, 242, 254, 0.7); }
    to { text-shadow: 0 0 25px rgba(0, 242, 254, 1); }
}

h1 {
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 900 !important;
    font-size: 3.2rem !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    animation: neonPulse 1.5s ease-in-out infinite alternate;
}

h2, h3, p, span, label {
    color: #e2e8f0 !important;
}

/* Tarjetas de Contenido Translúcidas (Glassmorphism) */
div[data-testid="stVerticalBlock"] > div {
    background: rgba(15, 23, 42, 0.5) !important;
    backdrop-filter: blur(8px);
    border-radius: 20px;
    border: 1px solid rgba(243, 85, 255, 0.2);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

/* Botón de Acción Principal ULTRA LLAMATIVO */
@keyframes pulse {
    0% { box-shadow: 0 0 15px rgba(243, 85, 255, 0.4); }
    50% { box-shadow: 0 0 35px rgba(243, 85, 255, 0.8); }
    100% { box-shadow: 0 0 15px rgba(243, 85, 255, 0.4); }
}

div.stButton > button {
    background: linear-gradient(90deg, #f355ff 0%, #fd3f94 50%, #ff7640 100%) !important;
    color: white !important;
    border-radius: 50px !important;
    border: none !important;
    height: 3.8em !important;
    width: 100%;
    font-size: 20px !important;
    font-weight: bold !important;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    box-shadow: 0 0 20px rgba(243, 85, 255, 0.5);
    transition: all 0.4s ease-in-out;
}

div.stButton > button:hover {
    transform: scale(1.04);
    box-shadow: 0 0 45px rgba(253, 63, 148, 0.9);
    animation: pulse 1s infinite;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("⚡ ROUTER_OPTIMA: CYBERNETIC DEPLOY")

st.markdown("""
<p style='font-size: 1.2rem; color: #94a3b8 !important; text-align: center; margin-bottom: 20px;'>
Modelo de optimización entera hardcore para planificación de infraestructura tecnológica.
</p>
""", unsafe_allow_html=True)

# =========================================================
# VARIABLES
# =========================================================

variables = [
    "Routers tipo1",
    "Routers tipo2",
    "Routers tipo3",
    "Routers tipo4"
]

# =========================================================
# FUNCIÓN OBJETIVO
# =========================================================

st.header("🎯 Maximizar Beneficio Total")

st.write("""
Ingrese la cantidad de usuarios asociada a cada tipo de router.
""")

col1, col2, col3, col4 = st.columns(4)

u1 = col1.number_input(
    "Cantidad de usuarios - Router tipo1",
    value=20
)

u2 = col2.number_input(
    "Cantidad de usuarios - Router tipo2",
    value=50
)

u3 = col3.number_input(
    "Cantidad de usuarios - Router tipo3",
    value=90
)

u4 = col4.number_input(
    "Cantidad de usuarios - Router tipo4",
    value=150
)

# Negativos porque scipy minimiza
c = [-u1, -u2, -u3, -u4]

# =========================================================
# RESTRICCIONES
# =========================================================

st.header("🛡️ Restricciones del Sistema")

restricciones = [
    "Energía",
    "Ancho de Banda",
    "Disponibilidad de Equipos",
    "Disipación Térmica",
    "Personal de Mantenimiento",
    "Cobertura de Routers",
    "Dependencia Mínima"
]

# =========================================================
# MATRIZ DE RESTRICCIONES
# =========================================================

st.subheader("📊 Coeficientes de Restricciones")

A_inicial = pd.DataFrame(
    [
        [6, 12, 25, 40],
        [5, 10, 20, 45],
        [1, 2, 3, 5],
        [2, 4, 15, 20],
        [3, 5, 8, 12],
        [400, 1200, 3000, 7000],
        [1, 0, 0, -2]
    ],
    columns=variables,
    index=restricciones
)

A_df = st.data_editor(
    A_inicial,
    use_container_width=True,
    num_rows="fixed"
)

# =========================================================
# LIMITES
# =========================================================

st.subheader("⚙️ Límites de Restricciones")

limites_df = pd.DataFrame({
    "Límite Inferior": [1, 1, 1, 1, 1, 1, 1],
    "Límite Superior": [500, 300, 40, 120, 80, 750000, np.inf]
}, index=restricciones)

limites_editados = st.data_editor(
    limites_df,
    use_container_width=True,
    num_rows="fixed"
)

# =========================================================
# VARIABLES ENTERAS
# =========================================================

st.subheader("🧬 Tipo de Variables")

st.write("""
0 = Continua  
1 = Entera
""")

integrality = []

cols = st.columns(4)

for i, var in enumerate(variables):

    val = cols[i].selectbox(
        f"{var}",
        options=[0, 1],
        index=1
    )

    integrality.append(val)

# =========================================================
# RESOLVER
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

if st.button("🔥 EJECUTAR PROTOCOLO DE OPTIMIZACIÓN 🔥"):

    try:

        A = A_df.values

        bl = limites_editados["Límite Inferior"].values
        bu = limites_editados["Límite Superior"].values

        constraints = LinearConstraint(A, bl, bu)

        bounds = Bounds(
            [0] * len(variables),
            [np.inf] * len(variables)
        )

        res = milp(
            c=c,
            constraints=constraints,
            bounds=bounds,
            integrality=integrality
        )

        st.header("✨ Resultado del Motor de Cálculo")

        st.write("Estado del Solver:", res.message)

        if res.success:

            st.success("Solución óptima encontrada exitosamente.")

            # MEGA-TARJETA DE RESULTADO TURQUESA NEÓN ULTRA BRILANTE
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #00f2fe 0%, #00d2f0 100%); 
                        padding: 35px; border-radius: 20px; text-align: center; margin-bottom: 30px;
                        box-shadow: 0 10px 40px rgba(0, 242, 254, 0.5);'>
                <p style='margin:0; font-size: 16px; font-weight: bold; color: #0f172a !important; letter-spacing: 2px;'>BENEFICIO MÁXIMO GLOBAL</p>
                <h1 style='margin:10px 0; color: white !important; -webkit-text-fill-color: white !important; font-size: 58px !important; font-weight: 900; text-shadow: 0px 0px 20px rgba(255,255,255,0.8);'>{round(-res.fun, 2):,}</h1>
                <p style='margin:0; font-size: 14px; color: #1e293b !important; opacity: 0.8;'>Usuarios totales soportados de forma eficiente</p>
            </div>
            """, unsafe_allow_html=True)

            resultado_df = pd.DataFrame({
                "Tipo de Router": variables,
                "Cantidad Óptima": np.round(res.x, 2)
            })

            st.subheader("📦 Plan de Equipamiento Recomendado")

            st.dataframe(
                resultado_df,
                use_container_width=True
            )

            st.subheader("🔮 Vector de Solución Crudo")

            st.write(res.x)

        else:
            st.error("No se encontró solución factible.")

    except Exception as e:
        st.error(f"Error en el motor matemático: {e}")
