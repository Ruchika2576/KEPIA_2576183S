
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


kidney_exchange_allocator_url = 'https://kidney-nhs.optimalmatching.com/kidney/find.json'
def app():
    st.title("KEPIA")
    main()

def main():
    kep_instance_list = []
    recipients_list = []
    payload_list = None
    uploaded_zip_instance = None



    upload_data = st.empty()
    with upload_data.container():
        st.markdown(""" ---Kidney Exchange Program Instance Analyser ---""")
        st.header("Multiple Instance Analysis")
        st.markdown("#### Data Upload : Upload a zip file of instances for analysis")

        operation, altruistic_chain_length = get_operation_and_chain_length()
        with st.container():
                col2, col3 = st.columns(2)
                # col1.markdown(""" **_Uploaded File_** - """ + str(filename))
                col2.markdown(""" **_Operation_ ** - """ + str(operation))
                col3.markdown("""**_Altruistic Chain Length_** - """ + str(altruistic_chain_length))


        if 'payload_list' not in st.session_state and 'uploaded_zip_instance' not in st.session_state:
            payload_list, uploaded_zip_instance = upload_zip_file(operation, altruistic_chain_length)


        if payload_list:
            st.info('File Uploaded.Begin Analysis.')


        if 'begin_analysis_button' not in st.session_state:
            st.session_state.begin_analysis_button = False
        begin_analysis_button = st.button("Begin Analysis ")


    if (st.session_state.begin_analysis_button or( begin_analysis_button and uploaded_zip_instance)):
         st.session_state.payload_list = payload_list
         st.session_state.uploaded_zip_instance = uploaded_zip_instance
         upload_data.empty()
         st.session_state.begin_analysis_button = True

        #payload_list = (get4(uploaded_zip_instance,operation, altruistic_chain_length))

         if 'recipients_list' not in st.session_state and 'kep_instance_list' not in st.session_state:
             for instance in uploaded_zip_instance:

                recipients_list.append(instance['recipients'])
                kep_instance_list.append(instance['data'])
                st.session_state.recipients_list = recipients_list
                st.session_state.kep_instance_list = kep_instance_list

             with st.container():
                    col2, col3 = st.columns(2)
                    # col1.markdown(""" **_Uploaded File_** - """ + str(filename))
                    col2.markdown(""" **_Operation_ ** - """ + str(operation))
                    col3.markdown("""**_Altruistic Chain Length_** - """ + str(altruistic_chain_length))

             analysis(st.session_state.kep_instance_list,st.session_state.recipients_list,st.session_state.payload_list )

    elif (begin_analysis_button and not uploaded_zip_instance):
         st.error('No file uploaded! Refresh.')


def upload_zip_file(operation, altruistic_chain_length):
    uploaded_file = None
    instance = None
    payload_list = None
    try:

        uploaded_file = st.file_uploader("Choose a file : ", type = ['zip'])

    except Exception as e:
        st.error("!!! Exception has occurred while uploading the file try again, If Exception persists contact support." )


    if uploaded_file is not None:
        try:
            instance = get_zip_contents(uploaded_file)
            st.info('Zip File Upload and Extracted Successfully. Total Number of files extracted - ' + str(len(instance)))
            st.warning('File Uploading, Please Wait')
            payload_list = get_data_NHS_Optimal(instance,operation, altruistic_chain_length)
            #payload_list = ioloop.IOLoop.current().run_sync(get6(uploaded_zip_instance,operation, altruistic_chain_length))

        except Exception as e:
            st.error("!!! Exception has occurred while fetching data from external API. Please wait or contact if issue persist!!" )
            st.error(e)

    #start = time.time()
    #payload_list = get_all_response_from_KAL(uploaded_zip_instance,operation, altruistic_chain_length)

    #end = time.time()
    # st.write('Length of the final payload list:' + str(len(payload_list)))
    #st.write('total time taken for the entire process:' + str((end-start)/60) + 'mins')

    return payload_list, instance

def get_zip_contents(uploaded_file):
    instance_list = []
    zbytes = uploaded_file.getvalue()
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

def get_operation_and_chain_length():

    operation = st.selectbox('Choose Operation : ',('optimal','maxcard','pairs'))
    altruistic_chain_length = st.selectbox('Choose Altruistic Chain Length :',('1','2'))

    return operation,altruistic_chain_length

#multithread Processing
def get3(session,kep_instance_obj):

    response = session.send(requests.Request('POST',kidney_exchange_allocator_url, data = kep_instance_obj ).prepare())
    payload =  response.json()

    return payload

def get4(uploaded_zip_instance,operation,altruistic_chain_length ):
    #create an aiohttp session, to handle all the requests
    payload_list =[]
    instance_obj_list = []
    future_list = []
    for instance in uploaded_zip_instance:

        #this function will perform the actual request
        kep_instance = instance['data']

        #Creating request params to call the Kidney Exchange allocator
        kep_instances_dict = {'data': kep_instance}

        kep_instance_obj  = {
        'operation': operation,
        'altruistic_chain_length': int(altruistic_chain_length),
        'data': json.dumps(kep_instances_dict)
        }
        instance_obj_list.append(kep_instance_obj)


    with concurrent.futures.ThreadPoolExecutor(max_workers = 200) as executor:
        with requests.Session() as session:

            for kep_instance_obj in instance_obj_list:

                futures = executor.submit(get3,session = session ,kep_instance_obj =kep_instance_obj)
                future_list.append(futures)

            for future in concurrent.futures.as_completed(future_list):
                #st.write('length ' + str(len(future_list)))
                try:
                    payload_list.append(future.result())
                except requests.ConnectTimeout:
                    print("ConnectTimeout.")

    return payload_list

@st.cache(suppress_st_warning = True)
def get_data_NHS_Optimal(uploaded_zip_instance,operation, altruistic_chain_length):
    length = len(uploaded_zip_instance)
    rem = length % 50
    loops = (length-rem)//50
    payload_list = None
    final_payload_list = []

    k = 0
    b = 0
    a = 0

    if len(uploaded_zip_instance) > 50:
        for i in range(0,loops):
            # st.write('---------beginning loop :' + str(i) +'----------')
            a = k+49
            sub_instances = []
            for j in range(k,a+1):
                sub_instances.append(uploaded_zip_instance[j])
            st.write('length of sub list:', str(len(sub_instances)))
            start = time.time()
            st.write('sleeping for 60 seconds')
            sleep(400)
            payload_list = get4(sub_instances,operation,altruistic_chain_length )
            final_payload_list.extend(payload_list)
            end = time.time()
            st.write('time taken execute this loop' + str(i) + ':' + str((end-start)/60) + 'minutes')
            k = a+1


        if rem !=0:
            # st.write('---------remaining list----------')
            sub_instances = []
            for i in range(a, length):
                sub_instances.append(uploaded_zip_instance[i])
            st.write('length of sub list:', str(len(sub_instances)))
            payload_list = get4(sub_instances,operation,altruistic_chain_length )
            final_payload_list.extend(payload_list)

        return final_payload_list

    else:
        # st.write('---------List is less than 50----------')
        payload_list = get4(uploaded_zip_instance,operation,altruistic_chain_length )
        return payload_list

def analysis(kep_instance_list,recipients_list,payload_list ):
        with st.expander('Analyse Donors in the Set'):
            donor_data_analysis(kep_instance_list)
        with st.expander('Analyse Recipients in the Set'):
            recipient_data_analysis(recipients_list)
        with st.expander('Analyse All Cycles in the set'):
            all_cycle_anlysis(payload_list)
        with st.expander('Analyse Exchange Cycles in the set'):
            exchange_cycle_anlysis(payload_list)

def donor_data_analysis(donors_list):
        donor_instance_list_data = None
        donor_instances_df = None

        donors_count = []
        no_matches_list = []
        avg_total_matches_list = []
        max_matches_list = []
        min_matches_list =[]
        non_alt_list = []
        alt_list = []
        multiple_sources_l =[]
        avg_age_l =[]
        med_age_l =[]
        min_age_l =[]
        max_age_l =[]
        a_type_l = []
        b_type_l = []
        o_type_l = []
        ab_type_l = []

        if 'donor_instances_df' not in st.session_state:
            instance_ids = list(range(1, len(donors_list)+1))

            for donor_sub in donors_list:
                    number_of_donors = 0
                    no_matches = 0
                    average_total_matches = 0
                    max_matches = 0
                    min_matches = 0
                    non_alt = 0
                    alt = 0
                    multiple_sources = 0
                    avg_age = 0
                    med_age = 0
                    min_age = 0
                    max_age = 0
                    a,o,b,ab = 0,0,0,0

                    donor = pd.DataFrame(donor_sub).T
                    donor['matcoun'] = donor.apply(lambda row: (count_matches(row)) ,axis = 1)

                    #Calculating values
                    number_of_donors = donor.shape[0]
                    average_total_matches = donor['matcoun'].mean()
                    max_matches = donor['matcoun'].max()
                    min_matches = donor['matcoun'].min()
                    no_matches= donor['matcoun'].isnull().sum()
                    non_alt = donor['altruistic'].isnull().sum()
                    alt = number_of_donors - non_alt
                    multiple_sources = count_sources(donor)
                    avg_age = donor['dage'].mean()
                    med_age = donor['dage'].median()
                    min_age =donor['dage'].min()
                    max_age = donor['dage'].max()
                    a,o,b,ab = count_blood_distribution(donor)

                    #appending to list
                    donors_count.append(number_of_donors)
                    no_matches_list.append(no_matches)
                    avg_total_matches_list.append(average_total_matches)
                    min_matches_list.append(min_matches)
                    max_matches_list.append(max_matches)
                    non_alt_list.append(non_alt)
                    alt_list.append(alt)
                    multiple_sources_l.append(multiple_sources)
                    avg_age_l.append(avg_age)
                    med_age_l.append(med_age)
                    min_age_l.append(min_age)
                    max_age_l.append(max_age)
                    a_type_l.append(a)
                    b_type_l.append(b)
                    o_type_l.append(o)
                    ab_type_l.append(ab)

            donor_instance_list_data = {
            'Instance Id': instance_ids,
            'No. of Donors':donors_count,
            'Avg No. of Matches': avg_total_matches_list,
            'Donors with No Matches': no_matches_list,
            'Min No. of matches':min_matches_list,
            'Max No. of matches':max_matches_list,
            'Altruistic donors':alt_list,
            'Non Altruistuc donors:':non_alt_list,
            'Sources with multiple donors':multiple_sources_l,
            'Average Age':avg_age_l,
            'Min Age':min_age_l,
            'Max Age':max_age_l,
            'Median age':med_age_l,
            'A boodtype Avg':a_type_l,
            'B boodtype Avg':b_type_l,
            'O boodtype Avg':o_type_l,
            'AB boodtype Avg':ab_type_l,
            }

            donor_instances_df = pd.DataFrame(donor_instance_list_data)
            st.session_state.donor_instances_df = donor_instances_df
        st.markdown("""#### Donor Data Analysis in Sets""")
        st. dataframe(donor_instances_df)

        st.markdown("""#### Accumulative statistics of the set""")
        # index = ['No of Cycles','No of Two Cycles','No of Three Cycles', 'No of Short chains',
        #  'No of Long chains', 'weight Avg', 'weight Median','weight std','No of Cycles with backarcs']
        x = donor_instances_df.copy()
        del x['Instance Id']
        st.dataframe(x.describe().iloc[[1,2,3,4,5,6,7]])

        # a = donor_instances_df['No. of Donors'].mean()
        # st.markdown("""###### Average No. of donors """ + str(a))
        # b = donor_instances_df['Avg No. of Matches'].mean()
        # st.markdown("""###### Average No. of Matches """ + str(b))
        # c = donor_instances_df['Sources with multiple donors'].mean()
        # st.markdown("""###### Average No. of Multiple sources in donors """ + str(c))
        # d = donor_instances_df['A boodtype Avg'].mean()
        # e= donor_instances_df['B boodtype Avg'].mean()
        # f= donor_instances_df['O boodtype Avg'].mean()
        # g= donor_instances_df['AB boodtype Avg'].mean()
        # st.markdown("""###### Average No. donors with bloodtype A """ + str(d))
        # st.markdown("""###### Average No. donors with bloodtype B """ + str(e))
        # st.markdown("""###### Average No. donors with bloodtype O """ + str(f))
        # st.markdown("""###### Average No. donors with bloodtype AB """ + str(g))



def recipient_data_analysis(recipients_list):
    recipients_instances_data = None
    recipients_instances_fin_df = None

    number_of_recipients_l = []
    non_compatible_l = []
    compatible_l = []
    a_l = []
    o_l = []
    b_l = []
    ab_l = []
    cPRA_mean_l = []
    cPRA_median_l = []
    cPRA_std_deviation_l = []

    if 'recipients_instances_fin_df' not in st.session_state:
        instance_ids = list(range(1, len(recipients_list)+1))

        for recipients in recipients_list:
            number_of_recipients = 0
            non_compatible = 0
            compatible = 0
            a,o,b,ab = 0,0,0,0
            cPRA_mean = 0
            cPRA_median = 0
            cPRA_std_deviation = 0

            recipients_df = pd.DataFrame(recipients).T

            number_of_recipients = recipients_df.shape[0]
            non_compatible,compatible = count_compatible(recipients_df)
            a,o,b,ab = count_blood_distribution(recipients_df)
            cPRA_mean = recipients_df['cPRA'].mean()
            cPRA_median = recipients_df['cPRA'].median()
            cPRA_std_deviation = recipients_df['cPRA'].std()

            #appending to list
            number_of_recipients_l.append(number_of_recipients)
            non_compatible_l.append(non_compatible)
            compatible_l.append(compatible)
            a_l.append(a)
            o_l.append(o)
            b_l.append(b)
            ab_l.append(ab)
            cPRA_mean_l.append(cPRA_mean)
            cPRA_median_l.append(cPRA_median)
            cPRA_std_deviation_l.append(cPRA_std_deviation)

        recipients_instances_data = {
        'Instance id': instance_ids,
        'Number of recipients':number_of_recipients_l,
        'No compatible donor':non_compatible_l,
        'Has compatible donor': compatible_l,
        'A bloodtype avg' : a_l,
        'O bloodtype avg': o_l,
        'B bloodtype avg': b_l,
        'AB bloodtype avg': ab_l,
        'cPRA mean' : cPRA_mean_l,
        'cPRA median' : cPRA_median_l,
        'cPRA std': cPRA_std_deviation_l
        }

        recipients_instances_fin_df = pd.DataFrame(recipients_instances_data)

        st.session_state.recipients_instances_fin_df = recipients_instances_fin_df
    st.markdown("""#### Recipients Data Analysis in Sets""")
    st. dataframe(recipients_instances_fin_df)

    st.markdown("""#### Accumulative statistics of the set""")
    # index = ['No of Cycles','No of Two Cycles','No of Three Cycles', 'No of Short chains',
    #  'No of Long chains', 'weight Avg', 'weight Median','weight std','No of Cycles with backarcs']
    x = recipients_instances_fin_df.copy()
    del x['Instance id']
    st.dataframe(x.describe().iloc[[1,2,3,4,5,6,7]])

    # a = recipients_instances_fin_df['Number of recipients'].mean()
    # st.markdown("""###### Average No. of Recipients """ + str(a))
    # b = recipients_instances_fin_df['No compatible donor'].mean()
    # st.markdown("""###### Average No. of Recipients with no compatible donor """ + str(b))
    # b1 = recipients_instances_fin_df['Has compatible donor'].mean()
    # st.markdown("""###### Average No. of Recipients with Compatible donor """ + str(b1))
    #
    # # c = donor_instances_df['Sources with multiple donors'].mean()
    # # st.markdown("""###### Average No. of Multiple sources in donors """ + str(c))
    # d = recipients_instances_fin_df['A boodtype Avg'].mean()
    # e= recipients_instances_fin_df['B boodtype Avg'].mean()
    # f= recipients_instances_fin_df['O boodtype Avg'].mean()
    # g= recipients_instances_fin_df['AB boodtype Avg'].mean()
    # st.markdown("""###### Average No. Recipients with bloodtype A """ + str(d))
    # st.markdown("""###### Average No. Recipients with bloodtype B """ + str(e))
    # st.markdown("""###### Average No. Recipients with bloodtype O """ + str(f))
    # st.markdown("""###### Average No. Recipients with bloodtype AB """ + str(g))
    #
    # m = recipients_instances_fin_df['cPRA mean'].mean()
    # m1 =recipients_instances_fin_df['cPRA median'].mean()
    # m2 = recipients_instances_fin_df['cPRA std'].mean()
    #
    # st.markdown("""###### set cPRA mean :"""+str(m))
    # st.markdown("""###### set cPRA median :"""+str(m1))
    # st.markdown("""###### set cPRA std :"""+str(m2))

def all_cycle_anlysis(payload_list):
        payload_all_cycle_data = None
        payload_fin_df = None

        no_of_cycles_l = []
        no_of_two_cycles = []
        no_of_three_cycles = []
        no_of_short_chains_l = []
        no_of_long_chains_l = []
        weight_avg_l = []
        weight_median_l = []
        weight_std_l = []
        cycles_with_backarcs_l = []

        if 'payload_fin_df' not in st.session_state:
            instance_ids = list(range(1, len(payload_list)+1))

            for payload in payload_list:
                  no_of_cycles = 0
                  no_two_cycles = 0
                  no_three_cycles = 0
                  no_of_short_chains = 0
                  no_of_long_chains = 0
                  weight_avg = 0
                  weight_median = 0
                  weight_std = 0

                  all_ids = []
                  all_cycles = payload.get('output').get('all_cycles')
                  for i in all_cycles:
                        all_ids.append(i)
                  all_cycle_dataframe = pd.DataFrame(all_cycles).T
                  all_cycle_dataframe = all_cycle_dataframe.astype({'cycle': 'str' })
                  all_cycle_dataframe = all_cycle_dataframe.astype({'alt' : 'str'})

                  no_of_cycles = len(all_cycle_dataframe)

                  cycle_2, cycle_3, s_chain, l_chain = calculate_cycles_chains(payload,all_ids)

                  all_cycle_dataframe['Two cycles'] = cycle_2
                  all_cycle_dataframe['Three cycles'] = cycle_3
                  all_cycle_dataframe['Short Chains'] = s_chain
                  all_cycle_dataframe['Long Chains'] = l_chain

                  no_two_cycles = all_cycle_dataframe['Two cycles'].sum()
                  no_three_cycles = all_cycle_dataframe['Three cycles'].sum()
                  no_of_short_chains = all_cycle_dataframe['Short Chains'].sum()
                  no_of_long_chains = all_cycle_dataframe['Long Chains'].sum()

                  weight_avg = all_cycle_dataframe['weight'].mean()
                  weight_median = all_cycle_dataframe['weight'].median()
                  weight_std = all_cycle_dataframe['weight'].std()
                  cycles_with_backarcs = len(all_cycle_dataframe['backarcs'][all_cycle_dataframe['backarcs'] > 0])

                  no_of_cycles_l.append(no_of_cycles)
                  no_of_two_cycles.append(no_two_cycles)
                  no_of_three_cycles.append(no_three_cycles)
                  no_of_short_chains_l.append(no_of_short_chains)
                  no_of_long_chains_l.append(no_of_long_chains)
                  weight_avg_l.append(weight_avg)
                  weight_median_l.append(weight_median)
                  weight_std_l.append(weight_std)
                  cycles_with_backarcs_l.append(cycles_with_backarcs)

            payload_all_cycle_data = {
                'Instance Ids' : instance_ids,
                'No of Cycles' : no_of_cycles_l ,
                'No of Two Cycles' : no_of_two_cycles ,
                'No of Three Cycles' : no_of_three_cycles,
                'No of Short chains' : no_of_short_chains_l ,
                'No of Long chains' : no_of_long_chains_l ,
                'weight Avg' : weight_avg_l ,
                'weight Median' : weight_median_l ,
                'weight std' : weight_std_l ,
                'No of Cycles with backarcs' : cycles_with_backarcs_l
                }

            payload_fin_df = pd.DataFrame(payload_all_cycle_data)

            st.session_state.payload_fin_df = payload_fin_df
        st.markdown("""#### All cycles Analysis in Sets""")
        st. dataframe(payload_fin_df)
        st.markdown("""#### Accumulative statistics of the set""")
        index = ['No of Cycles','No of Two Cycles','No of Three Cycles', 'No of Short chains',
         'No of Long chains', 'weight Avg', 'weight Median','weight std','No of Cycles with backarcs']
        st.dataframe(payload_fin_df.describe()[index].iloc[[1,2,3,4,5,6,7]])



def exchange_cycle_anlysis(payload_list):
    exchange_data_instances = None
    exchange_data_final_df = None
    description = payload_list[0].get('output').get('exchange_data')[0].get('description')

    no_exc_cycles = []
    weight_l = []
    two_way_exc_l = []
    three_way_exc_l = []
    total_transplants_l = []
    no_of_two_cycles_l = []
    no_of_three_cycles_l = []
    no_of_short_chains_l = []
    no_of_long_chains_l = []
    weight_avg_l = []
    weight_median_l = []
    weight_std_l = []
    cycles_with_backarcs_l = []
    if 'exchange_data_final_df' not in st.session_state:
            instance_ids = list(range(1, len(payload_list)+1))

            for payload in payload_list:
                  exchange_data = payload.get('output').get('exchange_data')[0]
                  exchanges = exchange_data.get('exchanges')
                  weight_l.append(exchange_data.get('weight'))
                  two_way_exc_l.append(exchange_data.get('two_way_exchanges'))
                  three_way_exc_l.append(exchange_data.get('three_way_exchanges'))
                  total_transplants_l.append(exchange_data.get('total_transplants'))

                  exc_cycle_ids = []
                  exchange_cycle_list = []
                  for i in exchanges:
                        exc_cycle_ids.append(str(i))
                        exchange_cycle_list.append(payload.get('output').get('all_cycles').get(str(i)))
                  exc_cycle_df = pd.DataFrame(exchange_cycle_list)

                  no_exc_cycles.append(len(exc_cycle_df))

                  cycle_2, cycle_3, s_chain, l_chain = calculate_cycles_chains(payload,exc_cycle_ids)
                  exc_cycle_df['Two cycles'] = cycle_2
                  exc_cycle_df['Three cycles'] = cycle_3
                  exc_cycle_df['Short Chains'] = s_chain
                  exc_cycle_df['Long Chains'] = l_chain

                  no_of_two_cycles_l.append(exc_cycle_df['Two cycles'].sum())
                  no_of_three_cycles_l.append(exc_cycle_df['Three cycles'].sum())
                  no_of_short_chains_l.append(exc_cycle_df['Short Chains'].sum())
                  no_of_long_chains_l.append(exc_cycle_df['Long Chains'].sum())

                  weight_avg_l.append(exc_cycle_df['weight'].mean())
                  weight_median_l.append(exc_cycle_df['weight'].median())
                  weight_std_l.append(exc_cycle_df['weight'].std())
                  cycles_with_backarcs_l.append(len(exc_cycle_df['backarcs'][exc_cycle_df['backarcs'] > 0]))


            exchange_data_instances = {
            'Instance Ids' : instance_ids,
            'No. of Exchange Cycles' : no_exc_cycles,
            'Weight of exchanges': weight_l,
            'Two - way echange': two_way_exc_l,
            'Three Way exchange':three_way_exc_l ,
            'Total Transplants': total_transplants_l ,
            'No. of two cyles': no_of_two_cycles_l ,
            'No. of three cycles' : no_of_three_cycles_l ,
            'No. of short chains':no_of_short_chains_l ,
            'No. of long chains' : no_of_long_chains_l,
            'Cycle Containing Backarcs' : cycles_with_backarcs_l,
            'Avg weight of exc cycles' : weight_avg_l ,
            'Median weight of exc cycles':weight_median_l ,
            'Std weight of exc cycles':weight_std_l
            }

            exchange_data_final_df = pd.DataFrame(exchange_data_instances)
            st.session_state.exchange_data_final_df = exchange_data_final_df


    st.markdown("""#### Exchange cycles Analysis in Sets""")
    st.markdown('Description:' +description)
    st. dataframe(exchange_data_final_df)
    st.markdown("""#### Accumulative statistics of the set""")
    index = ['No. of Exchange Cycles','Weight of exchanges','Two - way echange', 'Three Way exchange',
     'Total Transplants', 'No. of two cyles', 'No. of three cycles','No. of short chains','No. of long chains', 'Cycle Containing Backarcs',
     'Avg weight of exc cycles']
    st.dataframe(exchange_data_final_df.describe()[index].iloc[[1,2,3,4,5,6,7]])










def calculate_cycles_chains(payload,ids):
    cycle_2 = []
    cycle_3 = []
    s_chain = []
    l_chain = []
    for i in ids:
      c2 = 0
      c3 = 0
      sc = 0
      lc = 0
      type =''

      a = payload.get('output').get('all_cycles').get(str(i)).get('cycle')
      df = pd.DataFrame(a)

      c2,c3,sc,lc,type = per_cycle(df)

      cycle_2.append(c2)
      cycle_3.append(c3)
      s_chain.append(sc)
      l_chain.append(lc)

    return cycle_2, cycle_3, s_chain, l_chain

def per_cycle(df):
    c2 = 0
    c3 = 0
    sc = 0
    lc = 0
    is_altruistic = False
    rows = len(df)
    type = ''
    if 'a' in df:
        is_altruistic = True

    if rows == 2:
         if is_altruistic:
             sc = 1
             type = 'Short chain'

         else:
             c2 = 1
             type = 'Two cycle'
    elif rows == 3:
        if is_altruistic:
            lc = 1
            type = 'Long chain'
        else:
            c3 = 1
            type = 'Three cycle'
    return c2,c3,sc,lc,type


def count_compatible(recipients):
  ncompatible,compatible = 0,0
  values = recipients['hasBloodCompatibleDonor'].value_counts()
  ind = values.index.tolist()

  for idx,comp in enumerate(ind):
    if comp == True:
      compatible = values[idx]
    else:
      ncompatible = values[idx]
  return ncompatible,compatible

def count_matches(row):
      if isinstance((row['matches']), list) :
        return int(len(row['matches']))
      else:
        return 0
def count_sources(donor):
      x = donor['sources'].value_counts(dropna = 'True')
      y = x.where(x > 1).value_counts(dropna = 'True').sum()
      return y
def count_blood_distribution(donor):
      a = 0
      b = 0
      o = 0
      ab = 0

      btvalues = donor['bloodtype'].value_counts()
      ind = btvalues.index.tolist()
      for idx,bt in enumerate(ind):
        if bt =='A':
          a = btvalues[idx]
        if bt =='O':
          o = btvalues[idx]
        if bt =='B':
          b = btvalues[idx]
        if bt =='AB':
          ab = btvalues[idx]
      return a,o,b,ab
# #direct call
# def get_all_response_from_KAL(uploaded_zip_instance,operation, altruistic_chain_length):
#     payload_list = []
#     a = []
#
#     for instance in uploaded_zip_instance:
#         payload = get_response_from_KAL(instance, operation,altruistic_chain_length)
#         payload_list.append(payload)
#     st.write('payload list' + str(len(payload_list)))
#
#
#
#     return payload_list
#
# def get_response_from_KAL(instance, operation,altruistic_chain_length):
#     #Extracting the json dictionary into KEP instances and recipients
#
#     kep_instance = instance['data']
#     recipients = instance['recipients']
#
#     #Creating request params to call the Kidney Exchange allocator
#     kep_instances_dict = {'data': kep_instance}
#
#     kep_instance_obj  = {
#     'operation': operation,
#     'altruistic_chain_length': int(altruistic_chain_length),
#     'data': json.dumps(kep_instances_dict)
#     }
#
#     try:
#         response = requests.post(kidney_exchange_allocator_url, data = kep_instance_obj)
#     except Exception as exc:
#         st.error('Error ocurred while fetching data from https://kidney-nhs.optimalmatching.com/' )
#         st.error(exc)
#
#     if response.status_code == 200:
#         payload = response.json()
#     else:
#         st.error(f"Request returned: {response.status_code} : '{response.reason}'")
#         raise RuntimeError('Error in Response from https://kidney-nhs.optimalmatching.com/')
#
#
#     return payload





    #payload_list = get4(uploaded_zip_instance,operation, altruistic_chain_length)


# @gen.coroutine
# def get6(uploaded_zip_instance,operation,altruistic_chain_length ):
#     #create an aiohttp session, to handle all the requests
#     payload_list =[]
#     instance_obj_list = []
#     future_list = []
#     http_client = httpclient.AsyncHTTPClient()
#
#     for instance in uploaded_zip_instance:
#
#         #this function will perform the actual request
#         kep_instance = instance['data']
#
#         #Creating request params to call the Kidney Exchange allocator
#         kep_instances_dict = {'data': kep_instance}
#
#         kep_instance_obj  = {
#         'operation': operation,
#         'altruistic_chain_length': int(altruistic_chain_length),
#         'data': json.dumps(kep_instances_dict)
#         }
#         instance_obj_list.append(kep_instance_obj)
#
#         request = httpclient.HTTPRequest(kidney_exchange_allocator_url,body = kep_instance_obj, method = 'POST' )
#         response = yield http_client.fetch(request)
#         payload_list.append(response)
#
#     return payload_list
# #asynchronous call
# async def get1(uploaded_zip_instance,operation,altruistic_chain_length ):
#     #create an aiohttp session, to handle all the requests
#     payload_list =[]
#     i = 0
#     async with aiohttp.ClientSession() as session:
#         #create task: each individual requests
#         tasks = []
#         for instance in uploaded_zip_instance:
#
#             #this function will perform the actual request
#             kep_instance = instance['data']
#
#             #Creating request params to call the Kidney Exchange allocator
#             kep_instances_dict = {'data': kep_instance}
#
#             kep_instance_obj  = {
#             'operation': operation,
#             'altruistic_chain_length': int(altruistic_chain_length),
#             'data': json.dumps(kep_instances_dict)
#             }
#
#             # task = asyncio.ensure_future(get2(session, kep_instance_obj))
#             task = get2(session, kep_instance_obj)
#             tasks.append(task)
#
#         payload_list = await asyncio.gather(*tasks)
#         return payload_list
#
# async def get2(session,kep_instance_obj):
#
#     async with session.post(kidney_exchange_allocator_url, data = kep_instance_obj ) as response:
#
#         payload = await response.json()
#
#         return payload

#Reading Files from firebase
# def get_files_from_firebase():
#     storage = get_firebase_connection()
#     all_files = storage.list_files()
#     instance_list = []
#     for file in all_files:
#         url = storage.child(file.name).get_url(None)
#         f = urllib.request.urlopen(url).read()
#         instance = json.loads(f)
#         instance_list.append(instance)
