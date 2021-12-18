import streamlit as st
import pandas as pd
import numpy as np
from utils import constants as const

# this function calculates no. of chains and no. of cycles in the given instance
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

      a = payload.get(const.output).get(const.all_cycles).get(str(i)).get(const.cycle)
      df = pd.DataFrame(a)

      c2,c3,sc,lc,type = per_cycle(df)

      cycle_2.append(c2)
      cycle_3.append(c3)
      s_chain.append(sc)
      l_chain.append(lc)

    return cycle_2, cycle_3, s_chain, l_chain

# This function calculates the given cycle type
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
             type = const.short_chains
         else:
             c2 = 1
             type = const.two_cycles
    elif rows == 3:
        if is_altruistic:
            lc = 1
            type = const.long_chains
        else:
            c3 = 1
            type =  const.three_cycles
    return c2,c3,sc,lc,type

# This fucntione counts the number of matches a donor has
def count_matches(row):
  if isinstance(row[const.matches], list) :
    return int(len(row[const.matches]))
  else:
    return 0

def render_donor(x,i, donors):
    a,b,c, = st.columns([1,1,2])
    with a:
        st.markdown(const.sub_heading_17 + str(i))
        st.markdown( const.sub_heading_18 + str(donors[const.source].iloc[i]))
        st.markdown( const.sub_heading_19 + str(donors[const.dage].iloc[i]))

    with b:
        st.markdown( const.sub_heading_20 + str(donors[const.bloodtype].iloc[i]))
        # st.markdown(""" **altruistic : ** """ + str(x['altruistic']))
        st.markdown( const.sub_heading_21 + str(donors[const.matches_count].iloc[i]))
    with c:
        if donors[const.matches_count].iloc[i] != 0:
            st.write(const.Matches)
            st.dataframe(donors[const.matches].iloc[i], width = 300, height = 170)

# This funciton counts the multiple sources of donors
def count_sources(donor):
      x = donor['sources'].value_counts(dropna = 'True')
      y = x.where(x > 1).value_counts(dropna = 'True').sum()
      return y

# This function counts bloodtype distribution for one donor
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

# This fucntions count comaptiblity in a set of given recipients
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

def calculate_cycles_chains_stored(payload,ids):
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

# def per_cycle(df):
#     c2 = 0
#     c3 = 0
#     sc = 0
#     lc = 0
#     is_altruistic = False
#     rows = len(df)
#     type = ''
#     if 'a' in df:
#         is_altruistic = True
#
#     if rows == 2:
#          if is_altruistic:
#              sc = 1
#              type = 'Short chain'
#
#          else:
#              c2 = 1
#              type = 'Two cycle'
#     elif rows == 3:
#         if is_altruistic:
#             lc = 1
#             type = 'Long chain'
#         else:
#             c3 = 1
#             type = 'Three cycle'
#     return c2,c3,sc,lc,type
