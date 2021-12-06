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


kidney_exchange_allocator_url = 'https://kidney-nhs.optimalmatching.com/kidney/find.json'
def app():

    main()

def main():
    kep_instance_list = []
    recipients_list = []





    multi_upload_data = st.empty()
    with multi_upload_data.container():
        st.title("KEPIA")
        st.markdown(""" ---Kidney Exchange Program Instance Analyser ---""")
        st.markdown("""***""")
        st.header("Multiple Instance Analysis")
        st.markdown("#### Data Upload : Upload a zip file of instances for analysis")

        operation, altruistic_chain_length = get_operation_and_chain_length()

        if 'payload_list' not in st.session_state and 'multi_uploaded_zip_instance' not in st.session_state:
            payload_list =None
            multi_uploaded_zip_instance =None
            payload_list, multi_uploaded_zip_instance = multi_upload_zip_file(operation, altruistic_chain_length)
            st.session_state.dup1 = payload_list
            st.session_state.dup2 = multi_uploaded_zip_instance

            if payload_list:
                st.info('File Uploaded.Begin Analysis.')


        if 'single_begin_analysis_butto' not in st.session_state:
            st.session_state.single_begin_analysis_butto = False
        single_begin_analysis_butto = st.button("Begin Analysis ")


    if (st.session_state.single_begin_analysis_butto or( single_begin_analysis_butto and st.session_state.dup2)):

         st.session_state.payload_list = st.session_state.dup1
         st.session_state.multi_uploaded_zip_instance = st.session_state.dup2
         multi_upload_data.empty()
         st.session_state.single_begin_analysis_butto = True

        #payload_list = (get4(multi_uploaded_zip_instance,operation, altruistic_chain_length))

         if 'recipients_list' not in st.session_state and 'kep_instance_list' not in st.session_state:
             for instance in multi_uploaded_zip_instance:

                recipients_list.append(instance['recipients'])
                kep_instance_list.append(instance['data'])
                st.session_state.recipients_list = recipients_list
                st.session_state.kep_instance_list = kep_instance_list

             with st.container():
                    col2, col3 = st.columns(2)
                    # col1.markdown(""" **_Uploaded File_** - """ + str(filename))
                    col2.markdown(""" **_Operation_ ** - """ + str(operation))
                    col3.markdown("""**_Altruistic Chain Length_** - """ + str(altruistic_chain_length))
         if 'recipients_list'  in st.session_state and 'kep_instance_list' in st.session_state:

            analysis(st.session_state.kep_instance_list,st.session_state.recipients_list,st.session_state.payload_list )

    elif (single_begin_analysis_butto and not multi_uploaded_zip_instance):
         st.error('No file uploaded! Refresh.')




def multi_upload_zip_file(operation, altruistic_chain_length):
    multi_uploaded_file = None
    instance = None
    payload_list = None
    cola, colb = st.columns([2,1])

    try:

        multi_uploaded_file = st.file_uploader("Choose a file : ", type = ['zip'], key = 'multi_file')

    except Exception as e:
        st.error("!!! Exception has occurred while multi_uploading the file try again, If Exception persists contact support." )
        st.error(e)


    if multi_uploaded_file is not None:
        try:
            instance = get_zip_contents(multi_uploaded_file)
            st.markdown(""" **Zip File Upload and Extracted Successfully. Total Number of files extracted - **""" + str(len(instance)))
            st.warning('File Uploading, Please Wait')
            payload_list = get_data_NHS_Optimal(instance,operation, altruistic_chain_length)
            #payload_list = ioloop.IOLoop.current().run_sync(get6(multi_uploaded_zip_instance,operation, altruistic_chain_length))

        except Exception as e:
            st.error("!!! Exception has occurred while fetching data from external API. Please wait or contact if issue persist!!" )
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

def get_operation_and_chain_length():
    col1, col2 =st.columns(2)
    with col1:
        operation = st.selectbox('Choose Operation : ',('optimal','maxcard','pairs'))
    with col2:
        altruistic_chain_length = st.selectbox('Choose Altruistic Chain Length :',('1','2'))

    return operation,altruistic_chain_length

#multithread Processing
def get3(session,kep_instance_obj):

    response = session.send(requests.Request('POST',kidney_exchange_allocator_url, data = kep_instance_obj ).prepare())
    payload =  response.json()

    return payload

def get4(multi_uploaded_zip_instance,operation,altruistic_chain_length ):
    #create an aiohttp session, to handle all the requests
    payload_list =[]
    instance_obj_list = []
    future_list = []
    for instance in multi_uploaded_zip_instance:

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
def get_data_NHS_Optimal(multi_uploaded_zip_instance,operation, altruistic_chain_length):
    length = len(multi_uploaded_zip_instance)
    rem = length % 50
    loops = (length-rem)//50
    payload_list = None
    final_payload_list = []

    k = 0
    b = 0
    a = 0

    if len(multi_uploaded_zip_instance) > 50:
        for i in range(0,loops):
            # st.write('---------beginning loop :' + str(i) +'----------')
            a = k+49
            sub_instances = []
            for j in range(k,a+1):
                sub_instances.append(multi_uploaded_zip_instance[j])
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
                sub_instances.append(multi_uploaded_zip_instance[i])
            st.write('length of sub list:', str(len(sub_instances)))
            payload_list = get4(sub_instances,operation,altruistic_chain_length )
            final_payload_list.extend(payload_list)

        return final_payload_list

    else:
        # st.write('---------List is less than 50----------')
        payload_list = get4(multi_uploaded_zip_instance,operation,altruistic_chain_length )
        return payload_list

def analysis(kep_instance_list,recipients_list,payload_list ):
        st.title("KEPIA")
        st.warning('Note: Refresh to upload New File!!')
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
            'Max No. of Matches':max_matches_list,
            'No. of Altruistic Donors':alt_list,
            'No. of Non Altruistic Donors':non_alt_list,
            'Donors with Multiple Sources':multiple_sources_l,
            'Average Age of Donors':avg_age_l,
            'Min Age of Donors':min_age_l,
            'Max Age of Donors':max_age_l,
            'Median Age of Donors':med_age_l,
            'A bloodtype Donors Count':a_type_l,
            'B bloodtype Donors Count':b_type_l,
            'O bloodtype Donors Count':o_type_l,
            'AB bloodtype Donors Count':ab_type_l,
            'Donors with No Matches': no_matches_list,
            'Min No. of Matches':min_matches_list,
            }

            donor_instances_df = pd.DataFrame(donor_instance_list_data)
            st.session_state.donor_instances_df = donor_instances_df

        donor_instances_df = st.session_state.donor_instances_df
        st.markdown("""#### Donor Data Analysis in Sets""")
        st. dataframe(donor_instances_df)

        st.markdown("""##### Accumulative Statistics of the Donors in the set""")
        x_d = donor_instances_df.copy()
        del x_d['Instance Id']
        st.dataframe(x_d.describe().iloc[[1,2,3,4,5,6,7]])


        with st.container():
            st.markdown("""##### 1. Distribution of No. of Donors in the set""")
            cola, colb = st.columns(2)
            with cola:
                b = donor_instances_df[['No. of Donors']].copy()
                st.dataframe(b.describe())
            with colb:
                a_3802 = b.copy()
                a_3802['Frequency in the Set'] = donor_instances_df['Instance Id'].copy()
                # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig = px.bar(a_3802, x="Frequency in the Set", y="No. of Donors",title = 'Donors Count distribution within set  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 17)

                st.plotly_chart(fig,use_container_width=True)

        with st.container():
            st.markdown("""##### 2. Distribution of Altruistic Donors in the set""")

            b1 = donor_instances_df[['No. of Altruistic Donors','No. of Non Altruistic Donors']].describe()
            st.dataframe(b1)
            colb1, colc1 = st.columns(2)
            with colb1:
                total = donor_instances_df['No. of Donors'].sum()
                sum = donor_instances_df['No. of Altruistic Donors'].sum()
                sum2 = donor_instances_df['No. of Non Altruistic Donors'].sum()
                aa = round(((sum)/total * 100),2)
                bb = round(((sum2)/total *100),2)

                values = [round(aa,2),round(bb,2)]
                labels = ['Altruistic\n' + str(aa) +'%','Non Altruistic\n '+ str(bb) +'%']
                fig1, ax1 = plt.subplots()
                ax1.pie(values, labels = labels, colors = ['#0077e6','#001a33'])
                st.write('Altruistic Donors Distribution in the set')
                st.pyplot(fig1,use_container_width=True)
            with colc1:
                fig = px.bar(donor_instances_df, x="Instance Id", y=["No. of Altruistic Donors", "No. of Non Altruistic Donors"],
                title="Accumulative Distribution of Altruistic Donors in instances",
                color_discrete_sequence = ['#0077e6','#001a33'])
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)

                st.plotly_chart(fig,use_container_width=True)


        with st.container():
            st.markdown("""##### 3. Distribution of Donor's Age in the set""")
            cola,colb = st.columns(2)
            with cola:
                b2 = donor_instances_df[[
                'Average Age of Donors',
                'Min Age of Donors',
                'Max Age of Donors',
                'Median Age of Donors']].describe()
                st.dataframe(b2)
            with colb:
                N = 100
                random_x = donor_instances_df['Instance Id']
                random_y0 = donor_instances_df['Average Age of Donors']
                random_y1 = donor_instances_df['Min Age of Donors']
                random_y2 = donor_instances_df['Max Age of Donors']

                # Create traces
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                                    mode='lines',
                                    name='Average Age of Donors',
                                    line = dict(color = '#001a33')))
                fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                                    mode='lines',
                                    name='Min Age of Donors',
                                    line = dict(color ='#0077e6')))
                fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                                    mode='lines', name='Max Age of Donors',
                                    line = dict(color = '#0059b3')))
                st.write('Age values distribution in the sets')
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            st.markdown("""##### 4. Matches Count Distribution of Donors in the set""")
            cola, colb = st.columns(2)
            with cola:
                b = donor_instances_df[['Avg No. of Matches','Max No. of Matches','Min No. of Matches']]
                st.dataframe(b.describe())
            with colb:

                # fig = px.histogram(b, x="Instance Id",y ="Avg No. of Matches",title = 'Recipients cPRA distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig = px.bar(donor_instances_df,
                x="Instance Id", y="Avg No. of Matches",title = 'Avg No. of Matches Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                with colb:
                    st.plotly_chart(fig, use_container_width=True)
        with st.container():
            st.markdown("""##### 5. Blood Type Distribution of Donors in the set""")


            b4 = donor_instances_df[[
            'A bloodtype Donors Count',
            'B bloodtype Donors Count','O bloodtype Donors Count','AB bloodtype Donors Count']].describe()
            st.dataframe(b4)
            colb5, colc5 = st.columns(2)
            with colb5:
                total = donor_instances_df['No. of Donors'].sum()
                a = round(donor_instances_df['A bloodtype Donors Count'].sum()/total * 100,3)
                b = round(donor_instances_df['B bloodtype Donors Count'].sum()/total * 100,3)
                c = round(donor_instances_df['O bloodtype Donors Count'].sum()/total * 100,3)
                d = round(donor_instances_df['AB bloodtype Donors Count'].sum()/total * 100,3)
                values = [a,b,c,d]
                labels = ['A -' + str(a) +'%','B - '+ str(b) +'%' ,'O -' + str(a) +'%','AB -'+ str(b) +'%']
                fig, ax = plt.subplots()
                ax.pie(values, labels = labels, colors = ['#0077e6','#0059b3','#003366','#001a33'])
                st.write('Distribution in the set')
                st.pyplot(fig)
            with colc5:
                fig = px.bar(donor_instances_df, x="Instance Id",
                 y=["A bloodtype Donors Count",
                  "B bloodtype Donors Count",
                  "O bloodtype Donors Count",
                  "AB bloodtype Donors Count"],
                title="Accumulative Distribution in instances",
                color_discrete_sequence = px.colors.sequential.Cividis)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                st.plotly_chart(fig, use_container_width=True)
        with st.container():
            st.markdown("""##### 6. Correlation of attributes in the Donor's set""")

            cola, colb = st.columns(2)
            with cola:
                cor = donor_instances_df[['No. of Donors','Avg No. of Matches','No. of Altruistic Donors',
                'No. of Non Altruistic Donors','Average Age of Donors','A bloodtype Donors Count',
                'B bloodtype Donors Count','O bloodtype Donors Count','AB bloodtype Donors Count'
                ]]

                corrMatrix = cor.corr()
                st.write('Correlation Matrix')

                st.dataframe(corrMatrix)

            with colb:
                 fig = plt.figure(figsize=(10, 4))
                 sn.heatmap(corrMatrix, annot = True)
                 st.write('Heatmap for Correlation Matrix')
                 st.pyplot(fig,use_container_width=True)
        with st.container():
            st.markdown("""##### 7. Correlation Between two Attributes""")

            cola8, colb8 = st.columns(2)
            with cola8:
                attributes = ['No. of Donors','Avg No. of Matches','No. of Altruistic Donors',
                'No. of Non Altruistic Donors','Average Age of Donors','A bloodtype Donors Count',
                'B bloodtype Donors Count','O bloodtype Donors Count','AB bloodtype Donors Count'
                ]
                with st.form('Select the Donor Attributes :'):

                    x_label = (st.selectbox("Select attribute for X Axis:",attributes, index = 0))
                    y_label = (st.selectbox("Select attribute for Y Axis:",attributes, index = 1))
                    submit_donor_filter = st.form_submit_button('Plot the Graph')
                    title = 'Correlation between ' + x_label + 'and' + y_label

            if(submit_donor_filter):
                    fig = px.scatter(donor_instances_df,x = donor_instances_df[x_label],
                    y = donor_instances_df[y_label],
                    title = title ,
                    color_discrete_sequence = px.colors.sequential.Cividis)
                    fig.update_layout(legend=dict(
                    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                    title_font_size= 15)
                    with colb8:
                        st.plotly_chart(fig, use_container_width=True)




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
        'Instance Id': instance_ids,
        'No. of Recipients':number_of_recipients_l,
        'No Compatible Donor count':non_compatible_l,
        'Has Compatible Donor count': compatible_l,
        'A bloodtype avg of Recipients' : a_l,
        'O bloodtype avg of Recipients': o_l,
        'B bloodtype avg of Recipients': b_l,
        'AB bloodtype avg of Recipients': ab_l,
        'cPRA mean' : cPRA_mean_l,
        'cPRA median' : cPRA_median_l,
        'cPRA std': cPRA_std_deviation_l
        }

        recipients_instances_fin_df = pd.DataFrame(recipients_instances_data)

        st.session_state.recipients_instances_fin_df = recipients_instances_fin_df

    recipients_instances_fin_df = st.session_state.recipients_instances_fin_df
    st.markdown("""#### Recipients Data Analysis in Sets""")
    st. dataframe(recipients_instances_fin_df)

    st.markdown("""#### Accumulative statistics of the set""")
    # index = ['No of Cycles','No of Two Cycles','No of Three Cycles', 'No of Short chains',
    #  'No of Long chains', 'weight Avg', 'weight Median','weight std','No of Cycles with backarcs']
    x = recipients_instances_fin_df.copy()
    del x['Instance Id']
    st.dataframe(x.describe().iloc[[1,2,3,4,5,6,7]])


    with st.container():
        st.markdown("""##### 1. Distribution of No. of Recipients in the set""")
        cola, colb = st.columns(2)
        with cola:
            b = recipients_instances_fin_df[['No. of Recipients']]
            st.dataframe(b.describe())
        with colb:
            a_3801 = b.copy()
            a_3801['Frequency in the Set'] = recipients_instances_fin_df['Instance Id'].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig = px.bar(a_3801, x="Frequency in the Set",
             y="No. of Recipients",
             title = 'Recipients Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.write('Distribution in the set')
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown("""##### 2. Distribution of Recipients compatibility in the set""")

        b1 = recipients_instances_fin_df[['No Compatible Donor count','Has Compatible Donor count']].describe()
        st.dataframe(b1)
        colb1, colc1 = st.columns(2)
        with colb1:
            total = recipients_instances_fin_df['No. of Recipients'].sum()
            sum = recipients_instances_fin_df['No Compatible Donor count'].sum()
            sum2 = recipients_instances_fin_df['Has Compatible Donor count'].sum()
            aa = round(((sum)/total * 100),2)
            bb = round(((sum2)/total *100),2)

            values = [round(aa,2),round(bb,2)]
            labels = ['No Compatible Donor\n' + str(aa) +'%',' Has Compatible Donor\n '+ str(bb) +'%']
            fig1, ax1 = plt.subplots()
            ax1.pie(values, labels = labels, colors = ['#0077e6','#001a33'])
            st.write('Distribution in the set')
            st.pyplot(fig1)
        with colc1:
            fig = px.bar(recipients_instances_fin_df, x="Instance Id", y=["No Compatible Donor count", "Has Compatible Donor count"],
            title="Accumulative Distribution in instances",
            color_discrete_sequence = ['#0077e6','#001a33'])
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.write('Distribution in the instances of set')
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown("""##### 3. Blood Type Distribution of Recipients in the set""")

        b6 = recipients_instances_fin_df[[
        'A bloodtype avg of Recipients',
        'O bloodtype avg of Recipients','B bloodtype avg of Recipients','AB bloodtype avg of Recipients']].describe()
        st.dataframe(b6)
        colb56, colc56 = st.columns(2)
        with colb56:
            total = recipients_instances_fin_df['No. of Recipients'].sum()
            a = round(recipients_instances_fin_df['A bloodtype avg of Recipients'].sum()/total * 100,3)
            b = round(recipients_instances_fin_df['O bloodtype avg of Recipients'].sum()/total * 100,3)
            c = round(recipients_instances_fin_df['B bloodtype avg of Recipients'].sum()/total * 100,3)
            d = round(recipients_instances_fin_df['AB bloodtype avg of Recipients'].sum()/total * 100,3)
            values = [a,b,c,d]
            labels = ['A -' + str(a) +'%','O - '+ str(b) +'%' ,'B -' + str(a) +'%','AB -'+ str(b) +'%']
            fig, ax = plt.subplots()
            ax.pie(values, labels = labels, colors = ['#0077e6','#0059b3','#003366','#001a33'])
            st.write('Distribution in the set')
            st.pyplot(fig)
        with colc56:
            fig = px.bar(recipients_instances_fin_df, x="Instance Id",
             y=[
             'A bloodtype avg of Recipients',
             'O bloodtype avg of Recipients','B bloodtype avg of Recipients','AB bloodtype avg of Recipients'],
            title="Accumulative Distribution in instances",
            color_discrete_sequence = px.colors.sequential.Cividis)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown("""##### 4. cPRA Distribution of Recipients in the set""")


        b2 = recipients_instances_fin_df[[
        'cPRA mean',
        'cPRA median',
        'cPRA std']].describe()
        st.dataframe(b2)
        cola,colb = st.columns(2)
        with cola:
            N = 100
            random_x = recipients_instances_fin_df['Instance Id']
            random_y0 = recipients_instances_fin_df['cPRA mean']
            random_y1 = recipients_instances_fin_df['cPRA median']
            random_y2 = recipients_instances_fin_df['cPRA std']

            # Create traces
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                                mode='lines',
                                name='cPRA mean',
                                line = dict(color = '#001a33')))
            fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                                mode='lines',
                                name='cPRA median',
                                line = dict(color ='#0077e6')))
            fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                                mode='lines', name='cPRA std',
                                line = dict(color = '#0059b3')))
            st.write('cPRA distribution in the sets')
            st.plotly_chart(fig, use_container_width=True)
        with colb:
            a_38010 = recipients_instances_fin_df.copy()
            a_38010['Instance Ids'] = recipients_instances_fin_df['Instance Id'].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig = px.bar(a_38010, x="Instance Ids",
             y="cPRA mean",
             title = 'Accumulative cPRA distribution in the instances  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)
    with st.container():
        st.markdown("""##### 6. Correlation of attributes in the Recipients's set""")

        cola, colb = st.columns(2)
        with cola:
            cor = recipients_instances_fin_df[['No. of Recipients','No Compatible Donor count','Has Compatible Donor count',
            'A bloodtype avg of Recipients','O bloodtype avg of Recipients','B bloodtype avg of Recipients',
            'AB bloodtype avg of Recipients','cPRA mean']]

            corrMatrix1 = cor.corr()
            st.write('Correlation Matrix1')

            st.dataframe(corrMatrix1)

        with colb:
             fig = plt.figure(figsize=(10, 4))
             sn.heatmap(corrMatrix1, annot = True)
             st.write('Heatmap for Correlation Matrix')
             st.pyplot(fig,use_container_width=True)

    with st.container():
        st.markdown("""##### 7. Correlation Between two Attributes""")

        cola8, colb8 = st.columns(2)
        with cola8:
            attributes = ['No. of Recipients','No Compatible Donor count','Has Compatible Donor count',
            'A bloodtype avg of Recipients','O bloodtype avg of Recipients','B bloodtype avg of Recipients',
            'AB bloodtype avg of Recipients','cPRA mean']

            with st.form('Select the Recipients Attributes  :'):

                x_label = (st.selectbox("Select attribute for X Axis:",attributes, index = 0))
                y_label = (st.selectbox("Select attribute for Y Axis:",attributes, index = 1))
                submit_donor_filter = st.form_submit_button('Plot Scatter plot')
                title = 'Correlation between ' + x_label + 'and' + y_label

            if(submit_donor_filter):
                    fig = px.scatter(recipients_instances_fin_df,x = recipients_instances_fin_df[x_label],
                    y = recipients_instances_fin_df[y_label],
                    title = title ,
                    color_discrete_sequence = px.colors.sequential.Cividis)
                    fig.update_layout(legend=dict(
                    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                    title_font_size= 15)
                    with colb8:
                        st.plotly_chart(fig, use_container_width=True)




def all_cycle_anlysis(payload_list):
        if payload_list in st.session_state:
            payload_list = st.session_state.payload_list
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
                'Instance Id' : instance_ids,
                'No. of Cycles' : no_of_cycles_l ,
                'No. of Two Cycles' : no_of_two_cycles ,
                'No. of Three Cycles' : no_of_three_cycles,
                'No. of Short chains' : no_of_short_chains_l ,
                'No. of Long chains' : no_of_long_chains_l ,
                'Weight Avg' : weight_avg_l ,
                'Weight Median' : weight_median_l ,
                'Weight std' : weight_std_l ,
                'No. of Cycles with backarcs' : cycles_with_backarcs_l
                }

            payload_fin_df = pd.DataFrame(payload_all_cycle_data)

            st.session_state.payload_fin_df = payload_fin_df
        payload_fin_df =  st.session_state.payload_fin_df
        st.markdown("""#### All cycles Analysis in Sets""")
        st. dataframe(payload_fin_df)
        st.markdown("""#### Accumulative statistics of the set""")
        index = ['No. of Cycles','No. of Two Cycles','No. of Three Cycles', 'No. of Short chains',
         'No. of Long chains', 'Weight Avg', 'Weight Median','Weight std','No. of Cycles with backarcs']
        st.dataframe(payload_fin_df.describe()[index].iloc[[1,2,3,4,5,6,7]])


        with st.container():
            st.markdown("""##### 1. Distribution of No. of Cycles in the set""")
            cola, colb = st.columns(2)
            with cola:
                b895= payload_fin_df[['No. of Cycles']]
                st.dataframe(b895.describe())
            with colb:
                a_38012 = b895.copy()
                a_38012['Frequency in the Set'] = payload_fin_df['Instance Id'].copy()
                # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig = px.bar(a_38012, x="Frequency in the Set",
                 y="No. of Cycles",
                 title = 'No. of cycles distribution in the Set ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            st.markdown("""##### 2. Weight Distribution of Cycles in the set""")

            b7 = payload_fin_df[[
            'Weight Avg',
            'Weight Median',
            'Weight std']].describe()
            st.dataframe(b7)
            cola,colb = st.columns(2)
            with cola:
                N = 100
                random_x = payload_fin_df['Instance Id']
                random_y0 = payload_fin_df['Weight Avg']
                random_y1 = payload_fin_df['Weight Median']
                random_y2 = payload_fin_df['Weight std']

                # Create traces
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                                    mode='lines',
                                    name='Weight Avg',
                                    line = dict(color = '#001a33')))
                fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                                    mode='lines',
                                    name='Weight Median',
                                    line = dict(color ='#0077e6')))
                fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                                    mode='lines', name='Weight std',
                                    line = dict(color = '#0059b3')))
                st.write('Weight distribution in the set')
                st.plotly_chart(fig, use_container_width=True)
            with colb:
                a_38010 = payload_fin_df.copy()
                a_38010['Instance Ids'] = payload_fin_df['Instance Id'].copy()
                # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig = px.bar(a_38010, x="Instance Ids",
                 y="Weight Avg",
                 title = 'Accumulative weight distribution in the instances  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            st.markdown("""##### 3. Cycle and chains Distribution in the set""")

            b6 = payload_fin_df[[
                'No. of Cycles',
                'No. of Two Cycles','No. of Three Cycles' ,'No. of Short chains' ,
                'No. of Long chains' ]]
            st.dataframe(b6)
            colb56, colc56 = st.columns(2)
            with colb56:
                total = payload_fin_df['No. of Cycles'].sum()
                a = round(payload_fin_df['No. of Two Cycles'].sum()/total * 100,3)
                b = round(payload_fin_df['No. of Three Cycles'].sum()/total * 100,3)
                c = round(payload_fin_df['No. of Short chains'].sum()/total * 100,3)
                d = round(payload_fin_df['No. of Long chains'].sum()/total * 100,3)
                values = [a,b,c,d]
                labels = ['2 Cycles -' + str(a) +'%','3 Cycles - '+ str(b) +'%' ,'Short Chains -' + str(a) +'%','Long Chains -'+ str(b) +'%']
                fig, ax = plt.subplots()
                ax.pie(values, labels = labels, colors = ['#0077e6','#0059b3','#003366','#001a33'])
                st.write('Distribution in the set')
                st.pyplot(fig)
            with colc56:
                fig = px.bar(payload_fin_df, x="Instance Id",
                 y=['No. of Two Cycles','No. of Three Cycles' ,'No. of Short chains' ,
                 'No. of Long chains'],
                title="Accumulative Distribution in instances",
                color_discrete_sequence = px.colors.sequential.Cividis)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            st.markdown("""##### 4. Correlation of attributes in the All cycles set""")

            cola, colb = st.columns(2)
            with cola:
                cor = payload_fin_df[
                ['No. of Cycles','No. of Two Cycles',
                'No. of Three Cycles',
                'No. of Short chains',
                'No. of Long chains',
                'Weight Avg']]

                corrMatrix1 = cor.corr()
                st.write('Correlation Matrix1')

                st.dataframe(corrMatrix1)

            with colb:
                 fig = plt.figure(figsize=(10, 4))
                 sn.heatmap(corrMatrix1, annot = True)
                 st.write('Heatmap for Correlation Matrix')
                 st.pyplot(fig,use_container_width=True)

        with st.container():
            st.markdown("""##### 5. Correlation Between two Attributes""")

            cola8, colb8 = st.columns(2)
            with cola8:
                attributes = ['No. of Cycles','No. of Two Cycles',
                'No. of Three Cycles',
                'No. of Short chains',
                'No. of Long chains',
                'Weight Avg']

                with st.form('Select the Cycles Attributes  :'):

                    x_label = (st.selectbox("Select attribute for X Axis:",attributes, index = 0))
                    y_label = (st.selectbox("Select attribute for Y Axis:",attributes, index = 1))
                    submit_donor_filter = st.form_submit_button('Plot the graph')
                    title = 'Correlation between ' + x_label + 'and' + y_label

            if(submit_donor_filter):
                    fig = px.scatter(payload_fin_df,x = payload_fin_df[x_label],
                    y = payload_fin_df[y_label],
                    title = title ,
                    color_discrete_sequence = px.colors.sequential.Cividis)
                    fig.update_layout(legend=dict(
                    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                    title_font_size= 15)
                    with colb8:
                        st.plotly_chart(fig, use_container_width=True)



def exchange_cycle_anlysis(payload_list):
    if payload_list in st.session_state:
        payload_list = st.session_state.payload_list
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
            'Instance Id' : instance_ids,
            'No. of Exchange Cycles' : no_exc_cycles,
            'Weight of Exchanges': weight_l,
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

    exchange_data_final_df = st.session_state.exchange_data_final_df
    st.markdown("""#### Exchange cycles Analysis in Sets""")
    st.markdown('Description:' +description)
    st. dataframe(exchange_data_final_df)
    st.markdown("""#### Accumulative statistics of the set""")
    index = ['No. of Exchange Cycles','Weight of Exchanges','Two - way echange', 'Three Way exchange',
     'Total Transplants', 'No. of two cyles', 'No. of three cycles','No. of short chains','No. of long chains', 'Cycle Containing Backarcs',
     'Avg weight of exc cycles']
    st.dataframe(exchange_data_final_df.describe()[index].iloc[[1,2,3,4,5,6,7]])

    with st.container():
        st.markdown("""##### 1. Distribution of No. of Exchange Cycles in the set""")
        cola, colb = st.columns(2)
        with cola:
            b895= exchange_data_final_df[['No. of Exchange Cycles']]
            st.dataframe(b895.describe())
        with colb:
            a_38012 = b895.copy()
            a_38012['Frequency in the Set'] = exchange_data_final_df['Instance Id'].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig = px.bar(a_38012, x="Frequency in the Set",
             y="No. of Exchange Cycles",
             title = 'No. of Exchange cycles distribution in the Set ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)
    with st.container():
        st.markdown("""##### 2. Distribution of No. of Total Transplants""")
        cola, colb = st.columns(2)
        with cola:
            b895= exchange_data_final_df[['Total Transplants']]
            st.dataframe(b895.describe())
        with colb:
            a_38012 = b895.copy()
            a_38012['Frequency in the Set'] = exchange_data_final_df['Instance Id'].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig = px.bar(a_38012, x="Frequency in the Set",
             y="Total Transplants",
             title = 'No. of Transplants distribution in the Set ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)
    with st.container():
        st.markdown("""##### 3. Weight Distribution of Exchanges in the set""")

        b7 = exchange_data_final_df[['Weight of Exchanges','Avg weight of exc cycles']].describe()
        # 'Weight Avg',
        # 'Weight Median',
        # 'Weight std']].describe()
        st.dataframe(b7)
        cola,colb = st.columns(2)
        with cola:
            N = 100
            random_x = exchange_data_final_df['Instance Id']
            random_y0 = exchange_data_final_df['Weight of Exchanges']
            random_y1 = exchange_data_final_df['Avg weight of exc cycles']
            # random_y2 = payload_fin_df['Weight std']
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                                mode='lines',
                                name='Weight of Exchanges',
                                line = dict(color = '#001a33')))
            fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                                mode='lines',
                                name='Avg weight of exc cycles',
                                line = dict(color ='#0077e6')))
            # fig.add_trace(go.Scatter(x=random_x, y=random_y2,
            #                     mode='lines', name='Weight std',
            #                     line = dict(color = '#0059b3')))
            st.write('Exchanges Weight distribution in the set')
            st.plotly_chart(fig, use_container_width=True)
        with colb:
            a_38010 = exchange_data_final_df.copy()
            a_38010['Instance Ids'] = exchange_data_final_df['Instance Id'].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig = px.bar(a_38010, x="Instance Ids",
             y="Weight of Exchanges",
             title = 'Accumulative Exchanges weight distribution in the instances  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)
    with st.container():
        st.markdown("""##### 4. Cycle and chains Distribution in the set""")
        b6 = exchange_data_final_df[[
            'No. of Exchange Cycles',
            'No. of two cyles','No. of three cycles' ,
            'No. of short chains' ,
            'No. of long chains' ]]
        st.dataframe(b6)
        colb56, colc56 = st.columns(2)
        with colb56:
            total = exchange_data_final_df['No. of Exchange Cycles'].sum()
            a = round(exchange_data_final_df['No. of two cyles'].sum()/total * 100,3)
            b = round(exchange_data_final_df['No. of three cycles'].sum()/total * 100,3)
            c = round(exchange_data_final_df['No. of short chains'].sum()/total * 100,3)
            d = round(exchange_data_final_df['No. of long chains'].sum()/total * 100,3)
            values = [a,b,c,d]
            labels = ['2 Cycles -' + str(a) +'%','3 Cycles - '+ str(b) +'%' ,'Short Chains -' + str(a) +'%','Long Chains -'+ str(b) +'%']
            fig, ax = plt.subplots()
            ax.pie(values, labels = labels, colors = ['#0077e6','#0059b3','#003366','#001a33'])
            st.write('Distribution in the set')
            st.pyplot(fig)
        with colc56:
            fig = px.bar(exchange_data_final_df, x="Instance Id",
             y=['No. of two cyles','No. of three cycles' ,'No. of short chains' ,
             'No. of long chains'],
            title="Accumulative Distribution in instances",
            color_discrete_sequence = px.colors.sequential.Cividis)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown("""##### 5. Correlation of attributes in the Exchange Cycle set""")

        cola, colb = st.columns(2)
        with cola:
            cor = exchange_data_final_df[[
            'No. of Exchange Cycles','Weight of Exchanges',
            'Two - way echange','Avg weight of exc cycles',
            'Three Way exchange','No. of two cyles','No. of three cycles',
            'Total Transplants','No. of short chains','No. of long chains']]

            corrMatrix1 = cor.corr()
            st.write('Correlation Matrix1')

            st.dataframe(corrMatrix1)

        with colb:
             fig = plt.figure(figsize=(10, 4))
             sn.heatmap(corrMatrix1, annot = True)
             st.write('Heatmap for Correlation Matrix')
             st.pyplot(fig,use_container_width=True)

    with st.container():
        st.markdown("""##### 6. Correlation Between two Attributes""")

        cola8, colb8 = st.columns(2)
        with cola8:
            attributes = [
            'No. of Exchange Cycles','Weight of Exchanges',
            'Two - way echange','Avg weight of exc cycles','Three Way exchange','No. of two cyles','No. of three cycles',
            'Three Way exchange','Total Transplants','No. of short chains','No. of long chains'
            'Weight Avg']

            with st.form('Select the Exchanges Attributes  :'):

                x_label = (st.selectbox("Select attribute for X Axis:",attributes, index = 0))
                y_label = (st.selectbox("Select attribute for Y Axis:",attributes, index = 1))
                submit_donor_filter = st.form_submit_button('Plot the Graph:')
                title = 'Correlation between ' + x_label + 'and' + y_label

        if(submit_donor_filter):
                fig = px.scatter(exchange_data_final_df,x = exchange_data_final_df[x_label],
                y = exchange_data_final_df[y_label],
                title = title ,
                color_discrete_sequence = px.colors.sequential.Cividis)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                with colb8:
                    st.plotly_chart(fig, use_container_width=True)









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
# def get_all_response_from_KAL(multi_uploaded_zip_instance,operation, altruistic_chain_length):
#     payload_list = []
#     a = []
#
#     for instance in multi_uploaded_zip_instance:
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





    #payload_list = get4(multi_uploaded_zip_instance,operation, altruistic_chain_length)


# @gen.coroutine
# def get6(multi_uploaded_zip_instance,operation,altruistic_chain_length ):
#     #create an aiohttp session, to handle all the requests
#     payload_list =[]
#     instance_obj_list = []
#     future_list = []
#     http_client = httpclient.AsyncHTTPClient()
#
#     for instance in multi_uploaded_zip_instance:
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
# async def get1(multi_uploaded_zip_instance,operation,altruistic_chain_length ):
#     #create an aiohttp session, to handle all the requests
#     payload_list =[]
#     i = 0
#     async with aiohttp.ClientSession() as session:
#         #create task: each individual requests
#         tasks = []
#         for instance in multi_uploaded_zip_instance:
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
