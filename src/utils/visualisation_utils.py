import plotly
import plotly.graph_objects as go
import seaborn as sn
import altair as altair
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from utils import constants as const

# All the fuctions, produces the graph on the UI
def plot_altair_bar(a,title,x, y, color):
    p = altair.Chart(a, title = title).mark_bar().encode(
    x = x,
    y = y,
    tooltip = [x,y],
    color = altair.value(color)
    )
    p = p.properties(
     width = altair.Step(80)
    )
    st.write(p)

def plot_pie(df, names, title, color):
    fig = px.pie(df,  names = names,title = title ,
    color_discrete_sequence = color)
    fig.update_layout(legend=dict(
    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
    title_font_size= 15)
    st.plotly_chart(fig, use_container_width=True)

def plot_histogram(df,x,title,color):
    fig = px.histogram(df, x=x,title = title , color_discrete_sequence = color)
    fig.update_layout(legend=dict(
    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
    title_font_size= 15)
    st.plotly_chart(fig, use_container_width=True)

def plot_mat_pie(values,color,label):
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values,  colors = color,
    autopct = '%1.1f%%',
    textprops={ 'color':'white'})

    ax.legend(wedges, label,
     loc="center left",
     bbox_to_anchor=(1, 0, 0.5, 1), mode = 'expand')

    st.pyplot(fig,transparent = True)


def plot_bar_chart(df,x,y,title,color):

    fig = px.bar(df, x=x, y=y,title = title,  color_discrete_sequence = color)
    fig.update_layout(legend=dict(
    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
    title_font_size= 17)

    st.plotly_chart(fig,use_container_width=True)

def plot_bar_chart_2(df,x,y,title,color_map):

    fig = px.bar(df, x=x, y=y,
    title= title,
    color_discrete_map = color_map)
    fig.update_layout(legend=dict(
    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
    title_font_size= 15)

    st.plotly_chart(fig,use_container_width=True)


def plot_go_trace(random_x,random_y0,random_y1,random_y2, name,title,x_title,y_title):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                            mode='lines',
                            name=name[0],
                            line = dict(color = '#e64d00')))
        fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                            mode='lines',
                            name=name[1],
                            line = dict(color ='#cc0044')))
        fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                            mode='lines', name=name[2],
                            line = dict(color = '#800040')))
        fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title)

        st.plotly_chart(fig, use_container_width=True)

def plot_correlation_matrix(corrMatrix):
    fig = plt.figure(figsize=(10, 4))
    sn.heatmap(corrMatrix, annot = True)
    st.pyplot(fig,use_container_width=True)

def plot_scatter_plot(df,x,y,title):
    fig = px.scatter(df,x = x,
    y = y,
    title = title ,
    color_discrete_sequence = const.color_sequence )
    fig.update_layout(legend=dict(
    orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),
    title_font_size= 15)
    st.plotly_chart(fig, use_container_width=True)

def plot_go_trace2(random_x,random_y0,random_y1, name,title,x_title,y_title):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                            mode='lines',
                            name=name[0],
                            line = dict(color = '#e64d00')))
        fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                            mode='lines',
                            name=name[1],
                            line = dict(color ='#cc0044')))

        fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title)

        st.plotly_chart(fig, use_container_width=True)
