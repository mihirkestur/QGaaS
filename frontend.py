import streamlit as st
st.set_page_config(page_title='QGaaS', layout = 'wide', initial_sidebar_state = 'auto')

with st.spinner(text="Loading dependencies...."):
    import model
    import media_to_text
    import extract_text
    import os

message = st.sidebar.text_area("Enter the text", height=200)
file = st.sidebar.file_uploader("Upload Video/Audio/Text", type=["mp4", "txt", "wav"])

if file is not None:
    filetype = {file.type}
    if filetype == {'video/mp4'} or filetype == {'text/plain'} or filetype == {'audio/wav'}:
        with open(os.path.join("./uploads", file.name),"wb") as f: 
            f.write(file.getbuffer())         
            st.sidebar.success("File Saved!")
        

if(st.sidebar.button('Obtain questions')):
    result = message.title()

    if(result is not None):
        data = " ".join(message.split("\n")).split(".")
        for i in data[:-1]:
            st.write(i)
            st.write(model.get_questions(i)[0][0])
            
    if(file is not None):
        saved_media_path = f"./uploads/{file.name}"
        if(filetype == {"audio/wav"}):
            pass
        elif(filetype == {"video/mp4"}):
            with st.spinner(text = f"Obtaining questions for video: {file.name}"):
                transcript = media_to_text.obtain_transcript(saved_media_path)
                for i in transcript:
                    st.write(i)
                    st.write(model.get_questions(i)[0][0])
                text_from_vid = extract_text.get_text_from_vid(saved_media_path)
                for i in text_from_vid:
                    st.write(i)
                    st.write(model.get_questions(i)[0][0])

        elif(filetype == {"text/plain"}):
            with st.spinner(text = f"Obtaining questions for text in file: {file.name}"):
                text_file = open(saved_media_path, 'r')
                data = " ".join(text_file.read().split("\n")).split(".")
                for i in data[:-1]:
                    st.write(i)
                    st.write(model.get_questions(i)[0][0])
                text_file.close()
        else:
            pass