import streamlit as st
from utils import navigation_bar
from instance_analysis import single_instance_analysis, multiple_instance_analysis, analysis_stored_data, upload_stored_sets
from utils import firebase
from utils import constants as const

# This is the main entery of the program
# The following functions sets the page configuration
st.set_page_config(
     page_title=const.title,
     layout="wide",
     initial_sidebar_state="expanded",
 )

# The db_ref is created only once
if 'db_ref' not in st.session_state:
    st.session_state['db_ref'] = firebase.get_DB_Config()

# The following lines set the navigation bar
nav_instance = navigation_bar.Navigation()
nav_instance.add_page(const.stored_set, analysis_stored_data.app)
nav_instance.add_page(const.single_instance, single_instance_analysis.app)
nav_instance.add_page(const.multiple_instance, multiple_instance_analysis.app)
nav_instance.add_page(const.store_DB, upload_stored_sets.app)


nav_instance.run()
