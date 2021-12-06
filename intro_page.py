import streamlit as st
from hydralit import HydraHeadApp
from utils import *


class AppIntro(HydraHeadApp):
    def __init__(self) -> None:
        self.MText1 = """
                      Gun violence has always been a big problem here in States and 
                      thousands of people's lives have been threaten and taken because of gun shoots.        
                      Recently, a student from The University of Chicago has been murdered on a street 
                      in Hyde Park, just a few blocks from the campus, which made us feel sorry and 
                      gave us a big shock.
        """

        self.image1 = 'resources/i1.png'

        self.ZhengStory = """
        Zheng — like many of those in the crowd, including Cai — was from China. He had recently graduated with a master’s degree in statistics from the University of Chicago after completing a bachelor’s at the University of Hong Kong. He sent out his resume to find work as a data scientist, possibly in California, maybe even Silicon Valley, Cai said. He had written a book on statistics and hosted a blog on WeChat with at least 3,000 followers.
        
        And Zheng was the third student or recent graduate from the university to have been fatally shot in Chicago within a year: two in Hyde Park, one on the Green Line. He was the second victim who was an international student from China. These deaths, while unrelated, brought Chicago’s biggest problem close to the students, especially those who grew up in countries where gun violence is nonexistent.
        """

        self.image_influence = "resources/intro_who_is_next.jpeg"
        self.influence = """
        The university faculty, staff and students all agree that the violence should stop, but how to get there is where the community divides.
        
        A letter to the president and provost — signed by almost 350 faculty and staff members — bolded and underlined “Anti-violence should be made TOP priority at the University.” The letter explained that they wanted the university’s police force to expand its borders, and to increase surveillance and security. They wanted more shuttle routes for students, and for the university to design a committee to address violence in the neighborhood. Their last demand was for the university to engage with the South Side community to create a long-term plan.
        
        “These tragedies have been happening right on and around campus, and we are hearing of gun robberies on a weekly basis!” the letter read. “As educators, parents, and community members, we are deeply disturbed and outraged. We are no longer certain if our campus allows students, staff, and faculty to study, work, and live safely. We are experiencing an existential crisis.”
        
        On Tuesday, a U. of C. statement acknowledged receipt of the letter.
        
        Students, including many in the university’s international Chinese community, held a rally to voice their own demands.
        
        At least 200 students gathered Tuesday at the campus’s Main Quadrangle. Many expressed how they no longer felt safe on the campus and could no longer recommend that other Chinese students apply to the U. of C., despite its prestige. Their lives were not worth the diploma, they said.
        """

        self.CareNotCops = """
        Last summer, a student campaign called #CareNotCops held protests in Hyde Park, advocating to defund the University of Chicago Police Department and the Chicago Police Department.
        
        Students connected with the campaign also recently wrote a letter to the president and provost, saying in part that gun violence is not new and that the university “must first dismantle racist systems and begin the process of reparation, on the terms of historically harmed Black communities.”
        
        Signed by at least 330 students, alumni, neighbors and faculty members, the letter added that policing is the perpetrator of violence, not the solution. The group recently held its own rally, with at least 50 people in attendance.
        """

        self.MText2 = """
Depressed by this news, we looked into some reports and found some surprising data:    
"At least 3,909 people have been shot this year in Chicago, an increase of almost 9% compared 
to the same point in 2020 and 69% compared to 2019."

It is at this moment, we decide to do a project that explores the gun violence in the U.S. and 
analysis its distribution on the following dimensions:

1. The Geographical Distribution.

2. The Suspencts' Feature Distribution.
    - Is male or female more easily get involved in gun violence as a suspect?
    - Is male or female more easily to be a victim?
    - What is the age distribution of suspects and victims?
    - What is the survival rate of gun violence?
    - Is gun violence seasonal?

3. The Victims' Feature Distribution.

4. The code details about the preprocess of the dataset.
        """

        self.dataset = """
Our dataset get from the Kaggle: this dataset aims to change that; they make a record of more than 260k gun violence incidents, with detailed information about each incident, available in CSV format. They hope that this will make it easier for data scientists and statisticians to study gun violence and make informed predictions about future trends.

The CSV file contains data for all recorded gun violence incidents in the US between January 2013 and March 2018, inclusive.
        """

    def run(self):
        st.title("Introduction - Motivation Of The Project")
        st.header("Background", anchor=None)
        st.write(self.MText1)
        st.image(self.image1, width=700, caption="U. of C. staff members, students and friends of Zheng — many of them \
                                       holding bouquets of flowers — stopped by a memorial in the 1000 block of East 54th street Wednesday evening. \
                                       Madeline Kenney/Sun-Times")

        st.header("After the Accident", anchor=None)
        st.write(self.ZhengStory)

        st.header("This Ripple Has Gone International", anchor=None)
        st.image(self.image_influence, width=700,
                 caption="Students rally on Nov. 16, 2021, to call attention to recent violence surrounding the University of Chicago campus.")
        st.write(self.influence)

        st.header("Different Calls for Justice", anchor=None)
        st.write(self.CareNotCops)

        st.header("Our Project", anchor=None)
        st.markdown(self.MText2)

        st.header("The dataset", anchor=None)
        st.write(self.dataset)

        st.subheader("Source")
        st.markdown("Chicago SunTimes: [‘Please, God, give me my angel back’: Mother joins others to mourn murdered U of C grad](https://chicago.suntimes.com/2021/11/18/22789762/please-god-give-me-my-angel-back-mother-others-mourn-murdered-u-of-c-grad-shaoxiong-dennis-zheng)")
        st.markdown("Chicago Tribune: [‘We’re all afraid of death’: A tragic shooting sparks a search for solutions at University of Chicago, amid divided opinions on policing](https://www.chicagotribune.com/news/breaking/ct-university-of-chicago-hyde-park-violence-solutions-20211122-7nkgl4x655hrnmvmu7antkrxjq-story.html)")
        st.markdown(
            "Kaggle: [Gun Violence Data](https://www.kaggle.com/jameslko/gun-violence-data)")
        add_sidebar()
