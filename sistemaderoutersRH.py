import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Optimización de Infraestructura de Routers",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# ESTILO CSS - FONDO CELESTE (TRANSFORMADO A SYNTHWAVE)
# =========================================================

st.markdown("""
<style>
/* Fondo profundo de la app - Sin fondo blanco */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
}

/* Títulos con gradiente y neón */
h1 {
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #f355ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    font-size: 3rem !important;
    text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.4);
}

h2, h3, p, span, label {
    color: #e2e8f0 !important;
}

/* Tarjetas con efecto de cristal y neón */
div[data-testid="stVerticalBlock"] > div {
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid rgba(243, 85, 255, 0.3);
    padding: 25px;
}

/* Botón "Glow" Ultra-Llamativo */
div.stButton > button {
    background: linear-gradient(90deg, #f355ff 0%, #fd3f94 100%) !important;
    color: white !important;
    border-radius: 50px !important;
    border: none !important;
    height: 4em !important;
    width: 100%;
    font-size: 20px !important;
    font-weight: bold !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 0 25px rgba(243, 85, 255, 0.6);
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 45px rgba(253, 63, 148, 0.8);
}

/* Estilo para los dataframes */
[data-testid="stDataFrame"] {
    background-color: #1e293b;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("Optimización de Infraestructura de Routers")

st.markdown("""
Modelo de optimización entera para planificación de infraestructura tecnológica.
""")

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

if st.button("Resolver Modelo de Optimización"):

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
            # EFECTO DE GLOBOS AL ENCONTRAR SOLUCIÓN
            st.balloons()

            st.success("Solución óptima encontrada")

            # Métrica estilizada
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #00f2fe 0%, #9b51e0 100%); 
                        padding: 30px; border-radius: 15px; text-align: center;
                        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4); margin-bottom: 25px;'>
                <p style='margin:0; font-size: 16px; font-weight: bold; color: white !important;'>BENEFICIO MÁXIMO</p>
                <h1 style='margin:10px 0; color: white !important; font-size: 55px !important;'>{round(-res.fun, 2):,}</h1>
                <p style='margin:0; font-size: 14px; color: rgba(255,255,255,0.8) !important;'>Usuarios totales soportados</p>
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
            st.error("No se encontró solución factible.")

    except Exception as e:
        st.error(f"Error en el modelo: {e}")
