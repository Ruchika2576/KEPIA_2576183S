
import streamlit as st
from utils import constants as const
from utils import input_utils
from utils import api_utils
from sub_component_analysis import single_donor_analysis, single_recipient_analysis, single_cycle_analysis

# this is the entry point for the single instance analysis execution
def app():
    main()

# the main starts the execution
def main():
    kep_single_instance = None
    recipients = None
    payload = None

    if 'begin_analysis_button' not in st.session_state:
        st.session_state.begin_analysis_button = False

    upload_data = st.empty()
    with upload_data.container():
        st.title(const.title)
        st.markdown(const.full_form)
        st.markdown(const.horizontal_line)
        st.header(const.single_instance_heading)
        st.markdown(const.single_file_upload)

        # reading user input for file and options
        uploaded_single_instance, filename = input_utils.upload_single_file()
        single_operation, single_altruistic_chain_length = input_utils.get_operation_and_chain_length()
        # displaying begin analysis buttton
        begin_analysis_button = st.button(const.single_begin_analysis)

    # brgin analysis if the button is clicked
    if st.session_state.begin_analysis_button or (begin_analysis_button and uploaded_single_instance):

        upload_data.empty()
        st.session_state.begin_analysis_button = True

        # fetch the data once, do not fetch it again and again
        if 'payload' not in st.session_state:
            payload = api_utils.get_response_from_KAL(uploaded_single_instance, single_operation, single_altruistic_chain_length)
            st.session_state.payload = payload

        if 'donors' not in st.session_state:
            donors = uploaded_single_instance[const.data]
            st.session_state.donors = donors

        if 'recipients' not in st.session_state:
            recipients = uploaded_single_instance[const.recipients]
            st.session_state.recipients = recipients

        with st.container():
            col1, col2, col3 = st.columns(3)
            # display the inputs as headers
            col1.markdown(const.upload_single_file + str(filename))
            col2.markdown(const.operation_heading + str(single_operation))
            col3.markdown(const.alt_heading + str(single_altruistic_chain_length))
            # send the prepared data for analysis
            analysis(st.session_state.donors, st.session_state.recipients, st.session_state.payload)

    elif (begin_analysis_button and not uploaded_single_instance):
        st.error(const.error1)

# the analysis is sectioned into expanders as shown
def analysis(single_instance, recipients, payload):
    st.title(const.title)
    st.info(const.warning1)
    with st.expander(const.donor_expand):
        single_donor_analysis.donor_data_analysis(single_instance)
    with st.expander(const.recipient_expand):
        single_recipient_analysis.recipient_data_analysis(recipients)
    with st.expander(const.all_cycle_expand):
        single_cycle_analysis.all_cycle_anlysis(single_instance, recipients, payload)
    with st.expander(const.exchange_cycle_expand):
        single_cycle_analysis.exchange_cycle_anlysis(single_instance, recipients, payload)
