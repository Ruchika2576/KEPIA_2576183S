
import streamlit as st
import pandas as pd
import numpy as np
from utils import constants as const
from utils import sub_component_utils
from utils import visualisation_utils as viz

# Exchange Cycle Analysis
def exchange_cycle_anlysis(single_instance, recipients, payload):
    st.header(const.heading_16)
    # Preparing Exchange Cycle Data
    e = payload.get(const.output).get(const.exchange_data)[0]
    keys = e.keys()
    values = e.values()
    i = 1

    with st.container():
        # Displaying exchange cycle data with its keys
        st.markdown( const.heading_17)
        for k in keys:
            st.write( str(i) +str('. ')+ str(k) +'  :    ' + str(e.get(k) ) )
            i = i+1

        st.markdown(const.horizontal_line)
        st.markdown( const.heading_18 )
        exc = []
        ids =[]
        all = payload.get(const.output).get(const.all_cycles)
        for i in e.get(const.exchanges):
            ids.append(str(i))
            exc.append(payload.get(const.output).get(const.all_cycles).get(str(i)))
        # Calculating cycles and chains
        cycle_2, cycle_3, s_chain, l_chain = sub_component_utils.calculate_cycles_chains(payload,ids)

        df = pd.DataFrame(exc)
        df[const.two_cycles] = cycle_2
        df[const.three_cycles] = cycle_3
        df[const.short_chains] = s_chain
        df[const.long_chains] = l_chain
        df.insert(0,const.cycle_id,ids)
        df = df.astype({const.cycle: 'str' })
        df = df.astype({const.alt : 'str'})
        st.dataframe(df)
        total = len(df)
        col1, col2 = st.columns(2)
        with col1:
            # displaying cycles and chains distribution in exchange cycles
            st.markdown(const.heading_19 + str(total))
            st.markdown(const.sub_heading_8)
            st.markdown( const.sub_heading_9+ str(df[const.two_cycles].sum()))
            st.markdown( const.sub_heading_10+ str(df[const.three_cycles].sum()))
            st.markdown(const.sub_heading_11)
            st.markdown(const.sub_heading_12 + str(df[const.short_chains].sum()))
            st.markdown( const.sub_heading_13+ str(df[const.long_chains].sum()))
            show_exchanges = st.checkbox(const.sub_heading_14)


        with col2:
            st.markdown(const.graph_title_7)
            a = round(df[const.two_cycles].sum()/total * 100,3)
            b = round(df[const.three_cycles].sum()/total *100,3)
            c = round(df[const.short_chains].sum()/total * 100,3)
            d = round(df[const.long_chains].sum()/total * 100,3)
            labels = [const.two_cycles + str(a) +'%',const.three_cycles + str(b) +'%',const.short_chains + str(c) +'%',const.long_chains+ str(d) +'%']
            values = [round(a,2),round(b,2),round(c,2),round(d,2)]
            viz.plot_mat_pie(values, const.color_list, [const.two_cycles,const.three_cycles,const.short_chains,const.long_chains])

        st.markdown(const.horizontal_line)
        # Code to display all exchange cycles
        if show_exchanges:
                col = []
                val = []
                for k in e.keys():
                    col.append(k)

                for v in e.values():
                    val.append(str(v))

                for i in e.get(const.exchanges):
                  a = payload.get(const.output).get(const.all_cycles).get(str(i)).get(const.cycle)
                  df_2 = pd.DataFrame(a)
                  c2,c3,sc,lc,type = sub_component_utils.per_cycle(df_2)
                  if i%2 == 0:
                      with col2:
                          st.markdown(const.sub_heading_15+ str(i) )
                          st.markdown(type)
                          st.write(df_2)
                  else:
                       with col1:
                           st.markdown(const.sub_heading_15+ str(i) )
                           st.markdown(type)
                           st.write(df_2)

        col1, col2 = st.columns(2)
        with col1:
            # displaying cycle weight Distribution
              st.markdown( const.heading_20)
              des = pd.to_numeric(df[const.weight]).describe().to_dict()
              des['median'] = df[const.weight].median()
              st.dataframe(list(des.items()))
        with col2:
              viz.plot_histogram(df,const.weight,const.graph_title_8,const.color_sequence)


        col1, col2 = st.columns(2)
        with col1:
            # displaying cycle backarc Distribution
              st.markdown(const.horizontal_line)
              st.markdown(const.heading_21 )
              values = df[const.backarcs].value_counts().rename()
              st.write(values)
        with col2:
              viz.plot_pie(df, const.backarcs, const.graph_title_9, const.color_sequence)

# All Cycle Analysis
def all_cycle_anlysis(single_instance, recipients, payload):
    st.header(const.heading_22)

    with st.container():
            all_ids = []
            all = payload.get(const.output).get(const.all_cycles)
            for i in all:
                all_ids.append(i)
# calculating number of cycles and chains
            df = pd.DataFrame(all).T
            df = df.astype({const.cycle: 'str' })
            df = df.astype({const.alt : 'str'})
            cycle_2, cycle_3, s_chain, l_chain = sub_component_utils.calculate_cycles_chains(payload,all_ids)
            df[const.two_cycles] = cycle_2
            df[const.three_cycles] = cycle_3
            df[const.short_chains] = s_chain
            df[const.long_chains] = l_chain
            st.dataframe(df)
    total = len(df)
    col1, col2 = st.columns(2)
    with col1:
        # displaying all cycles and chains in the distribution
        st.markdown(const.heading_19 + str(total))
        st.markdown(const.sub_heading_8)
        st.markdown(const.sub_heading_9 + str(df[const.two_cycles].sum()))
        st.markdown(const.sub_heading_10 + str(df[const.three_cycles].sum()))

        st.markdown("  ")
        st.markdown(const.sub_heading_11)
        st.markdown(const.sub_heading_12 + str(df[const.short_chains].sum()))
        st.markdown(const.sub_heading_13 + str(df[const.long_chains].sum()))
    with col2:

        st.write(const.graph_title_7)
        a = round(df[const.two_cycles].sum()/total * 100,3)
        b = round(df[const.three_cycles].sum()/total *100,3)
        c = round(df[const.short_chains].sum()/total * 100,3)
        d = round(df[const.long_chains].sum()/total * 100,3)
        labels = [const.two_cycles + str(a) +'%',const.three_cycles+ str(b) +'%',const.short_chains+ str(c) +'%',const.long_chains+ str(d) +'%']
        values = [round(a,2),round(b,2),round(c,2),round(d,2)]
        viz.plot_mat_pie(values, const.color_list, [const.two_cycles,const.three_cycles,const.short_chains,const.long_chains])

    st.markdown(const.horizontal_line)
    st.markdown(const.heading_23)

    col1,col2 = st.columns([2,1])
    with col1:
        selected_indices = st.multiselect(const.sub_heading_22, df.index)
    for i in selected_indices:

        a = payload.get(const.output).get(const.all_cycles).get(str(i)).get(const.cycle)
        exp_df = pd.DataFrame(a)
        c2,c3,sc,lc,type = sub_component_utils.per_cycle(exp_df)
        with col1:

            st.markdown(const.sub_heading_15+ str(i) )
            st.markdown(type)
            st.write(exp_df)
    col1, col2 = st.columns([1,3])
    with col1:
          st.markdown(const.horizontal_line)
          st.markdown(const.heading_24)
    #       show12 = st.checkbox('  Click to expand     ')
    # if show12:
    with col1:
        # weight distribution of all cycles
         d_w = (df[const.weight])
         des = d_w.describe().to_dict()
         des['median'] = df[const.weight].median()
         st.dataframe(list(des.items()))
    with col2:
         viz.plot_histogram(df,const.weight,const.graph_title_10,const.color_sequence)


    col1, col2 = st.columns(2)
    with col1:
        # backarc distribution of all cycles
            st.markdown(const.horizontal_line)
            st.markdown(const.heading_25)
            values = df[const.backarcs].value_counts().rename(const.graph_title_11).T
            st.write(values)
    with col2:
            viz.plot_pie(df, const.backarcs, const.graph_title_11, const.color_sequence)
