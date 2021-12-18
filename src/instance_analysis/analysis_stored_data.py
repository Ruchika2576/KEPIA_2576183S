import streamlit as st
import pandas as pd
import time

import plotly
import plotly.graph_objects as go
import seaborn as sn
import matplotlib.pyplot as plt
import plotly.express as px
from utils import constants as const
from sub_component_analysis import multiple_donor_analysis, multiple_recipient_analysis, multipl_all_cycle_analysis, multipl_exchange_cycle_analysis

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

    data_set = st.selectbox(const.select_set_message,const.set_options)

    if data_set:
        if 'data_set' not in st.session_state:
            st.session_state.data_set = data_set

        if st.session_state.data_set is not None:
            fetch_data(data_set)

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

def analysis_payload(payload_final_list_stored):
    if payload_final_list_stored in st.session_state:
        payload_final_list_stored = st.session_state.payload_final_list_stored
    payload_all_cycle_data_stored = None
    payload_fin_df_stored = None

    no_of_cycles_l = []
    no_of_two_cycles = []
    no_of_three_cycles = []
    no_of_short_chains_l = []
    no_of_long_chains_l = []
    weight_avg_l = []
    weight_median_l = []
    weight_std_l = []
    cycles_with_backarcs_l = []

    if 'payload_fin_df_stored' not in st.session_state:
        instance_ids = list(range(1, len(payload_final_list_stored)+1))

        for payload in payload_final_list_stored:
              no_of_cycles = 0
              no_two_cycles = 0
              no_three_cycles = 0
              no_of_short_chains = 0
              no_of_long_chains = 0
              weight_avg = 0
              weight_median = 0
              weight_std = 0

              all_cycles_dict = {}
              all_ids = []
              all_cycles = payload.get('output').get('all_cycles')
              k = 1
              for cycle in all_cycles:
                  if cycle is None:
                      continue
                  all_cycles_dict[str(k)] = cycle
                  all_ids.append(str(k))
                  k = k+1

              all_cycle_dataframe = pd.DataFrame(all_cycles_dict).T
              all_cycle_dataframe = all_cycle_dataframe.astype({'cycle': 'str' })
              all_cycle_dataframe = all_cycle_dataframe.astype({'altruistic' : 'str'})

              # all_ids = []
              # all_cycles = payload.get('output').get('all_cycles')
              # for i in all_cycles:
              #       all_ids.append(i)
              # all_cycle_dataframe = pd.DataFrame(all_cycles).T

              no_of_cycles = len(all_cycle_dataframe)



              cycle_2, cycle_3, s_chain, l_chain = calculate_cycles_chains(payload,all_ids)

              all_cycle_dataframe[const.sub_heading_8] = cycle_2
              all_cycle_dataframe[const.three_cycles] = cycle_3
              all_cycle_dataframe[const.sub_heading_10] = s_chain
              all_cycle_dataframe[const.long_chains] = l_chain

              no_two_cycles = all_cycle_dataframe[const.sub_heading_8].sum()
              no_three_cycles = all_cycle_dataframe[const.three_cycles].sum()
              no_of_short_chains = all_cycle_dataframe[const.sub_heading_10].sum()
              no_of_long_chains = all_cycle_dataframe[const.long_chains].sum()

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

        payload_all_cycle_data_stored = {
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

        payload_fin_df_stored= pd.DataFrame(payload_all_cycle_data_stored)

        st.session_state.payload_fin_df_stored= payload_fin_df_stored
    payload_fin_df_stored=  st.session_state.payload_fin_df_stored
    st.markdown(const.all_cycle_heading)
    st. dataframe(payload_fin_df_stored)
    st.markdown(const.horizontal_line)
    st.markdown(const.accumulative_all_cycle)
    index = ['No. of Cycles','No. of Two Cycles','No. of Three Cycles', 'No. of Short chains',
     'No. of Long chains', 'Weight Avg', 'Weight Median','Weight std','No. of Cycles with backarcs']

    st.dataframe(payload_fin_df_stored.describe()[index].iloc[[1,2,3,4,5,6,7]])


    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown("""##### 1. Distribution of No. of Cycles in the set""")
        cola, colb = st.columns(2)
        with cola:
            b895= payload_fin_df_stored[['No. of Cycles']]
            st.dataframe(b895.describe())
        with colb:
            a_38012 = b895.copy()
            a_38012['Frequency in the Set'] = payload_fin_df_stored['Instance Id'].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig = px.bar(a_38012, x="Frequency in the Set",
             y="No. of Cycles",
             title = 'No. of cycles distribution in the Set ' , color_discrete_sequence = px.colors.sequential.RdBu)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown("""##### 2. Weight Distribution of Cycles in the set""")

        b7 = payload_fin_df_stored[[
        'Weight Avg',
        'Weight Median',
        'Weight std']].describe()
        st.dataframe(b7)
        cola,colb = st.columns(2)
        with cola:
            N = 100
            random_x = payload_fin_df_stored['Instance Id']
            random_y0 = payload_fin_df_stored['Weight Avg']
            random_y1 = payload_fin_df_stored['Weight Median']
            random_y2 = payload_fin_df_stored['Weight std']

            # Create traces
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                                mode='lines',
                                name='Weight Avg',
                                line = dict(color = '#e64d00')))
            fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                                mode='lines',
                                name='Weight Median',
                                line = dict(color ='#cc0044')))
            fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                                mode='lines', name='Weight std',
                                line = dict(color = '#800040')))

            fig.update_layout(
            title='Weight distribution in the set',
            xaxis_title="Instance Id",
            yaxis_title="Weight values")
            st.plotly_chart(fig, use_container_width=True)
        with colb:
            a_38010 = payload_fin_df_stored.copy()
            a_38010['Instance Ids'] = payload_fin_df_stored['Instance Id'].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            fig = px.bar(a_38010, x="Instance Ids",
             y="Weight Avg",
             title = 'Accumulative weight distribution in the instances  ' , color_discrete_sequence = px.colors.sequential.RdBu)
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown("""##### 3. Cycle and chains Distribution in the set""")

        b6 = payload_fin_df_stored[[
            'No. of Cycles',
            'No. of Two Cycles','No. of Three Cycles' ,'No. of Short chains' ,
            'No. of Long chains' ]]
        st.dataframe(b6)
        colb56, colc56 = st.columns(2)
        with colb56:
            total = payload_fin_df_stored['No. of Cycles'].sum()
            a = round(payload_fin_df_stored['No. of Two Cycles'].sum()/total * 100,3)
            b = round(payload_fin_df_stored['No. of Three Cycles'].sum()/total * 100,3)
            c = round(payload_fin_df_stored['No. of Short chains'].sum()/total * 100,3)
            d = round(payload_fin_df_stored['No. of Long chains'].sum()/total * 100,3)
            values = [a,b,c,d]
            labels = ['2 Cycles -' + str(a) +'%','3 Cycles - '+ str(b) +'%' ,'Short Chains -' + str(a) +'%','Long Chains -'+ str(b) +'%']
            fig, ax = plt.subplots()

            wedges, texts, autotexts = ax.pie(values,
             colors = ['#ffbb99','#e64d00', '#cc0044','#800040'],
             autopct = '%1.1f%%',
             textprops={ 'color':'white'} )
            st.write('Distribution in the set')
            ax.legend(wedges, ['2 cycles','3 cycles',const.short_chains,const.long_chains],
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1), mode = 'expand')
            st.pyplot(fig,transparent = True)
        with colc56:
            fig = px.bar(payload_fin_df_stored, x="Instance Id",
             y=['No. of Two Cycles','No. of Three Cycles' ,'No. of Short chains' ,
             'No. of Long chains'],
            title="Accumulative Distribution in instances",
            color_discrete_map = {'No. of Two Cycles': '#ffbb99',
            'No. of Three Cycles': '#e64d00',
            'No. of Short chains': '#cc0044',
            'No. of Long chains': '#800040'
            })
            fig.update_layout(legend=dict(
            orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
            title_font_size= 15)
            st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown("""##### 4. Correlation of attributes in the All cycles set""")

        cola, colb = st.columns(2)
        with cola:
            cor = payload_fin_df_stored[
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
        st.markdown(const.horizontal_line)
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
                fig = px.scatter(payload_fin_df_stored,x = payload_fin_df_stored[x_label],
                y = payload_fin_df_stored[y_label],
                title = title ,
                color_discrete_sequence = px.colors.sequential.RdBu)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                with colb8:
                    st.plotly_chart(fig, use_container_width=True)

def analysis_exchanges(payload_final_list_stored):
        if payload_final_list_stored in st.session_state:
            payload_final_list_stored = st.session_state.payload_final_list_stored
        exchange_data_instances_stored = None
        exchange_data_final_df_stored = None
        description = payload_final_list_stored[0].get('output').get('exchange_data')[0].get('description')

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
        if 'exchange_data_final_df_stored' not in st.session_state:
                instance_ids = list(range(1, len(payload_final_list_stored)+1))

                for payload in payload_final_list_stored:
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
                            exchange_cycle_list.append(payload.get('output').get('all_cycles')[i])

                      exc_cycle_df = pd.DataFrame(exchange_cycle_list)


                      no_exc_cycles.append(len(exc_cycle_df))

                      cycle_2, cycle_3, s_chain, l_chain = calculate_cycles_chains(payload,exc_cycle_ids)
                      exc_cycle_df[const.sub_heading_8] = cycle_2
                      exc_cycle_df[const.three_cycles] = cycle_3
                      exc_cycle_df[const.sub_heading_10] = s_chain
                      exc_cycle_df[const.long_chains] = l_chain

                      no_of_two_cycles_l.append(exc_cycle_df[const.sub_heading_8].sum())
                      no_of_three_cycles_l.append(exc_cycle_df[const.three_cycles].sum())
                      no_of_short_chains_l.append(exc_cycle_df[const.sub_heading_10].sum())
                      no_of_long_chains_l.append(exc_cycle_df[const.long_chains].sum())

                      weight_avg_l.append(exc_cycle_df['weight'].mean())
                      weight_median_l.append(exc_cycle_df['weight'].median())
                      weight_std_l.append(exc_cycle_df['weight'].std())
                      cycles_with_backarcs_l.append(len(exc_cycle_df['backarcs'][exc_cycle_df['backarcs'] > 0]))


                exchange_data_instances_stored = {
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

                exchange_data_final_df_stored = pd.DataFrame(exchange_data_instances_stored)
                st.session_state.exchange_data_final_df_stored = exchange_data_final_df_stored

        exchange_data_final_df_stored = st.session_state.exchange_data_final_df_stored
        st.markdown(const.exchange_cycle_heading)
        st.markdown('Description:' +description)
        st. dataframe(exchange_data_final_df_stored)
        st.markdown(const.horizontal_line)
        st.markdown(const.all_cycle_accum)
        index = ['No. of Exchange Cycles','Weight of Exchanges','Two - way echange', 'Three Way exchange',
         'Total Transplants', 'No. of two cyles', 'No. of three cycles','No. of short chains','No. of long chains', 'Cycle Containing Backarcs',
         'Avg weight of exc cycles']
        st.dataframe(exchange_data_final_df_stored.describe()[index].iloc[[1,2,3,4,5,6,7]])

        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown("""##### 1. Distribution of No. of Exchange Cycles in the set""")
            cola, colb = st.columns(2)
            with cola:
                b895= exchange_data_final_df_stored[['No. of Exchange Cycles']]
                st.dataframe(b895.describe())
            with colb:
                a_38012 = b895.copy()
                a_38012['Frequency in the Set'] = exchange_data_final_df_stored['Instance Id'].copy()
                # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig = px.bar(a_38012, x="Frequency in the Set",
                 y="No. of Exchange Cycles",
                 title = 'No. of Exchange cycles distribution in the Set ' , color_discrete_sequence = px.colors.sequential.RdBu)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                st.plotly_chart(fig, use_container_width=True)
        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown("""##### 2. Distribution of No. of Total Transplants""")
            cola, colb = st.columns(2)
            with cola:
                b895= exchange_data_final_df_stored[['Total Transplants']]
                st.dataframe(b895.describe())
            with colb:
                a_38012 = b895.copy()
                a_38012['Frequency in the Set'] = exchange_data_final_df_stored['Instance Id'].copy()
                # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig = px.bar(a_38012, x="Frequency in the Set",
                 y="Total Transplants",
                 title = 'No. of Transplants distribution in the Set ' , color_discrete_sequence = px.colors.sequential.RdBu)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                st.plotly_chart(fig, use_container_width=True)
        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown("""##### 3. Weight Distribution of Exchanges in the set""")

            b7 = exchange_data_final_df_stored[['Weight of Exchanges','Avg weight of exc cycles']].describe()
            # 'Weight Avg',
            # 'Weight Median',
            # 'Weight std']].describe()
            st.dataframe(b7)
            cola,colb = st.columns(2)
            with cola:
                N = 100
                random_x = exchange_data_final_df_stored['Instance Id']
                random_y0 = exchange_data_final_df_stored['Weight of Exchanges']
                random_y1 = exchange_data_final_df_stored['Avg weight of exc cycles']
                # random_y2 = payload_fin_df_stored['Weight std']
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                                    mode='lines',
                                    name='Weight of Exchanges',
                                    line = dict(color = '#e64d00')))
                fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                                    mode='lines',
                                    name='Avg weight of exc cycles',
                                    line = dict(color ='#cc0044')))
                # fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                #                     mode='lines', name='Weight std',
                #                     line = dict(color = '#0059b3')))

                fig.update_layout(
                title='Exchanges Weight distribution in the set',
                xaxis_title="Instance Id",
                yaxis_title="Weight values")
                st.plotly_chart(fig, use_container_width=True)
            with colb:

                a_38010 = exchange_data_final_df_stored.copy()
                a_38010['Instance Ids'] = exchange_data_final_df_stored['Instance Id'].copy()
                # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
                fig = px.bar(a_38010, x="Instance Ids",
                 y="Weight of Exchanges",
                 title = 'Accumulative Exchanges weight distribution in the instances  ' , color_discrete_sequence = px.colors.sequential.RdBu)
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                st.plotly_chart(fig, use_container_width=True)
        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown("""##### 4. Cycle and chains Distribution in the set""")
            b6 = exchange_data_final_df_stored[[
                'No. of Exchange Cycles',
                'No. of two cyles','No. of three cycles' ,
                'No. of short chains' ,
                'No. of long chains' ]]
            st.dataframe(b6)
            colb56, colc56 = st.columns(2)
            with colb56:
                total = exchange_data_final_df_stored['No. of Exchange Cycles'].sum()
                a = round(exchange_data_final_df_stored['No. of two cyles'].sum()/total * 100,3)
                b = round(exchange_data_final_df_stored['No. of three cycles'].sum()/total * 100,3)
                c = round(exchange_data_final_df_stored['No. of short chains'].sum()/total * 100,3)
                d = round(exchange_data_final_df_stored['No. of long chains'].sum()/total * 100,3)
                values = [a,b,c,d]
                labels = ['2 Cycles -' + str(a) +'%','3 Cycles - '+ str(b) +'%' ,'Short Chains -' + str(a) +'%','Long Chains -'+ str(b) +'%']
                fig, ax = plt.subplots()
                wedges, texts, autotexts =ax.pie(values,
                colors = ['#ffbb99','#e64d00', '#cc0044','#800040'],
                autopct = '%1.1f%%',
                textprops={ 'color':'white'})
                st.write('Distribution in the set')
                ax.legend(wedges, ['2 cycles','3 cycles',const.sub_heading_10,const.long_chains],
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1), mode = 'expand')
                st.pyplot(fig,transparent = True)
            with colc56:
                fig = px.bar(exchange_data_final_df_stored, x="Instance Id",
                 y=['No. of two cyles','No. of three cycles' ,'No. of short chains' ,
                 'No. of long chains'],
                title="Accumulative Distribution in instances",
                color_discrete_map = {'No. of two cyle':'#ffbb99',
                'No. of three cycles':'#e64d00','No. of short chains':'#cc0044','No. of long chains':'#800040'}
                 )
                fig.update_layout(legend=dict(
                orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
                title_font_size= 15)
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown("""##### 5. Correlation of attributes in the Exchange Cycle set""")

            cola, colb = st.columns(2)
            with cola:
                cor = exchange_data_final_df_stored[[
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
            st.markdown(const.horizontal_line)
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
                    fig = px.scatter(exchange_data_final_df_stored,x = exchange_data_final_df_stored[x_label],
                    y = exchange_data_final_df_stored[y_label],
                    title = title ,
                    color_discrete_sequence = px.colors.sequential.RdBu )
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

      # st.write(str(int(i)-1))
      if i == 0:
          continue
      if i == len(payload.get('output').get('all_cycles')):
          break

      a = payload.get('output').get('all_cycles')[int(i)].get('cycle')
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







    #         donor_final_list.append(donors)
    # st.write(donor_final_list)
