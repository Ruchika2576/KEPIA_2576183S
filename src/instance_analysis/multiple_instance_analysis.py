import streamlit as st
import pandas as pd
import zipfile
import io
import json
import requests
import concurrent.futures
import time
from time import sleep
import plotly
import plotly.graph_objects as go
import seaborn as sn
import altair as altair
import matplotlib.pyplot as plt
import plotly.express as px

from utils import constants as const
from utils import input_utils
from utils import api_utils
from sub_component_analysis import multiple_donor_analysis, multiple_recipient_analysis, multipl_all_cycle_analysis, multipl_exchange_cycle_analysis


def app():
    # the main execution for analysis starts here
    main()

def main():
    kep_instance_list = []
    recipients_list = []
    multi_upload_data = st.empty()
    with multi_upload_data.container():
        st.title(const.title)
        st.markdown(const.full_form)
        st.markdown(const.horizontal_line)
        st.header(const.multiple_instance_heading)
        st.markdown(const.multiple_file_upload)
        # reading the input options and  zip file

        operation, altruistic_chain_length = input_utils.get_operation_and_chain_length()

        if 'payload_list' not in st.session_state and 'multi_uploaded_zip_instance' not in st.session_state:
            payload_list =None
            multi_uploaded_zip_instance =None
            payload_list, multi_uploaded_zip_instance = input_utils.multi_upload_zip_file(operation, altruistic_chain_length)
            st.session_state.dup1 = payload_list
            st.session_state.dup2 = multi_uploaded_zip_instance
        # displaying message on file upload
            if payload_list:
                st.success(const.success2)
        # displaying begin analysis button
        if 'single_begin_analysis_butto' not in st.session_state:
            st.session_state.single_begin_analysis_butto = False
        single_begin_analysis_butto = st.button(const.multiple_begin_button)

        # proceed with analysis if user clicks the button
    if (st.session_state.single_begin_analysis_butto  or ( single_begin_analysis_butto and st.session_state.dup2)):

         st.session_state.payload_list = st.session_state.dup1
         st.session_state.multi_uploaded_zip_instance = st.session_state.dup2
         multi_upload_data.empty()
         st.session_state.single_begin_analysis_butto = True

        #payload_list = (get4(multi_uploaded_zip_instance,operation, altruistic_chain_length))

         if 'recipients_list' not in st.session_state and 'kep_instance_list' not in st.session_state:
             for instance in multi_uploaded_zip_instance:
                 # Extracting, recipient and donors list
                recipients_list.append(instance[const.recipients])
                kep_instance_list.append(instance[const.data])
                st.session_state.recipients_list = recipients_list
                st.session_state.kep_instance_list = kep_instance_list

             with st.container():
                    col2, col3 = st.columns(2)
                    # col1.markdown(""" **_Uploaded File_** - """ + str(filename))
                    col2.markdown(const.operation_heading + str(operation))
                    col3.markdown(const.alt_heading + str(altruistic_chain_length))
         if 'recipients_list'  in st.session_state and 'kep_instance_list' in st.session_state:
             # after fetching data beginning analysis
             # after extracting recipient and donor and payload information proceed for analysis
            analysis(st.session_state.kep_instance_list,st.session_state.recipients_list,st.session_state.payload_list )

    elif (single_begin_analysis_butto and not multi_uploaded_zip_instance):
         st.error(const.error6)

# analysis is grouped into expanders as shown below
def analysis(kep_instance_list,recipients_list,payload_list ):
        st.title(const.title)
        st.warning(const.warning1)

        with st.expander(const.donor_expand_multiple):
            multiple_donor_analysis.analysis_donor(kep_instance_list, 'donor_instances_df')
        with st.expander(const.recipient_expand_multiple):
            multiple_recipient_analysis.analysis_recipient(recipients_list,'recipients_instances_fin_df')
        with st.expander(const.all_cycle_expand_multiple):
            multipl_all_cycle_analysis.analysis_multiple_payload(payload_list,'payload_fin_df')
        with st.expander(const.exchange_cycle_expand_multiple):
            multipl_exchange_cycle_analysis.analysis_multiple_exchanges(payload_list,'exchange_data_final_df')
