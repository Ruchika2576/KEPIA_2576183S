import streamlit as st
from utils import constants as const
from sub_component_analysis import multiple_donor_analysis, multiple_recipient_analysis, multipl_all_cycle_analysis, multipl_exchange_cycle_analysis

# This module performs analysis on a stored set
def app():
    st.title(const.title)
    st.markdown(const.full_form)
    st.markdown(const.horizontal_line)
    # the main execution for analysis starts here
    main()

def main():
    data_set = " "

    st.header(const.stored_heading)
    st.markdown(const.select_stored_set)
    with st.container():
           st.markdown(const.stored_set_option)
           col2, col3 = st.columns(2)
           col2.markdown(const.operation_heading + 'Maxcard')
           col3.markdown(const.alt_heading + '2')
           # user input to select the set
    data_set = st.selectbox(const.select_set_message,const.set_options)

    if data_set:
        if 'data_set' not in st.session_state:
            st.session_state.data_set = data_set

        if st.session_state.data_set is not None:
            fetch_data(data_set)
# the set is fetched from the Database
def fetch_data(data_set):
        db_ref = st.session_state.db_ref
        fetch_war = st.empty()
        with fetch_war.container():
            st.warning(const.warning3)

        all_files = db_ref.child(data_set).get()
        fetch_war.empty()
        donors_list_stored = []
        recipient_list_stored = []
        payload_list_stored = []

        if 'donors_list_stored' not in st.session_state and 'recipient_list_store' not in st.session_state and 'payload_list_stored' not in st.session_state:
            st.session_state.donors_list_stored = None
            st.session_state.recipient_list_store = None
            st.session_state.payload_list_stored = None

            for file in all_files.each():

                donors = file.val().get('donor')
                recipient = file.val().get('recipients')
                payload = file.val().get('payload')


                donors_list_stored.append(donors)
                recipient_list_stored.append(recipient)
                payload_list_stored.append(payload)

                st.session_state.donors_list_stored = donors_list_stored
                st.session_state.recipient_list_store = recipient_list_stored
                st.session_state.payload_list_stored = payload_list_stored

        if st.session_state.donors_list_stored is not None and st.session_state.recipient_list_store is not None and st.session_state.payload_list_stored is not None:
                prepare_data(data_set,st.session_state.donors_list_stored,st.session_state.recipient_list_store,st.session_state.payload_list_stored)

# the data is prepared in appropriate format before proceeding with the list
def prepare_data(data_set,donors_list_stored,recipient_list_stored,payload_list_stored):
    donor_final_list_stored = []
    recipient_final_list_stored = []
    payload_final_list_stored = []

    if 'donor_final_list_stored' not in st.session_state and 'recipient_final_list_stored' not in st.session_state and 'payload_final_list_stored' not in st.session_state:
        st.session_state.donor_final_list_stored = None
        st.session_state.recipient_final_list_stored = None
        st.session_state.payload_final_list_stored = None
        # st.write(type(donors_list_stored[0]))
        # st.write(len(donors_list_stored))
        # # st.write((donors_list_stored[0].keys()))
        # # st.write((donors_list_stored[0].values()))
        if data_set == 'SetB' or data_set == 'temp':
            donor_final_list_stored = donors_list_stored
            recipient_final_list_stored =recipient_list_stored
        else:

            for donors_in_file in donors_list_stored:
                i = 0
                donor_dict = {}
                for donors in donors_in_file:

                    if donors is None:
                        continue
                    donor_dict[str(i)] = donors
                    i = i+1
                donor_final_list_stored.append(donor_dict)



            for recipients_in_file in recipient_list_stored:
                j = 0
                recipient_dict = {}
                for recipients in recipients_in_file:
                    if recipients is None:
                        continue
                    recipient_dict[str(j)] = recipients
                    j = j+1
                recipient_final_list_stored.append(recipient_dict)

        for payload_in_file in payload_list_stored:
                if payload_in_file is None:
                    continue
                payload_final_list_stored.append(payload_in_file)

        st.session_state.donor_final_list_stored = donor_final_list_stored
        st.session_state.recipient_final_list_stored = recipient_final_list_stored
        st.session_state.payload_final_list_stored = payload_final_list_stored

    if st.session_state.donor_final_list_stored is not None and st.session_state.recipient_final_list_stored is not None and st.session_state.payload_final_list_stored is not None:

        analysis(st.session_state.donor_final_list_stored,st.session_state.recipient_final_list_stored,st.session_state.payload_final_list_stored)

# analysis is grouped into expanders and begins here
def analysis(donor_final_list_stored,recipient_final_list_stored,payload_final_list_stored):
        load_war = st.empty()
        with load_war.container():
            st.warning(const.warning4)
        with st.expander(const.donor_expand_multiple):
            multiple_donor_analysis.analysis_donor(donor_final_list_stored,'donor_instances_df_stored')
        with st.expander(const.recipient_expand_multiple):
            multiple_recipient_analysis.analysis_recipient(recipient_final_list_stored,'recipients_instances_fin_df_stored')
        with st.expander(const.all_cycle_expand_multiple):
            multipl_all_cycle_analysis.analysis_stored_payload(payload_final_list_stored,'payload_fin_df_stored')
        with st.expander(const.exchange_cycle_expand_multiple):
            multipl_exchange_cycle_analysis.analysis_stored_exchanges(payload_final_list_stored,'exchange_data_final_df_stored')
        load_war.empty()
