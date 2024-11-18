import pandas as pd
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path

# Firestore
cred = credentials.Certificate('./auth/firebase_credentials.json')

firebase_admin.initialize_app(cred)

db = firestore.client()

collection = db.collection('metals')
docs = collection.stream()

data = []
for doc in docs:
    data.append(doc.to_dict())
df = pd.DataFrame(data)

print(df)