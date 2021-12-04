import streamlit as st
import zipfile
import json
import io
import requests

kidney_exchange_allocator_url = 'https://kidney-nhs.optimalmatching.com/kidney/find.json'

def app():
    st.title("KEPIA")
    st.markdown(""" ---Kidney Exchange Program Instance Analyser ---""")
    st.markdown("#### Data Upload : Only admin")
    st.markdown("Upload a zip file (10 files only) to store")

    # password = st.text_input("Enter admin password", type="password")
    # if(password == 'Kepia@123'):
    main()
    # main()

def main():

    uploaded_instances = []
    zipped_file_name = None

    col1,col2 = st.columns(2)

    with col1:

        filename = st.text_input('Enter the root File name * (File will be stored under this directory)')
        i = int(st.number_input('Enter index  *(files will be stored as filename_index)'))
        uploaded_instances, zipped_file_name = upload_zip_file()

        upload_files_to_database(uploaded_instances, filename,i)

        st.markdown("""***""")
    with col2:
        st.markdown("#### Data Delete : Only admin")
        st.markdown("#### To delete Files")

        filename_del = st.text_input('Enter File name(root directory)')
        i = int(st.number_input('Enter Start index'))
        k = int(st.number_input('Enter End index '))

        if(st.button("delete")):
            delete_files(i,k,filename_del)
        st.markdown("""***""")


def upload_zip_file():
    uploaded_file = None
    instance = None
    zipped_file_name = None

    try:
        uploaded_file = st.file_uploader("Choose a file : ", type = ['zip'])
    except Exception as e:
        st.error("!!! Exception has occurred while uploading the file try again, If Exception persists contact support." )


    if uploaded_file is not None:
        try:
            instance, zipped_file_name = get_zip_contents(uploaded_file)
            st.info('Zip File Upload and Extracted Successfully. Total Number of files extracted - ' + str(len(instance)))
        except Exception as e:
            st.error("!!! Exception has occurred while reading the file try again, If Exception persists contact support." )
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
            db_ref.child(filename).child(sub).child("donor").set(uploaded_instance['data'])
            db_ref.child(filename).child(sub).child("recipients").set(uploaded_instance['recipients'])
            kep_instances_dict = {'data': uploaded_instance['data']}

            kep_instance_obj  = {
            'operation': 'maxcard',
            'altruistic_chain_length': 2,
            'data': json.dumps(kep_instances_dict)
            }
            response = requests.post(kidney_exchange_allocator_url, data = kep_instance_obj )
            payload =  response.json()

            db_ref.child(filename).child(sub).child("payload").set(payload)
            i = int(i) + 1
        st.info('File Stored Successfully!!')

def delete_files(i,k, filename):
    db_ref = None
    if  k:
        db_ref = st.session_state.db_ref

        for j in range(i,k):
            zipped_file_name = filename
            sub = (str(zipped_file_name) + '_' +str(j)).replace('/','_')
            db_ref.child(filename).child(sub).remove()
        st.info('File Deleted Successfully!!')
    # if filename:
    # db_ref.child('SetA').child('SetA_151').remove()
