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
# ESTILO CSS - INTERFAZ PREMIUM OSCURA CON NEÓN
# =========================================================

st.markdown("""
<style>
/* Fondo principal en gradiente oscuro futurista */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
}

/* Títulos principales con efecto gradiente de texto brillante */
h1 {
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #f355ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    font-size: 2.8rem !important;
}

h2, h3, p, span, label {
    color: #e2e8f0 !important;
}

/* Tarjetas contenedoras translúcidas con bordes de neón sutil */
div[data-testid="stVerticalBlock"] > div {
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(0, 242, 254, 0.2);
}

/* Botón de acción principal ultra llamativo y dinámico */
div.stButton > button {
    background: linear-gradient(90deg, #f355ff 0%, #fd3f94 100%) !important;
    color: white !important;
    border-radius: 50px !important;
    border: none !important;
    height: 3.5em !important;
    width: 100%;
    font-size: 18px !important;
    font-weight: bold !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    box-shadow: 0 0 20px rgba(243, 85, 255, 0.4);
    transition: all 0.3s ease-in-out;
}

div.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 35px rgba(253, 63, 148, 0.7);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("⚡ Optimización de Infraestructura de Routers")

st.markdown("""
<p style='font-size: 1.15rem; color: #94a3b8 !important;'>
Modelo de optimización entera para planificación de infraestructura tecnológica.
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

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Resolver Modelo de Optimización"):

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

        st.header("✨ Resultado de Optimización")

        st.write("Estado:", res.message)

        if res.success:

            st.success("Solución óptima encontrada exitosamente.")

            # Widget personalizado y de alto impacto visual para el KPI principal
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); 
                        padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 25px;
                        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.3);'>
                <p style='margin:0; font-size: 14px; font-weight: bold; color: #0f172a !important; letter-spacing: 1.5px;'>BENEFICIO MÁXIMO</p>
                <h1 style='margin:5px 0; color: #0f172a !important; -webkit-text-fill-color: #0f172a !important; font-size: 45px !important; font-weight: 800;'>{round(-res.fun, 2):,}</h1>
                <p style='margin:0; font-size: 13px; color: #1e293b !important; opacity: 0.8;'>Rendimiento total optimizado</p>
            </div>
            """, unsafe_allow_html=True)

            resultado_df = pd.DataFrame({
                "Tipo de Router": variables,
                "Cantidad Óptima": np.round(res.x, 2)
            })

            st.subheader("📦 Cantidad Óptima de Routers")

            st.dataframe(
                resultado_df,
                use_container_width=True
            )

            st.subheader("🔮 Vector Solución")

            st.write(res.x)

        else:
            st.error("No se encontró solución factible.")

    except Exception as e:
        st.error(f"Error en el modelo: {e}")
