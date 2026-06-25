import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Optimización de Infraestructura de Routers",
    page_icon="💎",
    layout="wide"
)

# =========================================================
# ESTILO CSS - ESTÉTICA PREMIUM "GLASSMORPHISM" DE BUEN GUSTO
# =========================================================

st.markdown("""
<style>
/* Fondo general: Oscuro profundo, elegante y cinemático */
.stApp {
    background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #090d16 70%);
}

/* Tipografías y Encabezados sofisticados */
h1 {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    font-size: 3rem !important;
    letter-spacing: -1px;
}

h2 {
    font-family: 'Inter', sans-serif;
    color: #f8fafc !important;
    font-weight: 600 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 8px;
    margin-top: 2rem !important;
}

h3, p, span, label {
    font-family: 'Inter', sans-serif;
    color: #94a3b8 !important;
}

/* Tarjetas de Cristal (Glassmorphism) para agrupar secciones */
div[data-testid="stVerticalBlock"] > div {
    background: rgba(15, 23, 42, 0.45);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 20px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* Inputs numéricos y selects estilizados en armonía oscura */
div[data-baseweb="input"], div[data-baseweb="select"] {
    background-color: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
}

/* Dataframes / Tablas integradas estéticamente */
div[data-testid="stDataFrame"] {
    background-color: transparent !important;
}

/* Botón de Ejecución: Lujoso, con un degradado sutil y premium */
div.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 14px !important;
    height: 3.5em !important;
    width: 100%;
    font-size: 16px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.3);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(79, 70, 229, 0.5);
    background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("Optimización de Infraestructura de Routers")

st.markdown("""
<p style='font-size: 1.1rem; color: #64748b !important; margin-top: -10px;'>
Plataforma analítica basada en optimización entera mixta para decisiones tecnológicas estratégicas.
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

st.header("Maximizar Beneficio Total")

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

st.header("Restricciones del Sistema")

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

st.subheader("Coeficientes de Restricciones")

A_df = st.data_editor(
    A_inicial,
    use_container_width=True,
    num_rows="fixed"
)

# =========================================================
# LIMITES
# =========================================================

st.subheader("Límites de Restricciones")

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

st.subheader("Tipo de Variables")

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

if st.button("Calcular Distribución Óptima"):

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

        st.header("Resultado de Optimización")

        st.write("Estado:", res.message)

        if res.success:

            st.success("Cálculo finalizado. Se ha hallado una solución matemáticamente óptima.")

            # Tarjeta de KPI Minimalista y elegante (estilo Apple)
            st.markdown(f"""
            <div style='background: linear-gradient(180deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%); 
                        border: 1px solid rgba(255,255,255,0.15); padding: 30px; border-radius: 20px; 
                        text-align: center; margin-bottom: 30px; margin-top: 15px;'>
                <p style='margin:0; font-size: 13px; font-weight: 600; color: #a5b4fc !important; letter-spacing: 1px; text-transform: uppercase;'>Beneficio Máximo Obtenido</p>
                <h1 style='margin:10px 0; font-size: 50px !important; font-weight: 800; background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{round(-res.fun, 2):,}</h1>
                <p style='margin:0; font-size: 13px; color: #64748b !important;'>Usuarios totales soportados de forma eficiente</p>
            </div>
            """, unsafe_allow_html=True)

            resultado_df = pd.DataFrame({
                "Tipo de Router": variables,
                "Cantidad Óptima": np.round(res.x, 2)
            })

            st.subheader("Cantidad Óptima de Routers")

            st.dataframe(
                resultado_df,
                use_container_width=True
            )

            st.subheader("Vector Solución")

            st.write(res.x)

        else:
            st.error("No se encontró solución factible bajo las condiciones actuales.")

    except Exception as e:
        st.error(f"Error en el modelo: {e}")
