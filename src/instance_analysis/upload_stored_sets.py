import streamlit as st
import zipfile
import json
import io
import requests
from utils import constants as const

# this page is only for admin, this was created for development purpose, but can be extended in future for users to upload their own sets
def app():
    st.title(const.title)
    st.markdown(const.full_form)
    st.markdown(const.horizontal_line)

    # So that by mistake data-sets cannot be manipilated, it is passwork protected
    ins_string = st.text_input(const.enter_pas, type="password")
    if(ins_string == const.ins_string):
        main()
    # main()

def main():

    uploaded_instances = []
    zipped_file_name = None

    col1,col2 = st.columns(2)

    with col1:
        st.markdown(const.head1)
        st.markdown(const.head2)
        # the file is stored under the filename as the root_directory in DB, starting with the index mentioned

        filename = st.text_input(const.head3)
        i = int(st.number_input(const.head4))
        # Only a zip file of maximum 10 can be uploaded at a time
        uploaded_instances, zipped_file_name = upload_zip_file()

        upload_files_to_database(uploaded_instances, filename,i)

        st.markdown(const.horizontal_line)
    with col1:
        st.markdown(const.head5)
        st.markdown(const.head6)
        # to delete the files , fileneame as well as index from deletion needs to take place is mentioned

        filename_del = st.text_input(const.head7)
        i = int(st.number_input(const.head8))
        k = int(st.number_input(const.head9))

        if(st.button(const.head10)):
            delete_files(i,k,filename_del)
        st.markdown(const.horizontal_line)


def upload_zip_file():
    uploaded_file = None
    instance = None

    try:
        # file area to accept the input
        uploaded_file = st.file_uploader(const.head11, type = ['zip'])
    except Exception as e:
        st.error(const.error_head1)
        st.error(e)


    if uploaded_file is not None:
        try:
            # unzipping the file
            instance, zipped_file_name = get_zip_contents(uploaded_file)
            st.info(const.error_head2 + str(len(instance)))
        except Exception as e:
            st.error(const.error_head3 )
            st.error(e)
    return instance, zipped_file_name

def get_zip_contents(uploaded_file):
    instance_list = []
    zbytes = uploaded_file.getvalue()
    zf = zipfile.ZipFile(io.BytesIO(zbytes), "r")
    zipped_file_name = (zf.infolist())[0].filename

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
    return instance_list, zipped_file_name

def upload_files_to_database(uploaded_instances, filename,i):
    db_ref = None
    if filename and uploaded_instances is not None:
        db_ref = st.session_state.db_ref
        # zipped_file_name = 'SetC'

        for uploaded_instance in uploaded_instances:
            sub = (str(filename) + '_'+str(i)).replace('/','_')
            st.write(sub + " stored")
            # for uploading the file, data and recipients are extracted and stored, and further payload is fetched from the KAL website
            db_ref.child(filename).child(sub).child(const.donor).set(uploaded_instance[const.data])
            db_ref.child(filename).child(sub).child(const.recipients).set(uploaded_instance[const.recipients])
            kep_instances_dict = {const.data: uploaded_instance[const.data]}


            kep_instance_obj  = {
            const.operation: 'maxcard',
            const.altruistic_chain_length: 2,
            const.data: json.dumps(kep_instances_dict)
            }
            response = requests.post(const.kidney_exchange_allocator_url, data = kep_instance_obj )
            payload =  response.json()

            db_ref.child(filename).child(sub).child(const.payload).set(payload)
            i = int(i) + 1
        st.info(const.head12)

def delete_files(i,k, filename):
    db_ref = None
    if  k:
        db_ref = st.session_state.db_ref

        for j in range(i,k):
            zipped_file_name = filename
            sub = (str(zipped_file_name) + '_' +str(j)).replace('/','_')
            db_ref.child(filename).child(sub).remove()
        st.info(const.head13)
    # if filename:
    # db_ref.child('SetA').child('SetA_151').remove()
