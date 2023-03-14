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

dbOrganizaciones = db.collection(u'organizaciones')


def filtrarProyectosByOrg(codigo_org):
    # filtered_data = data[data['Organizacion_SF'] == organizacion]
    proy_ref = list(db.collection(u'proyectos').stream())
    proy_dict = list(map(lambda x: x.to_dict(), proy_ref))
    data = pd.DataFrame(proy_dict)
    return data[data['Código_Organización'] == codigo_org]
    # return data[data['Codigo_Organizacion'] == codigo_org]


def filtrarRegistroByProy(codigo_proy):
    # filtered_data = data[data['Organizacion_SF'] == organizacion]
    reg_ref = list(db.collection(u'registro').stream())
    reg_dict = list(map(lambda x: x.to_dict(), reg_ref))
    data = pd.DataFrame(reg_dict)
    return data[data['CRN'] == int(codigo_proy)]
    # return data[data['Codigo_Organizacion'] == codigo_org]


org_ref = list(db.collection(u'organizaciones').stream())
org_dict = list(map(lambda x: x.to_dict(), org_ref))
org_dataframe = pd.DataFrame(org_dict)
# st.dataframe(org_dataframe)
# AgGrid(org_dataframe)


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
    # AgGrid(filterbyorg)

codigo_proyecto = st.text_input('CRN:')
proyectoBtn = st.button('Editar proyecto')

if (proyectoBtn):
    filterbyp = filtrarRegistroByProy(codigo_proyecto)
    # st.subheader( f" Resultado : {filterbyorg[filterbyorg['CRN'] == int_codigo]}")
    st.write(
        filterbyp.loc[:, ['Matricula', 'Estatus_de_inscripción ', 'Comentarios']])
