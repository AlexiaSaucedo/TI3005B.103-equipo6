import streamlit as st
import pandas as pd

st.title("Registro OSF")

DATA_URL = ('organizaciones.csv')


@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    def lowercase(x): return str(x).lower()
    return data


def filtrar_org(organizacion):
    filtered_data = data[data['Organizacion_SF'] == organizacion]
    return filtered_data


def filtrar_proyecto(proyecto):
    filtered_data = data[data['name'].str.upper().str.contains(proyecto)]
    return filtered_data


data_load_state = st.text('Loading data...')
data = load_data(500)
data_load_state.text("Done! (using st.cache)")

organizacion = st.selectbox(
    'Seleccionar Organizacion', data['Organizacion_SF'].unique())
st.text_input('Código')
orgBtn = st.button('Buscar Proyectos')

if (orgBtn):
    filterbyorg = filtrar_org(organizacion)
    count_row = filterbyorg.shape[0]
    st.write(f"Total de proyectos : {count_row}")
    st.write(filterbyorg)


st.dataframe(data)
