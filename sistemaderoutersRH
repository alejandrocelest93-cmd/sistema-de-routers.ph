import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

st.set_page_config(page_title="Optimización MILP", layout="wide")

st.title("Optimización de Infraestructura de Routers")

st.markdown("""
Modelo de optimización entera para planificación de infraestructura tecnológica.
""")

# =========================================================
# VARIABLES
# =========================================================

variables = ["x1", "x2", "x3", "x4"]

# =========================================================
# FUNCIÓN OBJETIVO
# =========================================================

st.header("Función Objetivo")

st.write("Maximizar beneficio total:")

col1, col2, col3, col4 = st.columns(4)

c1 = col1.number_input("Coeficiente x1", value=20)
c2 = col2.number_input("Coeficiente x2", value=50)
c3 = col3.number_input("Coeficiente x3", value=90)
c4 = col4.number_input("Coeficiente x4", value=150)

# Negativos porque scipy minimiza
c = [-c1, -c2, -c3, -c4]

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

# MATRIZ INICIAL
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
# LIMITES INFERIORES Y SUPERIORES
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

if st.button("Resolver Modelo"):

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

            st.metric(
                "Valor Óptimo",
                round(-res.fun, 2)
            )

            resultado_df = pd.DataFrame({
                "Variable": variables,
                "Valor Óptimo": np.round(res.x, 2)
            })

            st.subheader("Variables Óptimas")

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
