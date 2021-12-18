import streamlit as st
import pandas as pd
import numpy as np
from utils import constants as const
from utils import sub_component_utils
from utils import visualisation_utils as viz
# This module calculates multiple analysis on exchange cycles

# This function prepares data for multiple files uploaded, after preparing the the dataframe, the dataframe is further sent for analysis

def analysis_multiple_exchanges(payload_list,session_state_name):
    if payload_list in st.session_state:
        payload_list = st.session_state.payload_list
    exchange_data_instances = None
    exchange_data_final_df = None
    description = payload_list[0].get(const.output).get(const.exchange_data)[0].get(const.description)

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
    if session_state_name not in st.session_state:
            instance_ids = list(range(1, len(payload_list)+1))

            for payload in payload_list:
                  exchange_data = payload.get(const.output).get(const.exchange_data)[0]
                  exchanges = exchange_data.get(const.exchanges)
                  weight_l.append(exchange_data.get(const.weight))
                  two_way_exc_l.append(exchange_data.get(const.two_way_exchanges))
                  three_way_exc_l.append(exchange_data.get(const.three_way_exchanges))
                  total_transplants_l.append(exchange_data.get(const.total_transplants))

                  exc_cycle_ids = []
                  exchange_cycle_list = []
                  for i in exchanges:
                        exc_cycle_ids.append(str(i))
                        exchange_cycle_list.append(payload.get(const.output).get(const.all_cycles).get(str(i)))
                  exc_cycle_df = pd.DataFrame(exchange_cycle_list)

                  no_exc_cycles.append(len(exc_cycle_df))

                  cycle_2, cycle_3, s_chain, l_chain = sub_component_utils.calculate_cycles_chains(payload,exc_cycle_ids)
                  exc_cycle_df[const.two_cycles] = cycle_2
                  exc_cycle_df[const.three_cycles] = cycle_3
                  exc_cycle_df[const.short_chains] = s_chain
                  exc_cycle_df[const.long_chains] = l_chain

                  no_of_two_cycles_l.append(exc_cycle_df[const.two_cycles].sum())
                  no_of_three_cycles_l.append(exc_cycle_df[const.three_cycles].sum())
                  no_of_short_chains_l.append(exc_cycle_df[const.short_chains].sum())
                  no_of_long_chains_l.append(exc_cycle_df[const.long_chains].sum())

                  weight_avg_l.append(exc_cycle_df[const.weight].mean())
                  weight_median_l.append(exc_cycle_df[const.weight].median())
                  weight_std_l.append(exc_cycle_df[const.weight].std())
                  cycles_with_backarcs_l.append(len(exc_cycle_df[const.backarcs][exc_cycle_df[const.backarcs] > 0]))


            exchange_data_instances = {
            const.instance_id : instance_ids,
            const.exc_count : no_exc_cycles,
            const.exc_weight: weight_l,
            const.two_exc_weight: two_way_exc_l,
            const.three_way:three_way_exc_l ,
            const.Total_transplants: total_transplants_l ,
            const.Two_cycle_count: no_of_two_cycles_l ,
            const.Three_cycle_count : no_of_three_cycles_l ,
            const.sc_count:no_of_short_chains_l ,
            const.lc_count : no_of_long_chains_l,
            const.back_count : cycles_with_backarcs_l,
            const.avg_weight : weight_avg_l ,
            const.med_weight:weight_median_l ,
            const.std_weight:weight_std_l
            }

            exchange_data_final_df = pd.DataFrame(exchange_data_instances)
            st.session_state[session_state_name] = exchange_data_final_df

    exchange_data_final_df = st.session_state[session_state_name]
    analysis_exchanges(exchange_data_final_df,description)

# This function prepares data for stored set's exchange cycles, after preparing the the dataframe, the dataframe is further sent for analysis

def analysis_stored_exchanges(payload_final_list_stored,session_state_name):
    if payload_final_list_stored in st.session_state:
        payload_final_list_stored = st.session_state.payload_final_list_stored
    exchange_data_instances_stored = None
    exchange_data_final_df_stored = None
    description = payload_final_list_stored[0].get(const.output).get(const.exchange_data)[0].get(const.description)

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
    if session_state_name not in st.session_state:
            instance_ids = list(range(1, len(payload_final_list_stored)+1))

            for payload in payload_final_list_stored:
                  exchange_data = payload.get(const.output).get(const.exchange_data)[0]
                  exchanges = exchange_data.get(const.exchanges)
                  weight_l.append(exchange_data.get(const.weight))
                  two_way_exc_l.append(exchange_data.get(const.two_way_exchanges))
                  three_way_exc_l.append(exchange_data.get(const.three_way_exchanges))
                  total_transplants_l.append(exchange_data.get(const.total_transplants))

                  exc_cycle_ids = []
                  exchange_cycle_list = []
                  for i in exchanges:
                        exc_cycle_ids.append(str(i))
                        exchange_cycle_list.append(payload.get(const.output).get(const.all_cycles)[i])

                  exc_cycle_df = pd.DataFrame(exchange_cycle_list)
                  no_exc_cycles.append(len(exc_cycle_df))

                  cycle_2, cycle_3, s_chain, l_chain = sub_component_utils.calculate_cycles_chains_stored(payload,exc_cycle_ids)
                  exc_cycle_df[const.two_cycles] = cycle_2
                  exc_cycle_df[const.three_cycles] = cycle_3
                  exc_cycle_df[const.short_chains] = s_chain
                  exc_cycle_df[const.long_chains] = l_chain

                  no_of_two_cycles_l.append(exc_cycle_df[const.two_cycles].sum())
                  no_of_three_cycles_l.append(exc_cycle_df[const.three_cycles].sum())
                  no_of_short_chains_l.append(exc_cycle_df[const.short_chains].sum())
                  no_of_long_chains_l.append(exc_cycle_df[const.long_chains].sum())

                  weight_avg_l.append(exc_cycle_df[const.weight].mean())
                  weight_median_l.append(exc_cycle_df[const.weight].median())
                  weight_std_l.append(exc_cycle_df[const.weight].std())
                  cycles_with_backarcs_l.append(len(exc_cycle_df[const.backarcs][exc_cycle_df[const.backarcs] > 0]))


            exchange_data_instances_stored = {
            const.instance_id : instance_ids,
            const.exc_count : no_exc_cycles,
            const.exc_weight: weight_l,
            const.two_exc_weight: two_way_exc_l,
            const.three_way:three_way_exc_l ,
            const.Total_transplants: total_transplants_l ,
            const.Two_cycle_count: no_of_two_cycles_l ,
            const.Three_cycle_count : no_of_three_cycles_l ,
            const.sc_count:no_of_short_chains_l ,
            const.lc_count : no_of_long_chains_l,
            const.back_count : cycles_with_backarcs_l,
            const.avg_weight : weight_avg_l ,
            const.med_weight:weight_median_l ,
            const.std_weight:weight_std_l
            }

            exchange_data_final_df_stored = pd.DataFrame(exchange_data_instances_stored)
            st.session_state[session_state_name] = exchange_data_final_df_stored

    exchange_data_final_df_stored = st.session_state[session_state_name]
    analysis_exchanges(exchange_data_final_df_stored,description)

# Here the actual analysis begin
def analysis_exchanges(final_exchange_df,description):

        st.markdown(const.exchange_cycle_heading)
        st.markdown(const.sub_heading_multiple_20 + description)
        st. dataframe(final_exchange_df)
        st.markdown(const.horizontal_line)
        st.markdown(const.all_cycle_accum)
        index = [const.exc_count,const.exc_weight,const.two_exc_weight, const.three_way,
         const.Total_transplants, const.Two_cycle_count, const.Three_cycle_count,const.sc_count,const.lc_count, const.back_count,
         const.avg_weight]

        # This particular line displays the exchange cycle dataframe on the UI
        st.dataframe(final_exchange_df.describe()[index].iloc[[1,2,3,4,5,6,7]])

        # hereafter all analysis is sectioned into containers
        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown(const.heading_multiple_19)
            cola, colb = st.columns(2)
            with cola:
                sub_df_final= final_exchange_df[[const.exc_count]]
                st.dataframe(sub_df_final.describe())
            with colb:
                temp3 = sub_df_final.copy()
                temp3[const.sub_heading_multiple_14] = final_exchange_df[const.instance_id].copy()
                x=const.sub_heading_multiple_14
                y=const.exc_count
                viz.plot_bar_chart(temp3,x,y,const.graph_multi_title_14,const.color_sequence)

        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown(const.heading_multiple_20)
            cola, colb = st.columns(2)
            with cola:
                sub_df_final1= final_exchange_df[[const.Total_transplants]]
                st.dataframe(sub_df_final1.describe())
            with colb:
                sub_df_final1_copy = sub_df_final1.copy()
                sub_df_final1_copy[const.sub_heading_multiple_14]  = final_exchange_df[const.instance_id].copy()
                viz.plot_bar_chart(sub_df_final1_copy,const.sub_heading_multiple_14,const.Total_transplants,const.graph_multi_title_15,const.color_sequence)

        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown(const.heading_multiple_21)

            temp = final_exchange_df[[const.exc_weight,const.avg_weight]].describe()
            st.dataframe(temp)

            cola,colb = st.columns(2)
            with cola:

                random_x = final_exchange_df[const.instance_id]
                random_y0 = final_exchange_df[const.exc_weight]
                random_y1 = final_exchange_df[const.avg_weight]

                viz.plot_go_trace2(random_x,random_y0,random_y1, [const.exc_weight,const.avg_weight],const.graph_multi_title_16,const.instance_id,const.sub_heading_multiple_19)

            with colb:

                temp2 = final_exchange_df.copy()
                temp2[const.instance_id] = final_exchange_df[const.instance_id].copy()
                viz.plot_bar_chart(temp2,const.instance_id,const.exc_weight,const.graph_multi_title_17,const.color_sequence)

        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown(const.heading_multiple_22)
            b6 = final_exchange_df[[
                const.exc_count,
                const.Two_cycle_count,const.Three_cycle_count ,
                const.sc_count ,
                const.lc_count ]]
            st.dataframe(b6)
            colb56, colc56 = st.columns(2)
            with colb56:
                total = final_exchange_df[const.exc_count].sum()
                a = round(final_exchange_df[const.Two_cycle_count].sum()/total * 100,3)
                b = round(final_exchange_df[const.Three_cycle_count].sum()/total * 100,3)
                c = round(final_exchange_df[const.sc_count].sum()/total * 100,3)
                d = round(final_exchange_df[const.lc_count].sum()/total * 100,3)

                values = [a,b,c,d]
                labels = ['2 Cycles -' + str(a) +'%','3 Cycles - '+ str(b) +'%' ,'Short Chains -' + str(a) +'%','Long Chains -'+ str(b) +'%']
                st.write(const.graph_multi_title_12)
                viz.plot_mat_pie(values,const.color_list,[const.two_cycles,const.three_cycles,const.short_chains,const.long_chains])

            with colc56:
                x=const.instance_id
                y=[const.Two_cycle_count,const.Three_cycle_count ,const.sc_count ,const.lc_count]
                title= const.graph_multi_title_18
                color_map = {const.Two_cycle_count:'#ffbb99',const.Three_cycle_count:'#e64d00',const.sc_count:'#cc0044',const.lc_count:'#800040'}
                viz.plot_bar_chart_2(final_exchange_df,x,y,const.graph_multi_title_18,color_map)

        with st.container():
            st.markdown(const.horizontal_line)
            st.markdown(const.heading_multiple_23)

            cola, colb = st.columns(2)
            with cola:
                cor = final_exchange_df[[
                const.exc_count,const.exc_weight,
                const.two_exc_weight,const.avg_weight,
                const.three_way,const.Two_cycle_count,const.Three_cycle_count,
                const.Total_transplants,const.sc_count,const.lc_count]]

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
                attributes = [
                const.exc_count,const.exc_weight,
                const.two_exc_weight,const.avg_weight,const.three_way,const.Two_cycle_count,const.Three_cycle_count,
                const.three_way,const.Total_transplants,const.sc_count,const.lc_count]

                with st.form(const.sub_heading_multiple_17):

                    x_label = (st.selectbox(const.sub_heading_multiple_8,attributes, index = 0))
                    y_label = (st.selectbox(const.sub_heading_multiple_9,attributes, index = 1))
                    submit_donor_filter = st.form_submit_button(const.sub_heading_multiple_18)
                    title = const.sub_heading_multiple_11 + x_label + 'and' + y_label

            if(submit_donor_filter):
                with colb8:
                    x = final_exchange_df[x_label]
                    y = final_exchange_df[y_label]
                    viz.plot_scatter_plot(final_exchange_df,x,y,title)
