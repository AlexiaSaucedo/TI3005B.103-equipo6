from google.oauth2 import service_account
from google.cloud import firestore
import json
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

st.title("Registro OSF")

# key_dict = json.loads(st.secrets["textkey"])
# creds = service_account.Credentials.from_service_account_info(key_dict)
# db = firestore.Client(credentials=creds, project="registro")
db = firestore.Client.from_service_account_json("registro.json")


# Función para obtener los Proyectos de cada Organización


def filtrarProyectosByOrg(codigo_org):
    proy_ref = list(db.collection(u'proyectos').stream())
    proy_dict = list(map(lambda x: x.to_dict(), proy_ref))
    data = pd.DataFrame(proy_dict)
    return data[data['Código_Organización'] == codigo_org]

# Función para obtener los Registros de cada Proyecto


def filtrarRegistroByProy(codigo_proy):
    reg_ref = list(db.collection(u'registro').stream())
    reg_dict = list(map(lambda x: x.to_dict(), reg_ref))
    data = pd.DataFrame(reg_dict)
    return data[data['CRN'] == int(codigo_proy)]


dbMatriculas = db.collection(u'registro')


def loadByName(matricula):
    names_ref = dbMatriculas.where(u'Matricula', u'==', matricula)
    currentName = None
    for myname in names_ref.stream():
        currentName = myname
    return currentName


grid_options = {
    "columnDefs": [
        {
            "field": 'Matricula',
            "checkboxSelection": True,
        },
    ],
    "rowSelection": 'multiple',
}

org_ref = list(db.collection(u'organizaciones').stream())
org_dict = list(map(lambda x: x.to_dict(), org_ref))
org_dataframe = pd.DataFrame(org_dict)

organizacion = st.selectbox(
    'Seleccionar Organizacion', org_dataframe['Organizacion_SF'].unique())
codigo_org = st.text_input('Código')
orgBtn = st.button('Buscar Proyectos')

if (orgBtn):
    filterbyorg = filtrarProyectosByOrg(codigo_org)
    count_row = filterbyorg.shape[0]
    st.write(f"Total de proyectos : {count_row}")
    st.write(
        filterbyorg.loc[:, ['CRN', 'Proyecto_nombre', 'Plazas_autorizadas']])
    st.selectbox('Seleccionar Proyecto',
                 filterbyorg['Proyecto_nombre'].unique())


codigo_proyecto = st.text_input('CRN:', 0)
proyectoBtn = st.button('Editar proyecto')

filterbyp = filtrarRegistroByProy(codigo_proyecto)

if (proyectoBtn):
    st.write(
        filterbyp.loc[:, ['Matricula', 'Estatus_de_inscripción ', 'Comentarios']])

st.sidebar.subheader('Buscar Alumno')
nameSearch = st.sidebar.text_input('Matricula')
btnFiltrar = st.sidebar.button('Buscar')

if btnFiltrar:
    doc = loadByName(nameSearch)
    if doc is None:
        st.sidebar.write('Estudiante no existe')
    else:
        st.sidebar.write(doc.to_dict())

st.sidebar.markdown("""---""")
btnEliminar = st.sidebar.button("Eliminar")

if btnEliminar:
    deletename = loadByName(nameSearch)
    if deletename is None:
        st.sidebar.write(f"{nameSearch} no se encuentra inscrito")
    else:
        dbMatriculas.document(deletename.id).delete()
        st.sidebar.write(f"{nameSearch} eliminado")

st.sidebar.markdown("""---""")

st.sidebar.selectbox('Estatus de inscripción', ['Inscrito', 'En espera'])

# grid_return = AgGrid(filterbyp, grid_options)
