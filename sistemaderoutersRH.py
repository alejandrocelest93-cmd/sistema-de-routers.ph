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
# ESTILO CSS - FONDO CELESTE (Adaptado a Vaporwave sin fondo blanco)
# =========================================================

st.markdown("""
<style>
/* Fondo profundo de la app en azul medianoche/morado */
.stApp {
    background-color: #1a103c;
}

/* Títulos con gradiente de color Retro-Fucsia a Amarillo Eléctrico */
h1 {
    background: linear-gradient(90deg, #ff007f 0%, #ff00ff 50%, #ffea00 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Impact', 'Arial Black', sans-serif;
    font-weight: bold !important;
    font-size: 3rem !important;
    letter-spacing: 1px;
}

h2 {
    color: #ff00ff !important;
    font-size: 1.6rem !important;
    font-weight: bold !important;
    border-bottom: 2px dashed #ffea00;
    padding-bottom: 5px;
}

h3, p, span, label {
    color: #00ffff !important;
    font-weight: 500;
}

/* Contenedores con fondo morado medio y bordes cian neón */
div[data-testid="stVerticalBlock"] > div {
    background-color: #24144b;
    border-radius: 16px;
    border: 2px solid #00ffff;
    box-shadow: 0px 0px 15px rgba(0, 255, 255, 0.2);
    padding: 20px;
}

/* Modificación de data editors y selects para que no usen fondo blanco */
div[data-testid="stDataEditor"] {
    background-color: #1a103c !important;
}

/* Botón de acción ultra-llamativo en gradiente degradado */
div.stButton > button {
    background: linear-gradient(45deg, #ff007f 0%, #7000ff 100%) !important;
    color: #ffea00 !important;
    border-radius: 0px !important; /* Estilo retro rectangular */
    border: 3px solid #ffea00 !important;
    height: 3.5em !important;
    width: 100%;
    font-size: 18px !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 5px 5px 0px #00ffff;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translate(-2px, -2px);
    box-shadow: 7px 7px 0px #00ffff;
    color: #ffffff !important;
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

# Distribución horizontal compacta del diseño que te gustó
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
    "Límite Inferior": [1, 1, 1, 1, 1, 1, 1],
    "Límite Superior": [500, 300, 40, 120, 80, 750000, np.inf]
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

            st.success("Solución óptima encontrada")

            panel_res1, panel_res2 = st.columns([1, 1.2])

            with panel_res1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #ff007f 0%, #7000ff 100%); 
                            padding: 30px; border: 3px solid #00ffff; text-align: center;
                            box-shadow: 8px 8px 0px #ffea00;'>
                    <p style='margin:0; font-size: 14px; font-weight: bold; color: #ffea00 !important; letter-spacing: 2px;'>BENEFICIO MÁXIMO</p>
                    <h1 style='margin:15px 0; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-size: 50px !important; font-family: Impact;'>{round(-res.fun, 2):,}</h1>
                    <p style='margin:0; font-size: 13px; color: #00ffff !important;'>Usuarios totales soportados</p>
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
