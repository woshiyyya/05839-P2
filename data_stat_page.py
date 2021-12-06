import streamlit as st
from hydralit import HydraHeadApp
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import os

from utils import add_sidebar

MAX_AGE = 110
SURVIVAL_RATE_MAX_DISPLAY_AGE = 85
VICTIM_DATA_PATH = "data/victim_data.csv"
SUSPECT_DATA_PATH = "data/suspect_data.csv"
GENDERDIST_CACHE_PATH = "data/gender_dist.pkl"
SURVIVAL_CACHE_PATH = "data/survival_rate.pkl"

class DataStatApp(HydraHeadApp):
    def __init__(self) -> None:
        self._victim_data = pd.read_csv(VICTIM_DATA_PATH)
        self._victim_data['date'] = pd.to_datetime(self._victim_data['date'])
        self._suspect_data = pd.read_csv(SUSPECT_DATA_PATH)
        self._suspect_data['date'] = pd.to_datetime(self._suspect_data['date'])

        self._title = "Data Statistics"

        self.research_questions_subtitle = "Research Questions"
        self._reseach_quesitons = '''Here is a list of research questions that we want to explore in the following Data Statistics:
- Is male or female more easily get involved in gun violence as a suspect?
- Is male or female more easily to be a victim?
- What is the age distribution of suspects and victims?
- What is the survival rate of gun violence?
- Is gun violence seasonal?
        '''

        self._gender_distribution_subtitle = "Gender Distribution"
        self._survival_rate_subtitle = "Survival Rate"
        self._case_number_subtitle = "Case Number"

        self._gender_distribution_content_1 = """The above two plots are about the victim and suspect gender and age distribution. It is quite obvious that in both the suspect and victim gender distribution plot, the number of males is significantly more than the number of females. When it comes to suspect gender distribution, the number of males is significantly more than the number of females is somewhat we would expect. **However, the number of victims is also significantly more than the number of female victims is worth thinking about.** This may be due to the fact that gun violence always happens in areas that have more men than women or because women are less aggressive than men in general and therefore have a smaller probability of getting involved in gun violence. **There is also something worth noting is that there is a significant amount of cases that have suspects or victims younger than one-year-old.** Most of the cases that involve babies are due to the carelessness of parents who leave their babies along with guns. Here is one of those cases: https://www.mlive.com/news/grand-rapids/2016/10/2-year-old_firing_rifle_injure.html#incart_river_home"""
        self._gender_distribution_content_2 = """Another insight we got from the two plots is that although the age distribution is almost the same between male victims and female victims, the distribution is slightly different in suspects. It turns out that most male suspects have an age of 18 and 19 while most female suspects are in age around 23. This may suggest a different pattern of how crime probabilities relate to age between males and females."""

        self._survival_rate_content = """We also inspected the relationship between the survival rate and age among males and females. The survival rate is calculated using the number of victims who survived divided by the total number of victims. The relationship is in line with our common sense. The survival rate of males is slightly higher than the survival rate of females. And the survival rate is higher among young adults and lower among older people and children."""

        self._case_number_content = """There were some interesting discussions about whether crimes are easier to happen during hot seasons. So we visualized the relationship between the number of criminal cases and seasons. The plot above is calculated using 5 years of gun violence records and group them by their date. Criminal cases that have the same month and date but different years are also grouped together so we can see the relationship between seasons and crime numbers. **The plot shows that there is no clear relationship between the number of gun violence and seasons as the number of crimes is quite uniform,** which is aligns with the previous research conclusions: https://www.ojp.gov/ncjrs/virtual-library/abstracts/crime-seasonal. Maybe some further data analysis should be done to figure out the relationship between temperature and crime rates, but this needs weather data and is beyond the scope of this project."""

    def _gender_distribution(self) -> None:
        if os.path.exists(GENDERDIST_CACHE_PATH):
            with open(GENDERDIST_CACHE_PATH, 'rb') as fin:
                male_victim_age = pickle.load(fin)
                female_victim_age = pickle.load(fin)
                male_suspect_age = pickle.load(fin)
                female_suspect_age = pickle.load(fin)
                male_victim_distribution = pickle.load(fin)
                female_victim_distribution = pickle.load(fin)
                male_suspect_distribution = pickle.load(fin)
                female_suspect_distribution = pickle.load(fin)
        else:
            male_victim_age = []
            female_victim_age = []
            male_suspect_age = []
            female_suspect_age = []

            male_victim_num = [0 for i in range(MAX_AGE)]
            female_victim_num = [0 for i in range(MAX_AGE)]
            male_suspect_num = [0 for i in range(MAX_AGE)]
            female_suspect_num = [0 for i in range(MAX_AGE)]

            for index, row in self._victim_data.iterrows():
                victim_list = eval(row["victim_info"])
                for victim in victim_list:
                    if victim["age"] > MAX_AGE:
                        continue

                    if victim["gender"] == "Male":
                        male_victim_num[victim["age"]] += 1
                        male_victim_age.append(victim["age"])
                    elif victim["gender"] == "Female":
                        female_victim_num[victim["age"]] += 1
                        female_victim_age.append(victim["age"])

            for index, row in self._suspect_data.iterrows():
                suspect_list = eval(row["suspect_info"])
                for suspect in suspect_list:
                    if suspect["age"] > MAX_AGE:
                        continue
                    
                    if suspect["gender"] == "Male":
                        male_suspect_num[suspect["age"]] += 1
                        male_suspect_age.append(suspect["age"])
                    elif suspect["gender"] == "Female":
                        female_suspect_num[suspect["age"]] += 1
                        female_suspect_age.append(suspect["age"])

            male_victim_sum = sum(male_victim_num)
            female_victim_sum = sum(female_victim_num)
            male_suspect_sum = sum(male_suspect_num)
            female_suspect_sum = sum(female_suspect_num)

            male_victim_distribution = [num / male_victim_sum for num in male_victim_num]
            female_victim_distribution = [num / female_victim_sum for num in female_victim_num]
            male_suspect_distribution = [num / male_suspect_sum for num in male_suspect_num]
            female_suspect_distribution = [num / female_suspect_sum for num in female_suspect_num]
            
            with open(GENDERDIST_CACHE_PATH, 'wb') as fout:
                pickle.dump(male_victim_age, fout)
                pickle.dump(female_victim_age, fout)
                pickle.dump(male_suspect_age, fout)
                pickle.dump(female_suspect_age, fout)
                pickle.dump(male_victim_distribution, fout)
                pickle.dump(female_victim_distribution, fout)
                pickle.dump(male_suspect_distribution, fout)
                pickle.dump(female_suspect_distribution, fout)
                print("finished Dump Cache")
        

        male_victim_age_trace = go.Histogram(x=male_victim_age, name="male victim num")
        female_victim_age_trace = go.Histogram(x=female_victim_age, name="female victim num")
        male_suspect_age_trace = go.Histogram(x=male_suspect_age, name="male suspect num")
        female_suspect_age_trace = go.Histogram(x=female_suspect_age, name="female suspect num")

        male_victim_distribution_trace = go.Scatter(x=[i for i in range(MAX_AGE)], y=male_victim_distribution, mode='lines', line_shape='spline', line_smoothing=1.3, name='male victim distribution')
        female_victim_distribution_trace = go.Scatter(x=[i for i in range(MAX_AGE)], y=female_victim_distribution, mode='lines', line_shape='spline', line_smoothing=1.3, name='female victim distribution')
        male_suspect_distribution_trace = go.Scatter(x=[i for i in range(MAX_AGE)], y=male_suspect_distribution, mode='lines', line_shape='spline', line_smoothing=1.3, name='male suspect distribution')
        female_suspect_distribution_trace = go.Scatter(x=[i for i in range(MAX_AGE)], y=female_suspect_distribution, mode='lines', line_shape='spline', line_smoothing=1.3, name='female suspect distribution')
        
        victim_fig = make_subplots(specs=[[{"secondary_y": True}]])
        victim_fig.add_trace(male_victim_age_trace)
        victim_fig.add_trace(female_victim_age_trace)
        victim_fig.add_trace(male_victim_distribution_trace, secondary_y=True)
        victim_fig.add_trace(female_victim_distribution_trace, secondary_y=True)
        
        suspect_fig = make_subplots(specs=[[{"secondary_y": True}]])
        suspect_fig.add_trace(male_suspect_age_trace)
        suspect_fig.add_trace(female_suspect_age_trace)
        suspect_fig.add_trace(male_suspect_distribution_trace, secondary_y=True)
        suspect_fig.add_trace(female_suspect_distribution_trace, secondary_y=True)

        victim_fig.update_layout(title="Victim Gender and Age Distribution", barmode='overlay')
        victim_fig.update_yaxes(title_text="victim Number", secondary_y=False)
        victim_fig.update_yaxes(title_text="Victim Proportion", secondary_y=True)
        victim_fig.update_traces(opacity=0.75)
        suspect_fig.update_layout(title="Suspect Gender and Age Distribution", barmode='overlay')
        suspect_fig.update_yaxes(title_text="Suspect Number", secondary_y=False)
        suspect_fig.update_yaxes(title_text="Suspect Proportion", secondary_y=True)
        suspect_fig.update_traces(opacity=0.75)

        st.plotly_chart(victim_fig, use_container_width=True)
        st.plotly_chart(suspect_fig, use_container_width=True)

    def _survival_rate(self) -> None:
        if os.path.exists(SURVIVAL_CACHE_PATH):
            with open(SURVIVAL_CACHE_PATH, 'rb') as fin:
                male_survival_rate = pickle.load(fin)
                female_survival_rate = pickle.load(fin)
        else:
            male_survive_num = [0 for i in range(MAX_AGE)]
            female_survive_num = [0 for i in range(MAX_AGE)]
            male_victim_num = [0 for i in range(MAX_AGE)]
            female_victim_num = [0 for i in range(MAX_AGE)]

            for index, row in self._victim_data.iterrows():
                victim_list = eval(row["victim_info"])
                for victim in victim_list:
                    if victim["age"] > MAX_AGE:
                        continue
                    if victim["gender"] == "Male" and "Killed" not in victim["status"]:
                        male_survive_num[victim["age"]] += 1
                    elif victim["gender"] == "Female" and "Killed" not in victim["status"]:
                        female_survive_num[victim["age"]] += 1
                    if victim["gender"] == "Male":
                        male_victim_num[victim["age"]] += 1
                    elif victim["gender"] == "Female":
                        female_victim_num[victim["age"]] += 1
            
            male_survival_rate = [sum(male_survive_num[i-1:i+2]) / sum(male_victim_num[i-1:i+2]) if sum(male_victim_num[i-1:i+2]) > 0 else 0 for i in range(1, SURVIVAL_RATE_MAX_DISPLAY_AGE)]
            female_survival_rate = [sum(female_survive_num[i-1:i+2]) / sum(female_victim_num[i-1:i+2]) if sum(female_victim_num[i-1:i+2]) > 0 else 0 for i in range(1, SURVIVAL_RATE_MAX_DISPLAY_AGE)]

            with open(SURVIVAL_CACHE_PATH, "wb") as fout:
                pickle.dump(male_survival_rate, fout)
                pickle.dump(female_survival_rate, fout)
            
        male_survival_rate_trace = go.Scatter(x=[i for i in range(1, SURVIVAL_RATE_MAX_DISPLAY_AGE)], y=male_survival_rate, mode='lines', line_shape='spline', line_smoothing=1.3, name='male survival rate')
        female_survival_rate_trace = go.Scatter(x=[i for i in range(1, SURVIVAL_RATE_MAX_DISPLAY_AGE)], y=female_survival_rate, mode='lines', line_shape='spline', line_smoothing=1.3, name='female survival rate')
        
        fig = go.Figure()
        fig.add_trace(male_survival_rate_trace)
        fig.add_trace(female_survival_rate_trace)

        fig.update_layout(title="Survival Rate")

        st.plotly_chart(fig, use_container_width=True)

    def _case_number(self) -> None:
        case_num_per_date = self._victim_data[self._victim_data['date'] > datetime.datetime(2015, 1, 1)]['date']
        case_num_per_date = case_num_per_date.to_frame().reset_index()
        case_num_per_date['date'] = case_num_per_date['date'].dt.strftime('%m%d')

        case_num_per_date = case_num_per_date.groupby(['date']).size()

        case_num_per_date_trace = go.Scatter(x=case_num_per_date.index.tolist(), y=case_num_per_date.values.tolist(), mode='lines', line_shape='spline', line_smoothing=1.3, name='case number')
        
        fig = go.Figure()
        fig.add_trace(case_num_per_date_trace)
        
        fig.update_layout(title="Case Number", xaxis_title="Date")
        
        st.plotly_chart(fig, use_container_width=True)

    def run(self):
        st.title(self._title)
        st.header(self.research_questions_subtitle)
        st.markdown(self._reseach_quesitons)
        st.header(self._gender_distribution_subtitle)
        self._gender_distribution()
        st.markdown(self._gender_distribution_content_1)
        st.markdown(self._gender_distribution_content_2)
        st.header(self._survival_rate_subtitle)
        self._survival_rate()
        st.markdown(self._survival_rate_content)
        st.header(self._case_number_subtitle)
        self._case_number()
        st.markdown(self._case_number_content)
        add_sidebar()