""" Author: Jarrod Cruz
    Description: Dashboard using streamlit and plotly in python
"""
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import os 
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="spotify", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Spotify EDA")
st.markdown('')


#fl = st.file_uploader(':file_folder: Upload a file', type=(['csv']))
#if fl is not None:
#    filename = fl.name
#   st.write(filename)
#   df = pd.read_csv(filename, encoding='ISO-8859-1')
#else:
df = pd.read_csv('spotify-2023.csv', encoding='latin-1')
df.dropna(inplace=True)
df= df.drop(574)

df["streams"] = df["streams"].astype(np.int64)

df.sort_values(by=['released_year'])

mts = {1: 'Jan.', 2: 'Feb.', 3: 'Mar.',
       4: 'Apr.', 5: 'May', 6: 'Jun.',
       7: 'Jul..', 8: 'Aug.', 9: 'Sep.',
       10: 'Oct.', 11: 'Nov.', 12: 'Dec.'}

st.sidebar.header("Select filters: ")
released_year = st.sidebar.multiselect("Select song year", 
                                     options = sorted(df['released_year'].unique(), reverse=True),
                                     default= [2016,2017,2018,2019,2020,2021,2022,2023]
                                     )


released_month = st.sidebar.multiselect("Select song month", 
                                     options = sorted(df["released_month"].unique()),
                                     default = [1,2,3,4,5,6,7,8,9,10,11,12]
                                     )

musical_key = st.sidebar.multiselect("Select key of the song", 
                                     options = df["key"].unique(),
                                     default = df["key"].unique()
                                     )

df_selected = df.query(
    "released_year == @released_year & released_month == @released_month & key == @musical_key"
)

st.markdown('##')

left, mid, right = st.columns(3)

# show most popular artist in selected categories
# need to sort by streams 
with left:
    st.subheader("left")
    
    

with mid:
    st.subheader("mid")
with right:
    st.subheader("right")

st.markdown("---")


# bar chart for top 5 artists
artists = df_selected.groupby('artist(s)_name')['streams'].sum().sort_values(ascending=False).head()

fig_top_artists = px.bar(
        artists,
        x= artists.values,
        y= artists.index,
        orientation="h",
        title="<b>Top 5 Artists</b>",
        template="plotly_white",


    )
fig_top_artists.update_layout(
        xaxis_title ="Streams (in billions)",yaxis_title="Artist(s) Name",
        yaxis={'categoryorder':'total ascending'},
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)))

left2, right2 = st.columns(2)
left2.plotly_chart(fig_top_artists,use_container_width=True)
st.markdown("---")
