import streamlit as st
import pandas as pd
import pydeck as pdk
import datetime
from hydralit import HydraApp
from hydralit import HydraHeadApp
from preprocess_page import *
from IntroductionPage import *

@st.cache
def load_dataset():
    df = pd.read_csv("data.csv")
    df = df[pd.notnull(df['longitude']) & pd.notnull(df['latitude'])]
    return df


@st.cache
def load_geo_subset(df):
    geo_df = df[["longitude", "latitude"]]
    geo_df.dropna(inplace=True)
    return geo_df

@st.cache
def load_date_subset(df, date):
    subdf = df[df['date'].str.contains(date[:7])].copy()
    return subdf


@st.cache
def city_list(df):
    return sorted(list(df['city_or_county'].unique()))


@st.cache
def load_city_subset(df, city):
    subdf = df[df['city_or_county'] == city].copy()
    subdf = subdf[["longitude", "latitude",
                   "address", "n_killed", "n_injured"]]
    subdf.dropna(inplace=True)
    return subdf


class AppLayout:
    def __init__(self) -> None:
        self.df = load_dataset()

    def make_country_map(self):
        geo_df = load_geo_subset(self.df)
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
        col1, _ = st.columns([4, 1])
        with col1:
            select_city = st.selectbox(
                label='City', options=city_list(self.df))
            select_date = st.sidebar.slider(
                label="Choose time",
                value=datetime.date(2018, 3, 31), key="all_data", min_value=datetime.date(2013, 1, 1), 
                        max_value=datetime.date(2018, 3, 31)).strftime("%Y-%m-%d")
                
            city_df = load_city_subset(load_date_subset(self.df, select_date), select_city)
            if len(city_df) == 0:
                city_df = load_city_subset(self.df, select_city)
                
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


class MainApp(HydraHeadApp):
    def __init__(self) -> None:
        self._app = AppLayout()
        
        self.CouText = """
        According to the map, we can see that gun violences' clusters mainly locate on the west coast and east coast.
        The violences are more frequent in the following states:
        
        1. ILL
        
        2. MD
        
        3. N.J.
        
        Especially, Chicago is more severe than other cities.
        """
        
        self.CityText1 = """
        Here we want to explore: Is the frequencies of violences related to seasons?
        
        We propose that when it's spring/summer, there'll be more gun violences than in winter.
        
        To test our hypothesis, we build a time-select bar in the left side. You can try to see if our hypothesis stands.
        
        """
        
        self.CityText2 = """
        As you can see, our hypothesis does not apply to every city.
        
        However, in eastern cities, there're generally more gun violences in summer than in winter.
        
        It's probably because people tend to stay at home longer when it's winter, so there're less chances that 
        people will be shot on street outside.
        """
        

    def run(self):
        st.header("Gun Shots Distribution Over The Country")
        
        
        
        self._app.make_country_map()
        st.write(self.CouText)
        
        
        st.header("Gun Shots Distribution Over Cities")
        st.write(self.CityText1)
        self._app.make_city_map()
        st.write(self.CityText2)


if __name__ == "__main__":
    # st.set_page_config(layout="wide")
    over_theme = {'txc_inactive': '#FFFFFF'}
    app = HydraApp(
        title='Test Hydra APP',
        favicon="🐙",
        # hide_streamlit_markers=True,
        banner_spacing=[5, 30, 60, 30, 5],
        use_navbar=True,
        navbar_sticky=True,
        navbar_animation=True,
        navbar_theme=over_theme,
    )
    
    app.add_app("Introduction", app=AppIntro())
    app.add_app("Geographical Distribution", app=MainApp())
    app.add_app("Preprocess Of the Dataset", app=AppPreprocessPage())
    app.add_app("Presentation", app=AppVideoPage())
    app.add_app("Contacts", app=AppContactPage())

    complex_nav = {
        "Introduction": ['Introduction'],
        'Preprocess Of the Dataset': ['Preprocess Of the Dataset'],
        'Geographical Distribution': ['Geographical Distribution'],
        'Presentation': ['Presentation'],
        'Contacts': ['Contacts'],
    }
    app.run(complex_nav)
