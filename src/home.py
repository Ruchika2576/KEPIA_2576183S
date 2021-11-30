import streamlit as st

import sys
sys.path.append('utils')
from navigation_bar import Navigation

sys.path.append('instance_analysis')
import single_instance_analysis, multiple_instance_analysis, analysis_stored_data, upload_stored_sets

sys.path.append('utils')
from firebase import get_DB_Config

if 'db_ref' not in st.session_state:
    st.session_state['db_ref'] = get_DB_Config()

navigation_instance = Navigation()


navigation_instance.add_page("Multiple Instances Analysis(Stored Sets)", analysis_stored_data.app)
navigation_instance.add_page("Upload Data (Stored Sets) Only admin ", upload_stored_sets.app)
navigation_instance.add_page("Multiple Instances Analysis(Upto 100 Files)", multiple_instance_analysis.app)
navigation_instance.add_page("Single Instance Analysis", single_instance_analysis.app)
navigation_instance.run()
