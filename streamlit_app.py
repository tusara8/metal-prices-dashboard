import streamlit as st
import pandas as pd
import math
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

st.set_page_config(
    page_title='Metal prices dashboard',
    page_icon='https://static.thenounproject.com/png/4977682-200.png',
)

# Firestore
cred = credentials.Certificate('./auth/test_data.json')

firebase_admin.initialize_app(cred)

db = firestore.client()

collection = db.collection('metals')
docs = collection.stream()

data = []
for doc in docs:
    data.append(doc.to_dict())
df = pd.DataFrame(data)

df['Date'] = pd.to_datetime(df['Date'])

# Відображення DataFrame в Streamlit
st.dataframe(df)

'''
# Metal Prices Dashboard
'''

''
''

min_value = df['Date'].min()
max_value = df['Date'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

metals = df.columns[~df.columns.isin(['Date'])]

if not len(metals):
    st.warning("Select at least one country")

selected_metals = st.multiselect(
    'Which metals would you like to view?',
    metals,
    ['Platinum'])

''
''
''

# Filter the data
filtered_metal_prices_df = df[
    (metals.isin(selected_metals))
    & (df['Date'] <= to_year)
    & (from_year <= df['Date'])
]

st.header('metal_prices over time', divider='gray')

''

st.line_chart(
    filtered_metal_prices_df,
    x='Date',
    y='Price'
)

''
''


first_year = df[df['Date'] == from_year]
last_year = df[df['Date'] == to_year]