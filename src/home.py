import streamlit as st
from utils import navigation_bar
from instance_analysis import single_instance_analysis, multiple_instance_analysis, analysis_stored_data, upload_stored_sets
from utils import firebase

st.set_page_config(
     page_title="KEPIA",
     layout="wide",
     initial_sidebar_state="expanded",
 )

if 'db_ref' not in st.session_state:
    st.session_state['db_ref'] = firebase.get_DB_Config()

nav_instance = navigation_bar.Navigation()
nav_instance.add_page("Multiple Instances Analysis(Stored Sets)", analysis_stored_data.app)
nav_instance.add_page("Upload Data (Stored Sets) Only admin ", upload_stored_sets.app)
nav_instance.add_page("Multiple Instances Analysis(Upto 100 Files)", multiple_instance_analysis.app)
nav_instance.add_page("Single Instance Analysis", single_instance_analysis.app)
nav_instance.run()
