import streamlit as st
    
def add_sidebar():
    st.sidebar.subheader("Feedbacks")
    st.sidebar.text_area(label="Share your thoughts here:")
    st.sidebar.button("Submit")
    
    st.sidebar.subheader("Contacts")
    st.sidebar.markdown("Tianyi Sun, <tsun2@andrew.cmu.edu>")
    st.sidebar.markdown("Yufan Song, <yufans@andrew.cmu.edu>")
    st.sidebar.markdown("YunXuan Xiao, <yunxuan2@andrew.cmu.edu>")
    st.sidebar.markdown("Zhouyang Li, <zhouyanl@andrew.cmu.edu>")