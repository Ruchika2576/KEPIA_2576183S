import collections
from numpy.core.defchararray import lower
import streamlit as st
import numpy as np
import pandas as pd
import zipfile
import streamlit.components.v1 as components
import io
import json
import sys
import requests
import concurrent.futures
import time
from time import sleep


def app():
    st.title("KEPIA")
    st.markdown(""" ---Kidney Exchange Program Instance Analyser ---""")
    st.markdown("""***""")
    main()

def main():


    st.header("Multiple Instance Analysis")
    st.markdown("#### Select from the following Sets to Analyze: ")

    operation = st.selectbox('Choose Set : ',('Set A','Set B','Set C', 'Set D', 'Set E', 'Set F'))

    
