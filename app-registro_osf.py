import json
import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

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


# organizacion = st.selectbox('Seleccionar Organizacion', 'y','n')
# st.text_input('Código')
# orgBtn = st.button('Buscar Proyectos')

# if (orgBtn):
#     filterbyorg = filtrar_org(organizacion)
#     count_row = filterbyorg.shape[0]
#     st.write(f"Total de proyectos : {count_row}")
#     st.write(filterbyorg)

org_ref = list(db.collection(u'organizaciones').stream())
org_dict = list(map(lambda x: x.to_dict(), org_ref))
org_dataframe = pd.DataFrame(org_dict)
# st.dataframe(names_dataframe)

organizacion = st.selectbox(
    'Seleccionar Organizacion', org_dataframe['Organizacion_SF'].unique())
codigo_org = st.text_input('Código')
orgBtn = st.button('Buscar Proyectos')

if (orgBtn):
    filterbyorg = filtrarProyectosByOrg(codigo_org)
    st.write(filterbyorg.loc[:, ['Proyecto_nombre', 'Plazas_autorizadas']])
#     count_row = filterbyorg.shape[0]
#     st.write(f"Total de proyectos : {count_row}")
