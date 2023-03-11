import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

st.title("Registro OSF")

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db =firestore.Client.from_service_account_json("registro.json")
#db = firestore.Client(credentials=creds, project="registro")

dbOrganizaciones = db.collection(u'organizaciones')

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     def lowercase(x): return str(x).lower()
#     return data

def filtrar_org(organizacion):
    filtered_data = data[data['Organizacion_SF'] == organizacion]
    return filtered_data

def filtrar_proyecto(proyecto):
    filtered_data = data[data['name'].str.upper().str.contains(proyecto)]
    return filtered_data



#organizacion = st.selectbox('Seleccionar Organizacion', 'y','n')
# st.text_input('Código')
# orgBtn = st.button('Buscar Proyectos')

# if (orgBtn):
#     filterbyorg = filtrar_org(organizacion)
#     count_row = filterbyorg.shape[0]
#     st.write(f"Total de proyectos : {count_row}")
#     st.write(filterbyorg)


names_ref = list(db.collection(u'organizaciones').stream())
names_dict = list(map(lambda x: x.to_dict(), names_ref))
names_dataframe = pd.DataFrame(names_dict)
st.dataframe(names_dataframe)

organizacion = st.selectbox('Seleccionar Organizacion', names_dataframe)

# st.dataframe(data)

