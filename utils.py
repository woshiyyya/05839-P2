import streamlit as st
    
def add_sidebar():
    st.sidebar.subheader("Feedbacks")
    st.sidebar.text_area(label="Share your thoughts here:")
    st.sidebar.button("Submit")
    
    st.sidebar.subheader("Authors:")
    st.sidebar.markdown("**Interactive DS Group 23**")
    st.sidebar.markdown("Tianyi Sun, <tsun2@andrew.cmu.edu>")
    st.sidebar.markdown("Yufan Song, <yufans@andrew.cmu.edu>")
    st.sidebar.markdown("Yunxuan Xiao, <yunxuan2@andrew.cmu.edu>")
    st.sidebar.markdown("Zhouyang Li, <zhouyanl@andrew.cmu.edu>")
    
    st.sidebar.subheader("Github Repo:")
    st.sidebar.markdown("[https://github.com/woshiyyya/05839-P2](https://github.com/woshiyyya/05839-P2)")