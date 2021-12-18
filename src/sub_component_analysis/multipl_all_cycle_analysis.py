import streamlit as st
import pandas as pd
import numpy as np
from utils import constants as const
from utils import sub_component_utils
from utils import visualisation_utils as viz
# This module calculates multiple analysis on all cycles

# This function prepares data for multiple files uploaded, after preparing the the dataframe, the dataframe is further sent for analysis
def analysis_multiple_payload(payload_list,session_state_name):
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


    if session_state_name not in st.session_state:
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
              all_cycles = payload.get(const.output).get(const.all_cycles)
              for i in all_cycles:
                    all_ids.append(i)
              all_cycle_dataframe = pd.DataFrame(all_cycles).T
              all_cycle_dataframe = all_cycle_dataframe.astype({const.cycle: 'str' })
              all_cycle_dataframe = all_cycle_dataframe.astype({const.alt : 'str'})

              no_of_cycles = len(all_cycle_dataframe)

              cycle_2, cycle_3, s_chain, l_chain = sub_component_utils.calculate_cycles_chains(payload,all_ids)

              all_cycle_dataframe[const.two_cycles] = cycle_2
              all_cycle_dataframe[const.three_cycles] = cycle_3
              all_cycle_dataframe[const.short_chains] = s_chain
              all_cycle_dataframe[const.long_chains] = l_chain

              no_two_cycles = all_cycle_dataframe[const.two_cycles].sum()
              no_three_cycles = all_cycle_dataframe[const.three_cycles].sum()
              no_of_short_chains = all_cycle_dataframe[const.short_chains].sum()
              no_of_long_chains = all_cycle_dataframe[const.long_chains].sum()

              weight_avg = all_cycle_dataframe[const.weight].mean()
              weight_median = all_cycle_dataframe[const.weight].median()
              weight_std = all_cycle_dataframe[const.weight].std()
              cycles_with_backarcs = len(all_cycle_dataframe[const.backarcs][all_cycle_dataframe[const.backarcs] > 0])

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
            const.instance_id : instance_ids,
            const.cycle_count : no_of_cycles_l ,
            const.Two_cycle_count : no_of_two_cycles ,
            const.Three_cycle_count : no_of_three_cycles,
            const.sc_count : no_of_short_chains_l ,
            const.lc_count : no_of_long_chains_l ,
            const.avg_weight : weight_avg_l ,
            const.med_weight : weight_median_l ,
            const.std_weight : weight_std_l ,
            const.back_count : cycles_with_backarcs_l
            }

        payload_fin_df = pd.DataFrame(payload_all_cycle_data)
        st.session_state[session_state_name] = payload_fin_df
    payload_fin_df =  st.session_state[session_state_name]
    analysis_payload(payload_fin_df)

# This function prepares data for the stored sets, after preparing the the dataframe, the dataframe is further sent for analysis
def analysis_stored_payload(payload_final_list_stored,session_state_name):
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

    if session_state_name not in st.session_state:
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
              all_cycles = payload.get(const.output).get(const.all_cycles)
              k = 1
              for cycle in all_cycles:
                  if cycle is None:
                      continue
                  all_cycles_dict[str(k)] = cycle
                  all_ids.append(str(k))
                  k = k+1

              all_cycle_dataframe = pd.DataFrame(all_cycles_dict).T
              all_cycle_dataframe = all_cycle_dataframe.astype({const.cycle: 'str' })
              all_cycle_dataframe = all_cycle_dataframe.astype({const.altruistic : 'str'})

              # all_ids = []
              # all_cycles = payload.get(const.output).get(const.all_cycles)
              # for i in all_cycles:
              #       all_ids.append(i)
              # all_cycle_dataframe = pd.DataFrame(all_cycles).T

              no_of_cycles = len(all_cycle_dataframe)
              cycle_2, cycle_3, s_chain, l_chain = sub_component_utils.calculate_cycles_chains_stored(payload,all_ids)

              all_cycle_dataframe[const.two_cycles] = cycle_2
              all_cycle_dataframe[const.three_cycles] = cycle_3
              all_cycle_dataframe[const.sub_heading_10] = s_chain
              all_cycle_dataframe[const.long_chains] = l_chain

              no_two_cycles = all_cycle_dataframe[const.two_cycles].sum()
              no_three_cycles = all_cycle_dataframe[const.three_cycles].sum()
              no_of_short_chains = all_cycle_dataframe[const.sub_heading_10].sum()
              no_of_long_chains = all_cycle_dataframe[const.long_chains].sum()

              weight_avg = all_cycle_dataframe[const.weight].mean()
              weight_median = all_cycle_dataframe[const.weight].median()
              weight_std = all_cycle_dataframe[const.weight].std()
              cycles_with_backarcs = len(all_cycle_dataframe[const.backarcs][all_cycle_dataframe[const.backarcs] > 0])

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
            const.instance_id : instance_ids,
            const.cycle_count : no_of_cycles_l ,
            const.Two_cycle_count : no_of_two_cycles ,
            const.Three_cycle_count : no_of_three_cycles,
            const.sc_count : no_of_short_chains_l ,
            const.lc_count : no_of_long_chains_l ,
            const.avg_weight : weight_avg_l ,
            const.med_weight : weight_median_l ,
            const.std_weight : weight_std_l ,
            const.back_count : cycles_with_backarcs_l
            }

        payload_fin_df_stored= pd.DataFrame(payload_all_cycle_data_stored)

        st.session_state[session_state_name]= payload_fin_df_stored
    payload_fin_df_stored=  st.session_state[session_state_name]
    analysis_payload(payload_fin_df_stored)

# Here the actual analysis takes place
def analysis_payload(final_payload_df):

    st.markdown(const.all_cycle_heading)
    st. dataframe(final_payload_df)
    st.markdown(const.horizontal_line)
    st.markdown(const.accumulative_all_cycle)
    index = [const.cycle_count,const.Two_cycle_count,const.Three_cycle_count, const.sc_count,
     const.lc_count, const.avg_weight, const.med_weight,const.std_weight,const.back_count]

    # displaying the all cycles dataframe
    st.dataframe(final_payload_df.describe()[index].iloc[[1,2,3,4,5,6,7]])

    # Each analysis is breakdown and presented inside a container
    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_14)
        cola, colb = st.columns(2)
        with cola:
            sub_b= final_payload_df[[const.cycle_count]]
            st.dataframe(sub_b.describe())
        with colb:
            sub_b1 = sub_b.copy()
            sub_b1[const.sub_heading_multiple_14] = final_payload_df[const.instance_id].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            x=const.sub_heading_multiple_14
            y=const.cycle_count
            viz.plot_bar_chart(sub_b1,x,y,const.graph_multi_title_9,const.color_sequence)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_15)

        b7 = final_payload_df[[
        const.avg_weight,
        const.med_weight,
        const.std_weight]].describe()
        st.dataframe(b7)
        cola,colb = st.columns(2)
        with cola:
            N = 100
            random_x = final_payload_df[const.instance_id]
            random_y0 = final_payload_df[const.avg_weight]
            random_y1 = final_payload_df[const.med_weight]
            random_y2 = final_payload_df[const.std_weight]

            viz.plot_go_trace(random_x,random_y0,random_y1,random_y2, [const.avg_weight,const.med_weight,const.std_weight]
            ,const.graph_multi_title_10,const.instance_id,const.avg_weight)

        with colb:
            sub_d = final_payload_df.copy()
            sub_d[const.instance_id] = final_payload_df[const.instance_id].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            x=const.instance_id
            y=const.avg_weight
            viz.plot_bar_chart(sub_d,x,y,const.graph_multi_title_11,const.color_sequence)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_16)

        b6 = final_payload_df[[
            const.cycle_count,
            const.Two_cycle_count,const.Three_cycle_count ,const.sc_count ,
            const.lc_count ]]
        st.dataframe(b6)

        colb56, colc56 = st.columns(2)
        with colb56:
            total = final_payload_df[const.cycle_count].sum()
            a = round(final_payload_df[const.Two_cycle_count].sum()/total * 100,3)
            b = round(final_payload_df[const.Three_cycle_count].sum()/total * 100,3)
            c = round(final_payload_df[const.sc_count].sum()/total * 100,3)
            d = round(final_payload_df[const.lc_count].sum()/total * 100,3)
            values = [a,b,c,d]
            labels = ['2 Cycles -' + str(a) +'%','3 Cycles - '+ str(b) +'%' ,'Short Chains -' + str(a) +'%','Long Chains -'+ str(b) +'%']
            st.write(const.graph_multi_title_12)
            viz.plot_mat_pie(values,const.color_list,[const.two_cycles,const.three_cycles,const.short_chains,const.long_chains])

        with colc56:
            x=const.instance_id
            y=[const.Two_cycle_count,const.Three_cycle_count ,const.sc_count ,
             const.lc_count]
            title=const.graph_multi_title_13
            color_map = {const.Two_cycle_count: const.color_list[0],
            const.Three_cycle_count: const.color_list[1],
            const.sc_count: const.color_list[2],
            const.lc_count: const.color_list[3]
            }
            viz.plot_bar_chart_2(final_payload_df,x,y,title,color_map)


    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_17)

        cola, colb = st.columns(2)
        with cola:
            cor = final_payload_df[
            [const.cycle_count,const.Two_cycle_count,
            const.Three_cycle_count,
            const.sc_count,
            const.lc_count,
            const.avg_weight]]

            corrMatrix1 = cor.corr()
            st.write(const.sub_heading_multiple_5)

            st.dataframe(corrMatrix1)

        with colb:
             st.write(const.sub_heading_multiple_6)
             viz.plot_correlation_matrix(corrMatrix1)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_18)

        cola8, colb8 = st.columns(2)
        with cola8:
            attributes = [const.cycle_count,const.Two_cycle_count,
            const.Three_cycle_count,
            const.sc_count,
            const.lc_count,
            const.avg_weight]

            with st.form(const.sub_heading_multiple_15):

                x_label = (st.selectbox(const.sub_heading_multiple_8,attributes, index = 0))
                y_label = (st.selectbox(const.sub_heading_multiple_9,attributes, index = 1))
                submit_donor_filter = st.form_submit_button(const.sub_heading_multiple_16)
                title = const.sub_heading_multiple_11+ x_label + 'and' + y_label

        if(submit_donor_filter):
            with colb8:
                x = final_payload_df[x_label]
                y = final_payload_df[y_label]
                viz.plot_scatter_plot(final_payload_df,x,y,title)
