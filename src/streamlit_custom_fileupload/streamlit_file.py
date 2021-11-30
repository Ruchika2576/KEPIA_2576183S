import streamlit as st
import json
import zipfile
import io



st.write('Upload a file:')
try:
    uploaded_file = st.file_uploader("Choose a file : ", type = ['zip'])
except Exception as e:
    st.error("!!! Exception has occurred while uploading the file try again, If Exception persists contact support." )

if uploaded_file:
  zbytes = uploaded_file.getvalue()
  zf = zipfile.ZipFile(io.BytesIO(zbytes), "r")
  # st.write(zf.infolist())
  for fileinfo in zf.infolist():
      if fileinfo.file_size == 0:
          continue
      if str(fileinfo.filename).startswith('__MACOSX/'):
          continue
      st.write(f"Processing {fileinfo.filename}")
      with zf.open(fileinfo.filename, 'r') as jsonfile:
          contents = jsonfile.read()
          jsonobj = json.loads(contents)
          st.write('1----------------------------------------------------------------------')
          # st.write(jsonobj["data"])

          ## This break stops the loop from looking at every file. You probably want to remove it
