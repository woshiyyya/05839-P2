import streamlit as st
from hydralit import HydraHeadApp


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

        self.MText2 = """
                       Depressed by this news, we looked into some reports and found some surprising data:    
                       "At least 3,909 people have been shot this year in Chicago, an increase of almost 9% compared 
                       to the same point in 2020 and 69% compared to 2019."
                       
                       It is at this moment, we decide to do a project that explores the gun violence in the U.S. and 
                       analysis its distribution on the following dimensions:
                        
                       1. The Geographical Distribution.
                       
                       2. The Suspencts' Feature Distribution.
                       
                       3. The Victims' Feature Distribution.           
        """

        self.MText3 = """
                       
        """

    def run(self):
        st.title("Introduction")
        st.header("Motivation Of The Project", anchor=None)
        st.write(self.MText1)
        st.image(self.image1, width=1100, caption="U. of C. staff members, students and friends of Zheng — many of them \
                                       holding bouquets of flowers — stopped by a memorial in the 1000 block of East 54th street Wednesday evening. \
                                       Madeline Kenney/Sun-Times")
        st.write(self.MText2)

if __name__ == "__main__":
    Intro_app = AppIntro()
    Intro_app.run()