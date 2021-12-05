import streamlit as st
import pandas as pd
import pydeck as pdk
from hydralit import HydraApp
from hydralit import HydraHeadApp


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
    subdf = subdf[["longitude", "latitude",
                   "address", "n_killed", "n_injured"]]
    subdf.dropna(inplace=True)
    return subdf


@st.cache
def load_date_subset(df, date):
    subdf = df[df['date'] <= date].copy()
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
        self.df_unique_name = dict()

    def preprocess(self) -> None:
        # fill nan and create new map column
        self.df['participant_type'] = self.df['participant_type'].fillna("NA")
        self.df['participant_type_map'] = self.df['participant_type'].apply(
            lambda x: get_user_mapping(x))
        self.df['participant_age'] = self.df['participant_age'].fillna("NA")
        self.df['participant_age_map'] = self.df['participant_age'].apply(
            lambda x: get_user_mapping(x))
        self.df['participant_age_group'] = self.df['participant_age_group'].fillna(
            "NA")
        self.df['participant_age_group_map'] = self.df['participant_age_group'].apply(
            lambda x: get_user_mapping(x))
        self.df['participant_gender'] = self.df['participant_gender'].fillna(
            "NA")
        self.df['participant_gender_map'] = self.df['participant_gender'].apply(
            lambda x: get_user_mapping(x))
        # get unique name
        for name in ['participant_type_map', 'participant_age_group_map', 'participant_gender_map']:
            self.df_unique_name[name] = get_unique_name(self.df, name)

        return

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

    app.add_app("🐙Home1", app=MainApp())
    app.add_app("Home2", app=MainApp())

    complex_nav = {
        'Home-A': ['🐙Home1'],
        'Home-B': ['Home2'],
    }
    app.run(complex_nav)
