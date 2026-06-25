import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Optimización de Infraestructura de Routers",
    layout="wide"
)

# =========================================================
# ESTILO CSS - FRUTIGER AERO (WINDOWS VISTA / 7 GLOW)
# =========================================================

st.markdown("""
<style>
/* Fondo: El clásico degradado brillante de cielo azul limpio y naturaleza verde */
.stApp {
    background: linear-gradient(180deg, #50b5ff 0%, #a3e5ff 40%, #eefcff 65%, #60d643 100%);
    background-attachment: fixed;
}

/* Títulos principales con sombra suave y estilo tipográfico de la época */
h1 {
    color: #0c3c60 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 600 !important;
    font-size: 2.8rem !important;
    text-shadow: 1px 2px 4px rgba(255, 255, 255, 0.8);
}

h2, h3 {
    color: #0b4c10 !important;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 500 !important;
    text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.9);
}

p, span, label {
    color: #1a3a54 !important;
    font-weight: 600 !important;
}

/* Efecto Windows Aero Glass: Transparencia vítrea, bordes brillantes y reflejos de luz */
div[data-testid="stVerticalBlock"] > div {
    background: rgba(255, 255, 255, 0.45) !important;
    backdrop-filter: blur(15px) saturate(140%) !important;
    -webkit-backdrop-filter: blur(15px) saturate(140%) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.6) !important;
    box-shadow: 0 8px 32px 0 rgba(31, 135, 195, 0.25),
                inset 0 1px 0 rgba(255,255,255,0.6) !important;
    padding: 20px;
}

/* Modificación de data editors para que mantengan la transparencia Aqua */
div[data-testid="stDataEditor"] {
    background-color: rgba(240, 252, 255, 0.7) !important;
    border-radius: 8px;
}

/* Botón estilo Windows 7 / Aqua: Esfera vítrea brillante y bordes redondeados */
div.stButton > button {
    background: linear-gradient(180deg, #87e0fd 0%, #53cbf1 40%, #05abe0 100%) !important;
    color: white !important;
    text-shadow: 0px -1px 2px rgba(0, 0, 0, 0.4) !important;
    border-radius: 20px !important; 
    border: 1px solid #057ca5 !important;
    height: 3.5em !important;
    width: 100%;
    font-size: 16px !important;
    font-weight: bold !important;
    box-shadow: 0px 4px 10px rgba(5, 171, 224, 0.4), 
                inset 0px 1px 3px rgba(255,255,255,0.8);
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background: linear-gradient(180deg, #b3efff 0%, #76dbff 40%, #22c4f7 100%) !important;
    box-shadow: 0px 6px 15px rgba(5, 171, 224, 0.6), 
                inset 0px 1px 5px rgba(255,255,255,0.9);
    color: white !important;
    transform: translateY(-1px);
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

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
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

with col_der:
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
    "Límite Inferior": [1, 1, 1, 1, 1, 150000, 1],
    "Límite Superior": [500, 300, 40, 120, 80, np.inf]
}, index=restricciones)

limites_editados = st.data_editor(
    limites_df,
    use_container_width=True,
    num_rows="fixed"
)

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
            
            # Efecto mítico de globos intacto
            st.balloons()

            st.success("Solución óptima encontrada")

            panel_res1, panel_res2 = st.columns([1, 1.2])

            with panel_res1:
                # Banner con diseño de burbuja brillante Aqua tipo Windows Vista
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #a3e5ff 0%, #3ebbef 50%, #0599cb 100%); 
                            padding: 30px; border: 1px solid rgba(255,255,255,0.7); border-radius: 14px; text-align: center;
                            box-shadow: 0px 8px 20px rgba(5, 153, 203, 0.3), inset 0px 1px 6px rgba(255,255,255,0.8);'>
                    <p style='margin:0; font-size: 14px; font-weight: bold; color: #0c3c60 !important; letter-spacing: 1px;'>BENEFICIO MÁXIMO</p>
                    <h1 style='margin:15px 0; color: white !important; -webkit-text-fill-color: white !important; font-size: 50px !important; font-family: sans-serif; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>{round(-res.fun, 2):,}</h1>
                    <p style='margin:0; font-size: 13px; color: #e6f7ff !important; font-weight: bold;'>Usuarios totales soportados</p>
                </div>
                """, unsafe_allow_html=True)

            with panel_res2:
                resultado_df = pd.DataFrame({
                    "Tipo de Router": variables,
                    "Cantidad Óptima": np.round(res.x, 2)
                })

                st.subheader("Cantidad Óptima de Routers")
                st.dataframe(resultado_df, use_container_width=True)

                st.subheader("Vector Solución")
                st.write(res.x)

        else:
            st.error("No se encontró solución factible.")

    except Exception as e:
        st.error(f"Error en el modelo: {e}")
