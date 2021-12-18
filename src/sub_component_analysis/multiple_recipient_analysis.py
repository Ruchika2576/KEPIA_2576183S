import streamlit as st
import pandas as pd
import numpy as np
from utils import constants as const
from utils import sub_component_utils
from utils import visualisation_utils as viz

# this function performs analysis on all the recipients of the set
def analysis_recipient(recipient_final_list_stored,session_state_name):

    recipients_instances_data_stored = None
    recipients_instances_fin_df_stored = None

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

    if session_state_name not in st.session_state:
        instance_ids = list(range(1, len(recipient_final_list_stored)+1))
        # first, calculations are done on individual recipient and then combined in a table
        for recipients in recipient_final_list_stored:
            number_of_recipients = 0
            non_compatible = 0
            compatible = 0
            a,o,b,ab = 0,0,0,0
            cPRA_mean = 0
            cPRA_median = 0
            cPRA_std_deviation = 0

            recipients_df = pd.DataFrame(recipients).T

            number_of_recipients = recipients_df.shape[0]
            non_compatible,compatible = sub_component_utils.count_compatible(recipients_df)
            a,o,b,ab = sub_component_utils.count_blood_distribution(recipients_df)
            cPRA_mean = recipients_df[const.cPRA].mean()
            cPRA_median = recipients_df[const.cPRA].median()
            cPRA_std_deviation = recipients_df[const.cPRA].std()

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
        # all calculations are combined under a column name in resulting data frame
        recipients_instances_data_stored = {
        const.instance_id: instance_ids,
        const.recipients_count:number_of_recipients_l,
        const.comp_count:non_compatible_l,
        const.hascomp_count: compatible_l,
        const.a_rec_count : a_l,
        const.o_rec_count: o_l,
        const.b_rec_count: b_l,
        const.ab_rec_count: ab_l,
        const.cpra_mean : cPRA_mean_l,
        const.cpra_median : cPRA_median_l,
        const.cpra_std: cPRA_std_deviation_l
        }

        recipients_instances_fin_df_stored = pd.DataFrame(recipients_instances_data_stored)

        st.session_state[session_state_name] = recipients_instances_fin_df_stored

    recipients_instances_fin_df_stored = st.session_state[session_state_name]
    st.markdown(const.recipient_heading)
    # the recipient dataframe is shown on the UI
    st. dataframe(recipients_instances_fin_df_stored)
    st.markdown(const.horizontal_line)

    st.markdown(const.accumulative_recipient)

    x = recipients_instances_fin_df_stored.copy()
    del x[const.instance_id]
    st.dataframe(x.describe().iloc[[1,2,3,4,5,6,7]])

    # All the analysis begins here, and are grouped into containers
    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_8)
        cola, colb = st.columns(2)
        with cola:
            b = recipients_instances_fin_df_stored[[const.recipients_count]]
            st.dataframe(b.describe())
        with colb:
            b_sub = b.copy()
            b_sub[const.sub_heading_multiple_14] = recipients_instances_fin_df_stored[const.instance_id].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            st.write(const.sub_heading_multiple_4)
            viz.plot_bar_chart(b_sub,const.sub_heading_multiple_14,const.recipients_count,const.graph_multi_title_7,const.color_sequence)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_9)

        b1 = recipients_instances_fin_df_stored[[const.comp_count,const.hascomp_count]].describe()
        st.dataframe(b1)
        colb1, colc1 = st.columns(2)
        with colb1:
            total = recipients_instances_fin_df_stored[const.recipients_count].sum()
            sum = recipients_instances_fin_df_stored[const.comp_count].sum()
            sum2 = recipients_instances_fin_df_stored[const.hascomp_count].sum()
            aa = round(((sum)/total * 100),2)
            bb = round(((sum2)/total *100),2)

            values = [round(aa,2),round(bb,2)]
            labels = [const.comp_count + '\n' + str(aa) +'%',const.hascomp_count+'\n'+ str(bb) +'%']
            st.write(const.sub_heading_multiple_4)
            viz.plot_mat_pie(values,const.two_colors,[const.comp_count,const.hascomp_count])

        with colc1:
            color_map = {const.comp_count:const.color_list[0], const.hascomp_count:const.color_list[2]}
            viz.plot_bar_chart_2(recipients_instances_fin_df_stored,const.instance_id,[const.comp_count, const.hascomp_count],const.graph_multi_title_8,color_map)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_10)

        b6 = recipients_instances_fin_df_stored[[
        const.a_rec_count,
        const.o_rec_count,const.b_rec_count,const.ab_rec_count]].describe()
        st.dataframe(b6)
        colb56, colc56 = st.columns(2)
        with colb56:
            total = recipients_instances_fin_df_stored[const.recipients_count].sum()
            a = round(recipients_instances_fin_df_stored[const.a_rec_count].sum()/total * 100,3)
            b = round(recipients_instances_fin_df_stored[const.o_rec_count].sum()/total * 100,3)
            c = round(recipients_instances_fin_df_stored[const.b_rec_count].sum()/total * 100,3)
            d = round(recipients_instances_fin_df_stored[const.ab_rec_count].sum()/total * 100,3)
            values = [a,b,c,d]
            labels = ['A -' + str(a) +'%','O - '+ str(b) +'%' ,'B -' + str(a) +'%','AB -'+ str(b) +'%']
            st.write(const.sub_heading_multiple_4)
            viz.plot_mat_pie(values,const.color_list,['A','B','O','AB'])

        with colc56:
            y=[const.a_rec_count,const.o_rec_count,const.b_rec_count,const.ab_rec_count]
            title= const.graph_multi_title_8
            color_map={const.a_rec_count:const.color_list[0],const.o_rec_count:const.color_list[2],const.b_rec_count:const.color_list[1],const.ab_rec_count:const.color_list[3]}
            viz.plot_bar_chart_2(recipients_instances_fin_df_stored,const.instance_id,y,title,color_map)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_11)


        b2 = recipients_instances_fin_df_stored[[
        const.cpra_mean,
        const.cpra_median,
        const.cpra_std]].describe()
        st.dataframe(b2)
        cola,colb = st.columns(2)
        with cola:
            N = 100
            random_x = recipients_instances_fin_df_stored[const.instance_id]
            random_y0 = recipients_instances_fin_df_stored[const.cpra_mean]
            random_y1 = recipients_instances_fin_df_stored[const.cpra_median]
            random_y2 = recipients_instances_fin_df_stored[const.cpra_std]

            viz.plot_go_trace(random_x,random_y0,random_y1,random_y2,[const.cpra_mean,const.cpra_median,const.cpra_std],
            const.graph_title_12 ,const.instance_id,const.cpra_mean)

        with colb:
            sub_a = recipients_instances_fin_df_stored.copy()
            sub_a['Instance Ids'] = recipients_instances_fin_df_stored[const.instance_id].copy()
            x='Instance Ids'
            viz.plot_bar_chart(sub_a,x,const.cpra_mean,const.graph_title_13,const.color_sequence)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_12)

        cola, colb = st.columns(2)
        with cola:
            cor = recipients_instances_fin_df_stored[[const.recipients_count,const.comp_count,const.hascomp_count,
            const.a_rec_count,const.o_rec_count,const.b_rec_count,
            const.ab_rec_count,const.cpra_mean]]

            corrMatrix1 = cor.corr()
            st.write(const.sub_heading_multiple_5)

            st.dataframe(corrMatrix1)

        with colb:
            st.write(const.sub_heading_multiple_6)
            viz.plot_correlation_matrix(corrMatrix1)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_13)

        cola8, colb8 = st.columns(2)
        with cola8:
            attributes = [const.recipients_count,const.comp_count,const.hascomp_count,
            const.a_rec_count,const.o_rec_count,const.b_rec_count,
            const.ab_rec_count,const.cpra_mean]

            with st.form(const.sub_heading_multiple_12):

                x_label = (st.selectbox(const.sub_heading_multiple_8,attributes, index = 0))
                y_label = (st.selectbox(const.sub_heading_multiple_9,attributes, index = 1))
                submit_donor_filter = st.form_submit_button(const.sub_heading_multiple_13)
                title = const.sub_heading_multiple_11 + x_label + 'and' + y_label

        if(submit_donor_filter):
                x = recipients_instances_fin_df_stored[x_label]
                y = recipients_instances_fin_df_stored[y_label]
                with colb8:
                    viz.plot_scatter_plot(recipients_instances_fin_df_stored,x,y,title)
