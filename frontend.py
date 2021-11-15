import streamlit as st
st.set_page_config(page_title='QGaaS', layout = 'wide', initial_sidebar_state = 'auto')
message = st.text_area("Enter the text", height=200)

if(st.button('Obtain questions')):
    result = message.title()
    print(result)
    st.success("Saved")