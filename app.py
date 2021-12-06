from os import stat_result
from numpy import add
import streamlit as st
import pandas as pd
import pydeck as pdk
from hydralit import HydraApp
from hydralit import HydraHeadApp
from preprocess_page import *
from data_stat_page import *
from intro_page import *

from utils import add_sidebar
import plotly.graph_objects as go

@st.cache
def load_dataset():
    df = pd.read_csv("data/data.csv")
    df = df[pd.notnull(df['longitude']) & pd.notnull(df['latitude'])]
    df['date'] = df.apply(lambda x: int(x['date'].replace('-', '')), axis=1)
    return df


@st.cache
def load_geo_subset(df, start_date, end_date):
    geo_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    geo_df = geo_df[["longitude", "latitude"]]
    geo_df.dropna(inplace=True)
    return geo_df

@st.cache
def load_cities_subset(df, start_date, end_date):
    cities_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    cities = cities_df['city_or_county'].value_counts()[:20][::-1]
    return cities


@st.cache
def city_list(df):
    return list(df['city_or_county'].value_counts().index)


@st.cache
def load_city_subset(df, city, start_date, end_date):
    subdf = df[df['city_or_county'] == city].copy()
    subdf = subdf[(subdf['date'] >= start_date) & (subdf['date'] <= end_date)]
    subdf = subdf[["longitude", "latitude",
                   "address", "n_killed", "n_injured"]]
    subdf.dropna(inplace=True)
    return subdf

@st.cache
def load_date_subset(df, date):
    subdf = df[df['date'].str.contains(date[:7])].copy()
    return subdf


@st.cache
def get_user_mapping(element):
    if element == "NA":
        return {}
    mapping = {}
    for d in element.split("||"):
        try:
            key = d.split("::")[0]
            val = d.split("::")[1]
            if key not in mapping:
                mapping[key] = val
        except:
            pass
    return mapping


@st.cache
def get_unique_name(df, column_name):
    s = set()
    for item in df[column_name]:
        for k, v in item.items():
            s.add(v)
    return s
class AppLayout:
    def __init__(self) -> None:
        self.df = load_dataset()

    def make_country_map(self):
        geo_df = load_geo_subset(self.df, self.start_date, self.end_date)
        col1, _ = st.columns([4, 1])
        with col1:
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=37.76,
                    longitude=-95.8,
                    zoom=3,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        "HeatmapLayer",
                        data=geo_df,
                        get_position=["longitude", "latitude"],
                        opacity=0.5,
                        aggregation='MEAN',
                    )
                ],
            ))

    def make_city_map(self):
        select_city = st.selectbox(
            label='Choose a city:', options=city_list(self.df))
        city_df = load_city_subset(self.df, select_city, self.start_date, self.end_date)
        col1, col2 = st.columns([5, 2])
        with col1:
            init_lng = city_df["longitude"].median()
            init_lat = city_df["latitude"].median()
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=pdk.ViewState(
                    latitude=init_lat,
                    longitude=init_lng,
                    zoom=10,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',   # doc: https://pydeck.gl/gallery/scatterplot_layer.html
                        data=city_df,
                        get_position=["longitude", "latitude"],
                        get_color=[200, 30, 0, 160],
                        get_radius=70,
                        pickable=True
                    ),
                ],
                tooltip={
                    "text": "{address}\nn_killed={n_killed}\nn_injured={n_injured}"}
            )
            )
        with col2:
            cities = load_cities_subset(self.df, self.start_date, self.end_date)
            fig = go.Figure()
            fig.add_trace(go.Bar(x=cities, 
                                 y=cities.index, 
                                 orientation='h',
                                 marker=dict(
                                    color='rgba(246, 78, 139, 0.6)',
                                    line=dict(
                                        color='rgba(246, 78, 139, 1.0)',
                                        width=1))))
            fig.update_layout(title="Top 20 Most \"Dangerous\" Cities", 
                              xaxis=dict(
                                title_text="#Gun shots in 2013-2018"),
                              margin=dict(
                                    l=50,
                                    r=50,
                                    b=50,
                                    t=50,
                                ), width=400, height=550)
            st.plotly_chart(fig)
    
    def set_date_range(self, start_date, end_date):
        self.start_date = int(start_date.strftime("%Y%m%d"))
        self.end_date = int(end_date.strftime("%Y%m%d"))
            
class MainApp(HydraHeadApp):
    def __init__(self) -> None:
        self._app = AppLayout()

    def run(self):
        start_date, end_date = st.sidebar.slider(label="Choose time range",
                                        value=(datetime.date(2013, 1, 1), datetime.date(2018, 3, 31)), 
                                        key="all_data", 
                                        min_value=datetime.date(2013, 1, 1), 
                                        max_value=datetime.date(2018, 3, 31))
        self._app.set_date_range(start_date, end_date)
        add_sidebar()
        st.header("Geographical distribution of Gun Shots in the U.S.")
        self._app.make_country_map()
        st.header("City-wise Gun Shots Browser")
        self._app.make_city_map()
    


if __name__ == "__main__":
    # st.set_page_config(layout="wide")
    over_theme = {'txc_inactive': '#FFFFFF'}
    app = HydraApp(
        title='U.S. Gun Shots Analysis',
        favicon="🐙",
        # hide_streamlit_markers=True,
        banner_spacing=[5, 30, 60, 30, 5],
        use_navbar=True,
        navbar_sticky=True,
        navbar_animation=True,
        navbar_theme=over_theme,
    )

    app.add_app("Home", app=AppIntro())
    app.add_app("Geo Distribution", app=MainApp())
    app.add_app("Data Statistics", app=DataStatApp())
    app.add_app("Preprocess", app=AppPreprocessPage())
    app.add_app("Presentation", app=AppVideoPage())

    complex_nav = {
        'Home': ['Home'],
        'Geo Distribution': ['Geo Distribution'],
        'Data Statistics': ['Data Statistics'],
        'Preprocess': ['Preprocess'],
        'Presentation': ['Presentation'],
    }
    app.run(complex_nav)
