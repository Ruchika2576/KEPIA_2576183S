import streamlit as st
import pandas as pd
import numpy as np
from utils import constants as const
from utils import sub_component_utils
from utils import visualisation_utils as viz

def analysis_donor(donor_final_list_stored, session_state_name):

    donor_instance_list_data_stored = None
    donor_instances_df_stored = None

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

    if session_state_name not in st.session_state:
        instance_ids = list(range(1, len(donor_final_list_stored)+1))

        for donor_sub in donor_final_list_stored:
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
                donor[const.matches_count] = donor.apply(lambda row: (sub_component_utils.count_matches(row)) ,axis = 1)

                #Calculating values
                number_of_donors = donor.shape[0]
                average_total_matches = donor[const.matches_count].mean()
                max_matches = donor[const.matches_count].max()
                min_matches = donor[const.matches_count].min()
                no_matches= donor[const.matches_count].isnull().sum()
                non_alt = donor[const.altruistic].isnull().sum()
                alt = number_of_donors - non_alt
                multiple_sources = sub_component_utils.count_sources(donor)
                avg_age = donor[const.dage].mean()
                med_age = donor[const.dage].median()
                min_age =donor[const.dage].min()
                max_age = donor[const.dage].max()
                a,o,b,ab = sub_component_utils.count_blood_distribution(donor)

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

        donor_instance_list_data_stored = {
        const.instance_id: instance_ids,
        const.donors_count:donors_count,
        const.avg_match: avg_total_matches_list,
        const.max_match:max_matches_list,
        const.alt_count:alt_list,
        const.nonalt_count:non_alt_list,
        const.multiple_source:multiple_sources_l,
        const.avg_age:avg_age_l,
        const.min_age:min_age_l,
        const.max_age:max_age_l,
        const.median_age:med_age_l,
        const.a_type:a_type_l,
        const.b_type:b_type_l,
        const.o_type:o_type_l,
        const.ab_type:ab_type_l,
        const.no_match: no_matches_list,
        const.min_match:min_matches_list,
        }

        donor_instances_df_stored = pd.DataFrame(donor_instance_list_data_stored)
        st.session_state[session_state_name] = donor_instances_df_stored

    donor_instances_df_stored = st.session_state[session_state_name]
    st.markdown(const.donor_heading)
    st. dataframe(donor_instances_df_stored)
    st.markdown(const.horizontal_line)
    st.markdown(const.accumulative_donor)
    x_d = donor_instances_df_stored.copy()
    del x_d[const.instance_id]
    st.dataframe(x_d.describe().iloc[[1,2,3,4,5,6,7]])


    with st.container():
        st.markdown(const.horizontal_line)

        cola, colb = st.columns(2)
        with cola:
            st.markdown(const.heading_multiple_1)
            b = donor_instances_df_stored[[const.donors_count]].copy()
            st.dataframe(b.describe())
        with colb:
            sub_b = b.copy()
            sub_b[const.instance_id] = donor_instances_df_stored[const.instance_id].copy()
            # fig = px.histogram(a_380, x="No. of Donors",y = 'Frequency in the Set',title = 'Donors Count distribution  ' , color_discrete_sequence = px.colors.sequential.Cividis)
            viz.plot_bar_chart(sub_b,const.instance_id, const.donors_count, const.graph_multi_title_1, const.color_sequence )

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_2)

        b1 = donor_instances_df_stored[[const.alt_count,const.nonalt_count]].describe()
        st.dataframe(b1)
        colb1, colc1 = st.columns(2)
        with colb1:
            total = donor_instances_df_stored[const.donors_count].sum()
            sum = donor_instances_df_stored[const.alt_count].sum()
            sum2 = donor_instances_df_stored[const.nonalt_count].sum()
            aa = round(((sum)/total * 100),2)
            bb = round(((sum2)/total *100),2)

            values = [round(aa,2),round(bb,2)]
            labels = [const.sub_heading_multiple_1+'\n' + str(aa) +'%', const.sub_heading_multiple_2+'\n '+ str(bb) +'%']
            st.write(const.graph_multi_title_2)
            viz.plot_mat_pie(values,const.two_colors,[const.alt_count,const.nonalt_count])

        with colc1:
            viz.plot_bar_chart_2(donor_instances_df_stored,const.instance_id,[const.alt_count, const.nonalt_count],const.graph_multi_title_3,{const.alt_count:'#ffbb99', const.nonalt_count:'#cc0044'})


    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_3)
        cola,colb = st.columns(2)
        with cola:
            b2 = donor_instances_df_stored[[
            const.avg_age,
            const.min_age,
            const.max_age,
            const.median_age]].describe()
            st.dataframe(b2)
        with colb:
            N = 100
            random_x = donor_instances_df_stored[const.instance_id]
            random_y0 = donor_instances_df_stored[const.avg_age]
            random_y1 = donor_instances_df_stored[const.min_age]
            random_y2 = donor_instances_df_stored[const.max_age]

            # Create traces
            st.write(const.sub_heading_multiple_3)
            viz.plot_go_trace(random_x,random_y0,random_y1,random_y2,[const.avg_age,const.min_age,const.max_age],const.graph_multi_title_4 ,const.instance_id,const.avg_age)


    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_4)
        cola, colb = st.columns(2)
        with cola:
            b = donor_instances_df_stored[[const.avg_match,const.max_match,const.min_match]]
            st.dataframe(b.describe())
        with colb:
            viz.plot_bar_chart(donor_instances_df_stored, const.instance_id,const.avg_match,const.graph_multi_title_5,const.color_sequence)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_5)


        b4 = donor_instances_df_stored[[
        const.a_type,
        const.b_type,const.o_type,const.ab_type]].describe()
        st.dataframe(b4)
        colb5, colc5 = st.columns(2)
        with colb5:
            total = donor_instances_df_stored[const.donors_count].sum()
            a = round(donor_instances_df_stored[const.a_type].sum()/total * 100,3)
            b = round(donor_instances_df_stored[const.b_type].sum()/total * 100,3)
            c = round(donor_instances_df_stored[const.o_type].sum()/total * 100,3)
            d = round(donor_instances_df_stored[const.ab_type].sum()/total * 100,3)
            values = [a,b,c,d]
            labels = ['A -' + str(a) +'%','B - '+ str(b) +'%' ,'O -' + str(a) +'%','AB -'+ str(b) +'%']
            st.write(const.sub_heading_multiple_4)
            viz.plot_mat_pie(values,const.color_list,['A','B','O','AB'])
            # ['#0077e6','#0059b3','#003366','#001a33']

        with colc5:

            y=[const.a_type,const.b_type,const.o_type,const.ab_type]
            color_map={const.ab_type:const.color_list[3],const.a_type:const.color_list[0],const.o_type:const.color_list[2],
                     const.b_type:const.color_list[1], }
            viz.plot_bar_chart_2(donor_instances_df_stored,const.instance_id,y,const.graph_multi_title_6,color_map)


    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_6)

        cola, colb = st.columns(2)
        with cola:
            cor = donor_instances_df_stored[[const.donors_count,const.avg_match,const.alt_count,
            const.nonalt_count,const.avg_age,const.a_type,
            const.b_type,const.o_type,const.ab_type
            ]]

            corrMatrix = cor.corr()
            st.write(const.sub_heading_multiple_5)

            st.dataframe(corrMatrix)

        with colb:

             st.write(const.sub_heading_multiple_6)
             viz.plot_correlation_matrix(corrMatrix)

    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_multiple_7)

        cola8, colb8 = st.columns(2)
        with cola8:
            attributes = [const.donors_count,const.avg_match,const.alt_count,
            const.nonalt_count,const.avg_age,const.a_type,
            const.b_type,const.o_type,const.ab_type
            ]
            with st.form(const.sub_heading_multiple_7):

                x_label = (st.selectbox(const.sub_heading_multiple_8,attributes, index = 0))
                y_label = (st.selectbox(const.sub_heading_multiple_9,attributes, index = 1))
                submit_donor_filter = st.form_submit_button(const.sub_heading_multiple_10)
                title =  const.sub_heading_multiple_11 + x_label + 'and' + y_label

        if(submit_donor_filter):
                with colb8:
                    viz.plot_scatter_plot(donor_instances_df_stored,donor_instances_df_stored[x_label],donor_instances_df_stored[y_label],title)
