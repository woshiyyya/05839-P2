import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

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
def city_list(df):
    return sorted(list(df['city_or_county'].unique()))

@st.cache
def load_city_subset(df, city):
    subdf = df[df['city_or_county'] == city].copy()
    subdf = subdf[["longitude", "latitude", "address", "n_killed", "n_injured"]]
    subdf.dropna(inplace=True)
    return subdf

class AppLayout:
    def __init__(self) -> None:
        self.df = load_dataset()
    
    def make_country_map(self):
        geo_df = load_geo_subset(self.df)
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
    
    def make_city_map(self, select_city):
        city_df = load_city_subset(self.df, select_city)
        print(city_df)
        init_lng = city_df["longitude"].median()
        init_lat = city_df["latitude"].median()
        print(select_city, init_lng, init_lat)
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
            tooltip={"text": "{address}\nn_killed={n_killed}\nn_injured={n_injured}"}
            )
        )

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("U.S. Gun Shots")
    app = AppLayout()    
    app.make_country_map()

    select_city = st.selectbox(label='City', options=city_list(app.df))
    app.make_city_map(select_city)
    

