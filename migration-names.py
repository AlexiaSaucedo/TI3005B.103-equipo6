import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

path = "./" 

cred = credentials.Certificate(path +"registro.json") 
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'estudiantes') # Set the name of the Collection
# Import data
df = pd.read_csv(path+'Base de datos aplicación - Estudiantes.csv')
tmp = df.to_dict(orient='records')

for x in tmp:
    doc_ref = db.collection("estudiantes").document(x['Matricula'])
    doc_ref.set(x)
    print(x)
    print('inserted')

#list(map(lambda x: doc_ref.add(x), tmp))