import pyrebase
import streamlit as st

@st.experimental_singleton
def get_DB_Config():

    config ={
      "apiKey": "AIzaSyBgPQ03XDq3_ru7H-PgR_DdnnOpbeiGwTs",
      "authDomain": "kepia-rdb.firebaseapp.com",
      "projectId": "kepia-rdb",
      "databaseURL" : 'https://kepia-rdb-default-rtdb.firebaseio.com/',
      "serviceAccount" : 'src/utils/kepia-rdb-firebase-adminsdk-ffg2b-b67b5ea05c.json',
      "storageBucket": "kepia-rdb.appspot.com",
      "messagingSenderId": "368273954603",
      "appId": "1:368273954603:web:b0a04add2e56f79fd6576e",
      "measurementId": "G-6T9K2T2GRB"
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    dataBase = firebase.database()

    return dataBase
