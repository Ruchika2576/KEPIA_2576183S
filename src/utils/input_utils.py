from utils import constants as const
import json
import zipfile
import io
import streamlit as st
from utils import api_utils
# this module contains functions to read the inputs from the user

# This function handles reading single file
def upload_single_file():
    uploaded_file = None
    single_instance = None
    filename = None
    try:
        uploaded_file = st.file_uploader(const.file_upload, type = ['json'], key = 'single_file')

    except Exception as e:
        st.error(const.error2 )
        st.error(e)

    if uploaded_file is not None:
        filename = uploaded_file.name
        try:
            single_instance = json.loads(uploaded_file.getvalue().decode("utf-8"))
            if single_instance:
                st.success(const.success1)
        except Exception as e:
            st.error(const.error3 )
            st.error(e)
    return single_instance, filename

# This function reads the operation type and altruistic_chain_length
def get_operation_and_chain_length():

    col1, col2 = st.columns(2)
    with col1:
        single_operation = st.selectbox(const.choose_operation, const.operation_options)
    with col2:
        single_altruistic_chain_length = st.selectbox(const.choose_alt,const.alt_options)

    return single_operation,single_altruistic_chain_length


# This fucntion reads a zip_file, send if for extrcation, and fecthes the payload for each instance, and retirns all the sub-
# components to the calling function
def multi_upload_zip_file(operation, altruistic_chain_length):
    multi_uploaded_file = None
    instance = None
    payload_list = None
    cola, colb = st.columns([2,1])

    try:
        multi_uploaded_file = st.file_uploader(const.file_upload, type = ['zip'], key = 'multi_file')
    except Exception as e:
        st.error(const.error7)
        st.error(e)

    if multi_uploaded_file is not None:
        try:
            instance = get_zip_contents(multi_uploaded_file)
            st.markdown(const.success_text + str(len(instance)))
            multi_upload_data_file = st.empty()
            with multi_upload_data_file.container():
                st.warning(const.warning2)
            payload_list = api_utils.get_data_NHS_Optimal(instance,operation, altruistic_chain_length)
            #payload_list = ioloop.IOLoop.current().run_sync(get6(multi_uploaded_zip_instance,operation, altruistic_chain_length))
            multi_upload_data_file.empty()
        except Exception as e:
            st.error(const.error8 )
            st.error(e)

#start = time.time()
    #payload_list = get_all_response_from_KAL(multi_uploaded_zip_instance,operation, altruistic_chain_length)

    #end = time.time()
    # st.write('Length of the final payload list:' + str(len(payload_list)))
    #st.write('total time taken for the entire process:' + str((end-start)/60) + 'mins')

    return payload_list, instance

def get_zip_contents(multi_uploaded_file):
    instance_list = []
    zbytes = multi_uploaded_file.getvalue()
    zf = zipfile.ZipFile(io.BytesIO(zbytes), "r")

    for fileinfo in zf.infolist():

        if fileinfo.file_size == 0:
            continue
        if str(fileinfo.filename).startswith('__MACOSX/'):
            continue
        if '.DS_Store' in str(fileinfo.filename):
            continue

        with zf.open(fileinfo.filename, 'r') as jsonfile:
            contents = jsonfile.read()
            jsonobj = json.loads(contents)

        instance_list.append(jsonobj)
    return instance_list
