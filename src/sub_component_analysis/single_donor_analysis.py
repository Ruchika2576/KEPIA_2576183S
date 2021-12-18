import streamlit as st
import pandas as pd
import numpy as np
from utils import constants as const
from utils import sub_component_utils
from utils import visualisation_utils as viz

def donor_data_analysis(single_instance):
    donors = pd.DataFrame(single_instance).T
    donors = donors.astype({const.source: 'str' })

    # Counting no. of matches for each donor
    l = []
    for i in donors[const.matches]:
        l.append(str(i))
    donors[const.Matches] = l
    donors[const.Matches][donors[const.Matches] == np.NaN] = 0
    donors[const.matches_count] = donors.apply(lambda row: (sub_component_utils.count_matches(row)) ,axis = 1)

    # displaying donor table
    st.markdown(const.single_donor_heading)
    sub = (donors[[const.source,const.dage,const.Matches,const.matches_count,const.bloodtype]]).copy()
    st.dataframe(sub)

    # calculations to display donor statistics
    total = (donors.shape[0])
    alt_donors = str(donors.shape[0] - donors[const.altruistic].isnull().sum())
    non_alt_donors = str(donors[const.altruistic].isnull().sum())
    no_matches = str(donors[const.matches].isnull().sum())

    # code to count multiple donors, along with donor ids
    d = pd.DataFrame(single_instance)
    x = d.T[const.source].value_counts(dropna = 'True')
    y = x.where(x > 1).value_counts(dropna = 'True')
    multiple_donors_count = y.to_dict()
    k = list(multiple_donors_count.keys())
    v = list(multiple_donors_count.values())
    two_donors = x.index[x == 2]
    three_donors = x.index[x == 3]
    four_donors = x.index[x == 4]
    non_alt_list = donors.index[donors[const.altruistic] == True]
    no_matches_list = donors.index[donors[const.matches_count] == 0]
    multiple_total = 0
    for i in range(len(v)):
        multiple_total = multiple_total + int(v[i] )

    # displaying Donor analysis/ each analysis is divided within containers
    with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_1  + str(total ))
        st.markdown(const.heading_2 + no_matches  + const.sub_heading_1 + (const.comma.join(no_matches_list)) )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(const.heading_3 + alt_donors)
        with st.container():
            st.dataframe(sub[[const.dage,const.Matches,const.matches_count,const.bloodtype]][donors[const.altruistic] == True ])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(const.heading_4 + str(multiple_total) )
            for i in range(len(k)):
                st.markdown( str(v[i]) + const.sub_heading_2 + str(int(k[i] ))+ const.sub_heading_3 )
        with col2:
                st.markdown("  ")
                a = []
                for i in two_donors:
                    a.append(i)
                if(len(a) != 0):
                    st.write(const.sub_heading_4 + str(a))
                b = []
                for i in three_donors:
                    b.append(i)
                if(len(b) != 0):
                    st.write(const.sub_heading_5+ str(b) )
                c = []
                for i in four_donors:
                    c.append(i)
                if(len(c) != 0):
                    st.write(const.sub_heading_6+ str(c) )

    with st.container():
        # To render donor's based on specific ids
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_5)
        selected_indices = st.multiselect(const.sub_heading_7, donors.index)

        for i in selected_indices:
            i = int(i)
            x = sub.iloc[i]

            sub_component_utils.render_donor(x,i,donors)

    col1, col2 = st.columns(2)
    with col1:
        # Donor's age Distribution
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_6 )

        with col1:
           des = pd.to_numeric(donors[const.dage]).describe().to_dict()
           des['median'] = donors[const.dage].median()
           st.dataframe(list(des.items()))

        with col2:
            a = donors.copy()
            a1 = a[const.dage].value_counts().to_dict()
            a['Donors Count'] = a[const.dage].map(a1)
            viz.plot_altair_bar(a,const.graph_title_1,const.dage, 'Donors Count', const.single_orange)

    col1, col2 = st.columns(2)
    with col1:
        # Donor's count Distribution
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_7)

    with col1:
        btvalues = donors[const.bloodtype].value_counts().rename('Donor counts')
        st.write(pd.DataFrame(btvalues).T)
    with col2:
        viz.plot_pie(donors, const.bloodtype,const.graph_title_2 , const.color_sequence)


    col1, col2 = st.columns(2)
    with col1:
        # Donor's match count distribution
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_8)
        a = donors.copy()
        a1 = a[const.matches_count].value_counts().to_dict()
        a['Frequency'] = a[const.matches_count].map(a1)
        des = pd.to_numeric(donors[const.matches_count]).describe().to_dict()
        des['median'] = donors[const.matches_count].median()
        st.dataframe(list(des.items()))
    with col2:
        viz.plot_altair_bar(a,const.graph_title_3,const.matches_count,'Frequency',const.single_orange)

    with st.container():
        # filter donors form
        filter_data_donors(donors)

def filter_data_donors(donors):
    st.markdown(const.horizontal_line)
    st.markdown(const.heading_9)
    dage_low =0
    dage_high =1
    count_low = 0
    count_high = 1
    bloodtype_choices = 'A'
    altruistic_choices = True

    finaldisplay_donor = None
    min_age = donors[const.dage].min()
    max_age = donors[const.dage].max()
    min_count = donors[const.matches_count].min()
    max_count = donors[const.matches_count].max()
    # st.write(min_age,max_age,min_count,max_count)

    col111, col222 = st.columns(2)
    with col111:
        st.write(const.filter_heading_1)

        with st.form(const.form_name_1):
            # reading input for filtered donors
            dage_low = st.number_input(const.filter_heading_2, min_value=min_age, max_value=max_age)
            dage_high = st.number_input(const.filter_heading_3,min_value=min_age, max_value=max_age, value = max_age)
            bloodtype_choices = (st.selectbox(const.filter_heading_4,['A','O','AB','A','None'], index = 4))
            count_low = st.number_input(const.filter_heading_5, min_value=min_count, max_value=max_count )
            count_high = st.number_input(const.filter_heading_6,min_value=min_count, max_value=max_count, value = max_count)
            altruistic_choices = (st.selectbox(const.filter_heading_7,['True','False','None'], index = 2))


            submit_donor_filter = st.form_submit_button(const.form_name_2)

            # calculating the filtered donors list
            if(submit_donor_filter):
                if altruistic_choices != 'None' and bloodtype_choices != 'None' :
                    if(altruistic_choices == 'False'):
                        finaldisplay_donor = donors[
                            ((donors[const.dage] >= dage_low) & (donors[const.dage] <= dage_high)) &
                            (donors[const.bloodtype] == str(bloodtype_choices)) &
                            ((donors[const.matches_count] >= count_low) & (donors[const.matches_count] <= count_high)) &
                            (donors[const.altruistic].isnull())
                            ]
                    elif(altruistic_choices == 'True'):
                        finaldisplay_donor = donors[
                            ((donors[const.dage] >= dage_low) & (donors[const.dage] <= dage_high)) &
                            (donors[const.bloodtype] == str(bloodtype_choices)) &
                            ((donors[const.matches_count] >= count_low) & (donors[const.matches_count] <= count_high)) &
                            ((donors[const.altruistic]== True))
                            ]
                elif altruistic_choices == 'None' and bloodtype_choices != 'None':
                    finaldisplay_donor = finaldisplay_donor = donors[
                        ((donors[const.dage] >= dage_low) & (donors[const.dage] <= dage_high)) &
                        (donors[const.bloodtype] == str(bloodtype_choices)) &
                        ((donors[const.matches_count] >= count_low) & (donors[const.matches_count] <= count_high)) ]

                elif altruistic_choices != 'None' and bloodtype_choices == 'None':
                    if(altruistic_choices == 'False'):
                        finaldisplay_donor = donors[
                            ((donors[const.dage] >= dage_low) & (donors[const.dage] <= dage_high)) &
                            ((donors[const.matches_count] >= count_low) & (donors[const.matches_count] <= count_high)) &
                            (donors[const.altruistic].isnull())
                            ]
                    elif(altruistic_choices == 'True'):
                        finaldisplay_donor = donors[
                            ((donors[const.dage] >= dage_low) & (donors[const.dage] <= dage_high)) &
                            ((donors[const.matches_count] >= count_low) & (donors[const.matches_count] <= count_high)) &
                            ((donors[const.altruistic]== True))
                            ]
                elif altruistic_choices == 'None' and bloodtype_choices == 'None':
                    finaldisplay_donor = donors[
                        ((donors[const.dage] >= dage_low) & (donors[const.dage] <= dage_high)) &
                        ((donors[const.matches_count] >= count_low) & (donors[const.matches_count] <= count_high))
                        ]

    with col222:
        # displaying filtered donors
        if finaldisplay_donor is not None:
            st.markdown(const.heading_10)
            st.write(const.filter_heading_8 + str(len(finaldisplay_donor)))
            st.write(const.filter_heading_9 + str(dage_low) +const.to + str(dage_high) )
            st.write(const.filter_heading_10 + bloodtype_choices)
            st.write(const.filter_heading_11 +  altruistic_choices )
            st.write(const.filter_heading_12  + str(count_low) +const.to + str(count_high) )
            st.dataframe(finaldisplay_donor)
