import streamlit as st
import pandas as pd
import numpy as np
from utils import constants as const
from utils import visualisation_utils as viz

def recipient_data_analysis(recipients):

   # Preparing recpients data frame
   recipients = pd.DataFrame(recipients).T

   st.header(const.single_recipient_heading)
   # displaying rescipients table
   st.write(recipients)
   total = (recipients.shape[0])

   #displaying total number of recipients
   with st.container():
        st.markdown(const.horizontal_line)
        st.markdown(const.heading_11  + str(total ))

   col1, col2 = st.columns(2)
   with col1:
        #  displaying recipients blood type distribution
        st.markdown(const.horizontal_line)
        st.markdown( const.heading_12)
        btvalues = recipients[const.bloodtype].value_counts().rename(const.sub_heading_23)
        st.write(pd.DataFrame(btvalues).T)
   with col2:
        viz.plot_pie(recipients, const.bloodtype,const.graph_title_4 ,const.color_sequence)


   st.markdown(const.horizontal_line)
   st.markdown(const.heading_13)
   col1, col2 = st.columns(2)
   with st.container():
       # displaying recipient's compatibility distribution
        values = recipients[const.hasBloodCompatibleDonor].value_counts().rename(const.sub_heading_24)
        with col1:
            st.write(pd.DataFrame(values).T)
        with col2:
            viz.plot_pie(recipients, const.hasBloodCompatibleDonor,const.graph_title_5 ,const.color_sequence)

   col1, col2 = st.columns([1,3])
   with col1:
       # cPRA distribution in recipients
         st.markdown(const.horizontal_line)
         st.markdown(const.heading_14 )

   with st.container():
        des = pd.to_numeric(recipients[const.cPRA]).describe().to_dict()
        des['median'] = recipients[const.cPRA].median()
        with col1:
            st.dataframe(list(des.items()))
        with col2:
            viz.plot_histogram(recipients,const.cPRA,const.graph_title_6,const.color_sequence)

   with st.container():
       # Filtering Recipients
        filter_data_recipients(recipients)

def filter_data_recipients(recipients):
    st.markdown(const.horizontal_line)

    st.markdown( const.heading_15)

    cPRA_low =0.0
    cPRA_high =0.0
    bloodtype_choices = 'A'
    Compatibility_choices = True
    finaldisplay_rec = None
    cPRA_min = recipients[const.cPRA].min()
    cPRA_max = recipients[const.cPRA].max()

    l = []
    for i in recipients[const.hasBloodCompatibleDonor]:
        l.append(str(i))
    x = recipients.copy()
    x[const.hasBloodCompatibleDonor] = l

    col1, col2 = st.columns(2)
    with col1:
        st.write(const.filter_heading_13)
        with st.form(const.filter_heading_14):

            cPRA_low = st.number_input(const.filter_heading_15, min_value=cPRA_min, max_value=cPRA_max, value = cPRA_min)
            cPRA_high = st.number_input(const.filter_heading_16,min_value=cPRA_min, max_value=cPRA_max, value =cPRA_max)
            bloodtype_choices = (st.selectbox(const.filter_heading_4,['A','O','AB','A','None'], index = 4))
            Compatibility_choices = (st.selectbox(const.filter_heading_17,['True','False','None'], index = 2))

            submit_rec_filter = st.form_submit_button(const.filter_heading_18)

            if(submit_rec_filter):
                if bloodtype_choices != 'None' and Compatibility_choices != 'None':
                    finaldisplay_rec = recipients[
                        ((recipients[const.cPRA] >= cPRA_low) & (recipients[const.cPRA] <= cPRA_high)) &
                        (recipients[const.bloodtype] == str(bloodtype_choices)) &
                        (x[const.hasBloodCompatibleDonor] == (Compatibility_choices))
                        ]
                elif bloodtype_choices == 'None' and Compatibility_choices == 'None':
                    finaldisplay_rec = recipients[
                        ((recipients[const.cPRA] >= cPRA_low) & (recipients[const.cPRA] <= cPRA_high))
                        ]
                elif bloodtype_choices != 'None' and Compatibility_choices == 'None':
                    finaldisplay_rec = recipients[
                        ((recipients[const.cPRA] >= cPRA_low) & (recipients[const.cPRA] <= cPRA_high)) &
                        (recipients[const.bloodtype] == str(bloodtype_choices))
                        ]
                elif bloodtype_choices == 'None' and Compatibility_choices != 'None':
                    finaldisplay_rec = recipients[
                        ((recipients[const.cPRA] >= cPRA_low) & (recipients[const.cPRA] <= cPRA_high)) &
                        (x[const.hasBloodCompatibleDonor] == (Compatibility_choices))
                        ]

    with col2:
        if finaldisplay_rec is not None:
            st.markdown(const.filter_heading_19)
            st.write(const.filter_heading_8 + str(len(finaldisplay_rec)))
            st.write( const.filter_heading_20+ str(cPRA_low) +' to ' + str(cPRA_high) )
            st.write(const.filter_heading_10 + bloodtype_choices)
            st.write(const.filter_heading_21 +  Compatibility_choices )

            st.dataframe(finaldisplay_rec)
