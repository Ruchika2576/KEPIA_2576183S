
import streamlit as st
import pandas as pd
import json
import requests
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import plotly.express as px
from streamlit_vega_lite import vega_lite_component, altair_component
import plotly.graph_objects as go
import plotly


kidney_exchange_allocator_url = 'https://kidney-nhs.optimalmatching.com/kidney/find.json'

def app():
    st.title("KEPIA")
    main()

def main():
    kep_instance = None
    recipients = None
    payload = None

    if 'begin_analysis_button' not in st.session_state:
        st.session_state.begin_analysis_button = False

    upload_data = st.empty()
    with upload_data.container():
        st.markdown(""" ---Kidney Exchange Program Instance Analyser ---""")
        st.header("Single Instance Analysis")
        st.markdown("#### Data Upload : Upload an instance file for analysis")

        uploaded_instance, filename = upload_single_file()

        operation, altruistic_chain_length = get_operation_and_chain_length()

        begin_analysis_button = st.button("Begin Analysis ")

    if ( st.session_state.begin_analysis_button or (begin_analysis_button and uploaded_instance)):

        upload_data.empty()
        st.session_state.begin_analysis_button = True

        if 'payload' not in st.session_state:
            payload = get_response_from_KAL(uploaded_instance,operation, altruistic_chain_length)
            st.session_state.payload = payload

        if 'donors' not in st.session_state:
            donors = uploaded_instance['data']
            st.session_state.donors = donors


        if 'recipients' not in st.session_state:
            recipients = uploaded_instance['recipients']
            st.session_state.recipients = recipients


        with st.container():
            col1, col2, col3 = st.columns(3)
            col1.markdown(""" **_Uploaded File_** - """ + str(filename))
            col2.markdown(""" **_Operation_ ** - """ + str(operation))
            col3.markdown("""**_Altruistic Chain Length_** - """ + str(altruistic_chain_length))

            analysis(st.session_state.donors,st.session_state.recipients,st.session_state.payload )

    elif (begin_analysis_button and not uploaded_instance):
        st.error('No file uploaded')

def upload_single_file():
    uploaded_file = None
    instance = None
    filename = None
    try:
        uploaded_file = st.file_uploader("Choose a file : ", type = ['json'])

    except Exception as e:
        st.error("!!! Exception has occurred while uploading the file try again, If Exception persists contact support." )
        st.error(e)

    if uploaded_file is not None:
        filename = uploaded_file.name
        try:
            instance = json.loads(uploaded_file.getvalue().decode("utf-8"))
            if instance:
                st.info('File Upload Successful.')
        except Exception as e:
            st.error("!!! Exception has occurred while reading the file try again, If Exception persists contact support." )
            st.error(e)
    return instance, filename

def get_operation_and_chain_length():

    col1, col2 = st.columns(2)
    with col1:
        operation = st.selectbox('Choose Operation : ',('optimal','maxcard','pairs'))
    with col2:
        altruistic_chain_length = st.selectbox('Choose Altruistic Chain Length :',('1','2'))

    return operation,altruistic_chain_length


def get_response_from_KAL(instance, operation,altruistic_chain_length):
    #Extracting the json dictionary into KEP instances and recipients

    kep_instance = instance['data']
    recipients = instance['recipients']

    #Creating request params to call the Kidney Exchange allocator
    kep_instances_dict = {'data': kep_instance}

    kep_instance_obj  = {
    'operation': operation,
    'altruistic_chain_length': int(altruistic_chain_length),
    'data': json.dumps(kep_instances_dict)
    }

    try:
        response = requests.post(kidney_exchange_allocator_url, data = kep_instance_obj)
    except Exception as exc:
        st.error('Error ocurred while fetching data from https://kidney-nhs.optimalmatching.com/' )
        st.error(exc)

    if response.status_code == 200:
        payload = response.json()
    else:
        st.error(f"Request returned: {response.status_code} : '{response.reason}'")
        raise RuntimeError('Error in Response from https://kidney-nhs.optimalmatching.com/')


    return payload


def analysis(instance, recipients, payload):
    with st.expander('Analyse Donors in the instance'):
        donor_data_analysis(instance)
    with st.expander('Analyse Recipients in the instance'):
        recipient_data_analysis(recipients)
    with st.expander('Analyse All Cycles of the instance'):
        all_cycle_anlysis(instance, recipients, payload)
    with st.expander('Analyse Exchange Cycle of the instance'):
        exchange_cycle_anlysis(instance, recipients, payload)


def donor_data_analysis(instance):
    donors = pd.DataFrame(instance).T
    donors = donors.astype({'sources': 'str' })
    donors.astype( {'matches': 'str'})
    # donors.loc[donors.altruistic == np.NaN , "altruistic"] = "No"
    donors['altruistic'][donors['altruistic'] == np.NaN] = 'No'
    x = None

    donors['Matches Count'] = donors.apply(lambda row: (count_matches(row)) ,axis = 1)

    st.markdown(""" #### Donor Data Analysis
    """)

    sub = (donors[['sources','dage','matches','Matches Count','bloodtype']]).copy()
    #st.write('Non Altruistic Donors (Click on the headers to sort columns)')
    sub.astype( {'matches': str})
    st.dataframe(sub)
    # st.dataframe(sub.apply([donors['altruistic'].isnull()]))
    # st.write('Altruistic Donors ')
    # st.dataframe(sub[donors['altruistic'] == True ])
    # sub['altruistic'][sub['altruistic'].isnull()] = None
    # st.dataframe(sub['altruistic'].astype(str))
    # st.dataframe(sub['altruistic'].fillna(" "))
    # sub.apply(lambda x: x!=x)




    total = (donors.shape[0])
    alt_donors = str(donors.shape[0] - donors['altruistic'].isnull().sum())
    non_alt_donors = str(donors['altruistic'].isnull().sum())
    no_matches = str(donors['matches'].isnull().sum())

    d = pd.DataFrame(instance)
    x = d.T['sources'].value_counts(dropna = 'True')
    y = x.where(x > 1).value_counts(dropna = 'True')
    multiple_donors_count = y.to_dict()
    k = list(multiple_donors_count.keys())
    v = list(multiple_donors_count.values())

    two_donors = x.index[x == 2] #list
    three_donors = x.index[x == 3]
    four_donors = x.index[x == 4]
    non_alt_list = donors.index[donors['altruistic'] == True]
    no_matches_list = donors.index[donors['Matches Count'] == 0]

    # for i in a:
    #     st.write(str(i))

    multiple_total = 0
    for i in range(len(v)):
        multiple_total = multiple_total + int(v[i] )

    with st.container():
        st.markdown(""" ###### 1. Total No. of Donors : """  + str(total ))

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(""" ###### 2. Donors with no matches : """ + no_matches  + ' , Donor Ids :' + (",".join(no_matches_list)) )

            # show1 = st.checkbox("Click to expand Donor ids ")
            # if show1:

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(""" ###### 3. Altruistic donors count : """ + alt_donors)
        with st.container():
            st.dataframe(sub[donors['altruistic'] == True ])
            # show2 = st.checkbox("Click to expand Donor ids")
            # if show2:


        col1, col2 = st.columns(2)
        with col1:
            st.markdown(""" ###### 5. Sources with multiple Donors : """ + str(multiple_total) )
            for i in range(len(k)):
                st.markdown( str(v[i]) + ' Sources' +' with ' + str(int(k[i] ))+ ' Donors. ' )
        with col2:
            # show3 = st.checkbox("Click to expand Source ids")
            # if show3:
                a = []
                for i in two_donors:
                    a.append(i)
                if(len(a) != 0):
                    st.write("Two donors: " + str(a))
                b = []
                for i in three_donors:
                    b.append(i)
                if(len(b) != 0):
                    st.write("Three donors: "+ str(b) )
                c = []
                for i in four_donors:
                    c.append(i)
                if(len(c) != 0):
                    st.write("Four donors: "+ str(c) )


    with st.container():

        st.markdown(""" ###### 6. Info about specific Donors(only non altruistic) - """)
        selected_indices = st.multiselect('Select Donor Ids:', donors.index)

        for i in selected_indices:
            i = int(i)
            x = sub.iloc[i]


            render_donor(x,i,donors)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(""" ###### 7. Donor age Statistics : """ )
    # with col2:
    #     show7 = st.checkbox('Click to expand:')
    # if show7:

        with col1:
           # st.write((recipients['cPRA']).describe())
           des = pd.to_numeric(donors['dage']).describe().to_dict()
           des['median'] = donors['dage'].median()
           st.dataframe(list(des.items()))


        with col2:

            a = donors.copy()
            a1 = a['dage'].value_counts().to_dict()
            a['Donors Count'] = a['dage'].map(a1)


            p = alt.Chart(a, title = 'Donor Age Distribution').mark_bar().encode(
            x = 'dage',
            y = 'Donors Count',
            tooltip = ['dage','Donors Count']
            )

            p = p.properties(
             width = alt.Step(80)
            )
            st.write(p)



        #interactive dataframe
        # hist_data = pd.DataFrame(np.random.normal(42, 10, (200, 1)), columns=["x"])


        # brushed = alt.selection_interval(encodings=["x"], name="brushed")
        # a = alt.Chart(hist_data).mark_bar().encode(alt.X("x:Q", bin=True), y="count()").add_selection(brushed)
        # event_dict = altair_component(altair_chart=a)
        #
        # r = event_dict.get("x")
        # if r:
        #     filtered = hist_data[(hist_data.x >= r[0]) & (hist_data.x < r[1])]
        #     st.write(filtered)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(""" ###### 8. Donor's Blood type Distribution - """ )
    # with col2:
    #     show8 = st.checkbox('Click to expand')
    # if show8:

    with st.container():

        btvalues = donors['bloodtype'].value_counts().rename('Donor counts')

        st.write(pd.DataFrame(btvalues).T)

        fig = px.pie(donors,  names = 'bloodtype',title = 'Donor blood type distribution (hover to see the bloodtype)' , color_discrete_sequence = px.colors.sequential.Cividis)
        fig.update_layout(legend=dict(
        orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        title_font_size= 13)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
         st.markdown(""" ###### 9. Donor Matches Count Statistics : """ )
    # with col2:
    #      show8 = st.checkbox('Click to expand :')
    # if show8:
    with col1:
        a = donors.copy()
        a1 = a['Matches Count'].value_counts().to_dict()
        a['Frequency'] = a['Matches Count'].map(a1)
        # st.write((recipients['cPRA']).describe())
        des = pd.to_numeric(donors['Matches Count']).describe().to_dict()
        des['median'] = donors['Matches Count'].median()
        st.dataframe(list(des.items()))
    with col2:
        p = alt.Chart(a, title = 'Matches count Distribution').mark_bar().encode(
        x = 'Matches Count',
        y = 'Frequency',
        tooltip = ['Matches Count','Frequency']
        )

        p = p.properties(
         width = alt.Step(80)
        )
        st.write(p)


    # a =  donors.apply(lambda row: (count_matches(row)) ,axis = 1)
    # c = donors.copy()
    # c['counts'] = a
    #
    # mx = c.iloc[c['counts'].argmax()]
    # mn = c.iloc[c['counts'].argmin()]
    #
    # st.write('Donor with maximum matches: \n')
    # st.write('------------------')
    # st.write(str(mx))
    # st.write('Donors with minimum number of matches:',  )
    # st.write('------------------')
    # st.write(str(mn))




def recipient_data_analysis(recipients):

   recipients = pd.DataFrame(recipients).T

   st.header('----------Recipients Data Analysis------------')
   st.write(recipients)
   total = (recipients.shape[0])

   with st.container():
        st.markdown(""" ###### 1. Total No. of Recipients : """  + str(total ))

        # st.markdown(""" ###### 4. Recipients's blood Statistics : """ )
        # with st.container():
        #    st.write(recipients.describe()['bloodtype'])
           # des = pd.to_numeric(recipients['bloodtype']).describe().to_dict()

           # st.dataframe(list(des.items()))
   col1, col2 = st.columns(2)
   with col1:
        st.markdown(""" ###### 2. Recipients's Blood type Distribution : """ )
  # with col2:
   #      show9 = st.checkbox('Click to expand     ')
   # if show9:
   with st.container():

       btvalues = recipients['bloodtype'].value_counts().rename('Recipients counts')

       st.write(pd.DataFrame(btvalues).T)

       fig = px.pie(recipients,  names = 'bloodtype',title = 'Recipients blood type distribution (hover to see the bloodtype)' , color_discrete_sequence = px.colors.sequential.Cividis)
       fig.update_layout(legend=dict(
       orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
       title_font_size= 13)
       st.plotly_chart(fig, use_container_width=True)

    # st.markdown(""" ###### 4. Recipients's blood Statistics : """ )
    # with st.container():
    #   st.write(recipients.describe()['hasBloodCompatibleDonor'])
   col1, col2 = st.columns(2)
   with col1:
         st.markdown(""" ###### 3. Recipients's Donor Compatibility Distribution : """ )
   # with col2:
   #       show10 = st.checkbox('Click to expand ')
   # if show10:

   with st.container():
        values = recipients['hasBloodCompatibleDonor'].value_counts().rename('Has Compatible Donor ')

        st.write(pd.DataFrame(values).T)
        fig = px.pie(recipients,  names = 'hasBloodCompatibleDonor',title = 'Recipients Donor Compatibility distribution ' , color_discrete_sequence = px.colors.sequential.Cividis)
        fig.update_layout(legend=dict(
        orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        title_font_size= 13)
        st.plotly_chart(fig, use_container_width=True)

   col1, col2 = st.columns(2)
   with col1:
         st.markdown(""" ###### 4. Recipients's cPRA Statistics : """ )

   with st.container():
        # st.write((recipients['cPRA']).describe())
        des = pd.to_numeric(recipients['cPRA']).describe().to_dict()
        des['median'] = recipients['cPRA'].median()
        st.dataframe(list(des.items()))

        fig = px.histogram(recipients, x="cPRA",title = 'Recipients cPRA distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
        fig.update_layout(legend=dict(
        orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
        title_font_size= 13)
        st.plotly_chart(fig, use_container_width=True)



def exchange_cycle_anlysis(instance, recipients, payload):
    st.header('----------Exchange Cycle Analysis------------')
    e = payload.get('output').get('exchange_data')[0]
    keys = e.keys()
    values = e.values()
    i = 1

    with st.container():
        st.markdown( """ ######  Exchange Data: """)
        for k in keys:

            st.write( str(i) +str('. ')+ str(k) +'  :    ' + str(e.get(k) ) )
            i = i+1



        st.markdown( """ ######  Summary of exchange cycles: """+str('(Scroll right)'))
        exc = []
        ids =[]
        all = payload.get('output').get('all_cycles')
        for i in e.get('exchanges'):
            ids.append(str(i))
            exc.append(payload.get('output').get('all_cycles').get(str(i)))
        # st.write(type(payload.get('output').get('all_cycles').get(str('1'))))
        # st.write(exc)
        # st.write(payload.get('output').get('all_cycles').get(str('1')))
        cycle_2, cycle_3, s_chain, l_chain = calculate_cycles_chains(payload,ids)

        df = pd.DataFrame(exc)
        df['Two cycles'] = cycle_2
        df['Three cycles'] = cycle_3
        df['Short Chains'] = s_chain
        df['Long Chains'] = l_chain
        df.insert(0,'cycle Id',ids)
        st.dataframe(df)
        total = len(df)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(""" ###### Total No. of Cycles: """ + str(total))
            st.markdown(""" ###### 1. Cycles - """)
            st.markdown("""  Total no. of 2 cycles - """ + str(df['Two cycles'].sum()))
            st.markdown("""  Total no. of 3 cycles - """ + str(df['Three cycles'].sum()))
            show12 = st.checkbox('       Click to see the distrbution of cylces and chains. ')

        with col2:
            show_exchanges = st.checkbox("""Click to see all Exchange cycles""")
            st.markdown(""" ###### 2. Chains - """)
            st.markdown("""  Total no. of short chains - """ + str(df['Short Chains'].sum()))
            st.markdown("""  Total no. of long chains - """ + str(df['Long Chains'].sum()))
            # st.markdown("""" Cycles with alternatives - """ + str(df['alt'][len(df['alt']) > 2].sum()))
        if show12:
            a = round(df['Two cycles'].sum()/total * 100,3)
            b = round(df['Three cycles'].sum()/total *100,3)
            c = round(df['Short Chains'].sum()/total * 100,3)
            d = round(df['Long Chains'].sum()/total * 100,3)
            labels = ['2 cycles ' + str(a) +'%','3 cycles '+ str(b) +'%','short chains ' + str(c) +'%','long chains '+ str(d) +'%']
            values = [round(a,2),round(b,2),round(c,2),round(d,2)]
            fig, ax = plt.subplots()
            ax.pie(values, labels = labels, colors = ['#0077e6','#0059b3','#003366','#001a33'])
            st.pyplot(fig)

        showa =st.checkbox('Click to see weight distribution in Exchange cycles')
        showb = st.checkbox('Click to see backarc distribution in Exchange cycles')

        if showa:
            col1, col2 = st.columns(2)
            with col1:
                  st.markdown(""" ######  Exchange Cycle Weight Statistics : """ )
            with st.container():
            #       show12 = st.checkbox('  Click to expand     ')
            # if show12:

                 des = pd.to_numeric(df['weight']).describe().to_dict()
                 des['median'] = df['weight'].median()
                 st.dataframe(list(des.items()))

                 fig = px.histogram(df, x="weight",title = 'Exchange Cycle Weight distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                 fig.update_layout(legend=dict(
                 orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                 title_font_size= 13)
                 st.plotly_chart(fig, use_container_width=True)

        if showb:
            col1, col2 = st.columns(2)
            with col1:
                  st.markdown(""" ###### Backarcs in Exchange Data : """ )
            with st.container():
            #       show13 = st.checkbox('           Click to expand     ')
            # if show13:

                    values = df['backarcs'].value_counts().rename('Cycles Backarcs distribution ')
                    st.write(values.T)

                    fig = px.pie(df,  names = 'backarcs',title = 'Exchange Cycles Backarcs distribution' , color_discrete_sequence = px.colors.sequential.Cividis)
                    fig.update_layout(legend=dict(
                    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                    title_font_size= 13)
                    st.plotly_chart(fig, use_container_width=True)



    with st.container():
        st.markdown( """ *** """)
        if show_exchanges:

            col = []
            val = []

            for k in e.keys():
                col.append(k)

            for v in e.values():
                val.append(str(v))

            for i in e.get('exchanges'):
              a = payload.get('output').get('all_cycles').get(str(i)).get('cycle')
              df = pd.DataFrame(a)
              c2,c3,sc,lc,type = per_cycle(df)
              st.markdown("""**-----------Cycle:  **"""+ str(i) )
              st.markdown(type)
              st.write(df)



def all_cycle_anlysis(instance, recipients, payload):
    st.header('----------All Cycles Analysis------------')
    # e = payload.get('output').get('exchange_data')[0]

    with st.container():
            # a = 'a b c d \n 2 3 4 5 '
            all_ids = []
            all = payload.get('output').get('all_cycles')
            for i in all:
                all_ids.append(i)

            # st.markdown(type(all))
            df = pd.DataFrame(all).T
            # a = st.markdown("**Ruchika**")
            # l = [(a)] * len(all)
            # df.insert(1,"cycles",l)
            df = df.astype({'cycle': 'str' })
            df = df.astype({'alt' : 'str'})
            cycle_2, cycle_3, s_chain, l_chain = calculate_cycles_chains(payload,all_ids)
            df['Two cycles'] = cycle_2
            df['Three cycles'] = cycle_3
            df['Short Chains'] = s_chain
            df['Long Chains'] = l_chain
            st.dataframe(df)
    total = len(df)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(""" ###### Total No. of Cycles: """ + str(total))
        st.markdown(""" ###### 1. Cycles - """)
        st.markdown("""  Total no. of 2 cycles - """ + str(df['Two cycles'].sum()))
        st.markdown("""  Total no. of 3 cycles - """ + str(df['Three cycles'].sum()))
        show12 = st.checkbox('       Click to see the distrbution ')

    with col2:
        st.markdown(""" ###### 2. Chains - """)
        st.markdown("""  Total no. of short chains - """ + str(df['Short Chains'].sum()))
        st.markdown("""  Total no. of long chains - """ + str(df['Long Chains'].sum()))

    if show12:
        a = round(df['Two cycles'].sum()/total * 100,3)
        b = round(df['Three cycles'].sum()/total *100,3)
        c = round(df['Short Chains'].sum()/total * 100,3)
        d = round(df['Long Chains'].sum()/total * 100,3)
        labels = ['2 cycles ' + str(a) +'%','3 cycles '+ str(b) +'%','short chains ' + str(c) +'%','long chains '+ str(d) +'%']
        values = [round(a,2),round(b,2),round(c,2),round(d,2)]
        fig, ax = plt.subplots()
        ax.pie(values, labels = labels, colors = ['#0077e6','#0059b3','#003366','#001a33'])
        st.pyplot(fig)
        # st.plotly_chart(fig)

    st.markdown(""" ###### 3. Expand specific Cycles - """)
    selected_indices = st.multiselect('Select Cycle Ids:', df.index)
    col1,col2 = st.columns([2,1])
    for i in selected_indices:

        a = payload.get('output').get('all_cycles').get(str(i)).get('cycle')
        df = pd.DataFrame(a)
        c2,c3,sc,lc,type = per_cycle(df)
        with col1:
            st.markdown("""**-----------Cycle:  **"""+ str(i) )
            st.markdown(type)
            st.write(df)
    col1, col2 = st.columns(2)
    with col1:
          st.markdown(""" ###### 4. Cycle Weight Statistics : """ )
    with st.container():
    #       show12 = st.checkbox('  Click to expand     ')
    # if show12:

         des = pd.to_numeric(df['weight']).describe().to_dict()
         des['median'] = df['weight'].median()
         st.dataframe(list(des.items()))

         fig = px.histogram(df, x="weight",title = 'Cycle Weight distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
         fig.update_layout(legend=dict(
         orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
         title_font_size= 13)
         st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
          st.markdown(""" ###### 5. Backarcs : """ )
    with st.container():
    #       show13 = st.checkbox('           Click to expand     ')
    # if show13:

            values = df['backarcs'].value_counts().rename('Cycles Backarcs distribution ')
            st.write(values.T)

            fig = px.pie(df,  names = 'backarcs',title = 'Cycles Backarcs distribution' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 13)
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


def count_matches(row):
  if isinstance((row['matches']), list) :
    return int(len(row['matches']))
  else:
    return 0

def render_donor(x,i, donors):
    a,b,c, = st.columns([1,1,2])
    with a:
        st.markdown(""" ##### **Donor -- **""" + str(i))
        st.markdown(""" **Source : ** """ + str(x['sources']))
        st.markdown(""" **dage : ** """ + str(x['dage']))

    with b:
        st.markdown(""" **BloodType : ** """ + str(x['bloodtype']))
        st.markdown(""" **altruistic : ** """ + str(x['altruistic']))
        st.markdown(""" **Matches Count : ** """ + str(x['Matches Count']))
    with c:
        st.write('Matches ')
        st.dataframe(donors['matches'].iloc[i], width = 300, height = 170)
