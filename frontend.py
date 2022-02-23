from difflib import context_diff
import streamlit as st
st.set_page_config(page_title='QGaaS', layout = 'wide', initial_sidebar_state = 'auto')


with st.spinner(text="Loading dependencies...."):
    import model
    import media_to_text
    import extract_text
    import rankings
    import os

st.header("QGaaS: Question Generation as a Service")

choice = st.sidebar.radio("Choose input media!", (
    "Video/Audio/Textfile",
    "Enter text!"
))

if(choice == "Video/Audio/Textfile"):
    file = st.sidebar.file_uploader("Upload Video/Audio/Textfile", type=["mp4", "txt", "wav"])
    if file is not None:
        filetype = {file.type}
        if filetype == {'video/mp4'} or filetype == {'text/plain'} or filetype == {'audio/wav'}:
            with open(os.path.join("./uploads", file.name),"wb") as f: 
                f.write(file.getbuffer())         
                st.sidebar.success("File saved successfully!")
else:
    message = st.sidebar.text_area("Enter the text!", height=100)

        
if(st.sidebar.button('Obtain questions!')):
    
    total_questions = 0
    if(choice == "Enter text!"):
        
        result = message.title()

        if(result is not None):
            progress_count = 0
            progress_bar = st.progress(progress_count)

            progress_count += 10
            progress_bar.progress(progress_count)

            data = " ".join(message.split("\n")).split(".")
            
            progress_count += 10
            progress_bar.progress(progress_count)

            data = rankings.RankContexts(data)
            
            progress_count += 10
            progress_bar.progress(progress_count)

            for i in range(len(data[:-1])):
                total_questions += 1
                progress_count = (30+int(70*(i+1)/(len(data[:-1]))))
                progress_bar.progress(progress_count)

                context = f'<h2 style="font-family:Courier; color:brown; font-size: 20px;">Context: {data[i]}</h2>'
                st.markdown(context, unsafe_allow_html=True)
                st.write(total_questions, model.get_questions(data[i])[0][0])
            
    elif(file is not None):
        saved_media_path = f"./uploads/{file.name}"
        
        if(filetype == {"video/mp4"}):
            with st.spinner(text = f"Obtaining questions for video: {file.name}"):
                progress_count = 0
                progress_bar = st.progress(progress_count)
                
                progress_count += 5
                progress_bar.progress(progress_count)

                transcript = media_to_text.obtain_transcript(saved_media_path)

                progress_count += 5
                progress_bar.progress(progress_count)

                text_from_vid = extract_text.get_text_from_vid(saved_media_path)

                progress_count += 10
                progress_bar.progress(progress_count)

                contexts_speech = rankings.RankContexts(transcript)
                contexts_slide = rankings.RankContexts(text_from_vid)

                contexts = contexts_speech + contexts_slide
                progress_count += 10

                progress_bar.progress(progress_count)
                
                for i in range(len(contexts)):
                    total_questions += 1
                    progress_count = (30+int(70*(i+1)/(len(contexts))))
                    progress_bar.progress(progress_count)
                    context = f'<h2 style="font-family:Courier; color:brown; font-size: 20px;">Context: {contexts[i]}</h2>'
                    st.markdown(context, unsafe_allow_html=True)
                    st.write(total_questions, model.get_questions(contexts[i])[0][0])

        elif(filetype == {"text/plain"}):
            with st.spinner(text = f"Obtaining questions for text in file: {file.name}"):
                progress_count = 0
                progress_bar = st.progress(progress_count)

                text_file = open(saved_media_path, 'r')

                progress_count += 10
                progress_bar.progress(progress_count)

                data = " ".join(text_file.read().split("\n")).split(".")

                progress_count += 10
                progress_bar.progress(progress_count)

                data = rankings.RankContexts(data)

                progress_count += 10
                progress_bar.progress(progress_count)

                for i in range(len(data[:-1])):
                    total_questions += 1
                    progress_count = (30+int(70*(i+1)/(len(data[:-1]))))
                    progress_bar.progress(progress_count)

                    context = f'<h2 style="font-family:Courier; color:brown; font-size: 20px;">Context: {data[i]}</h2>'
                    st.markdown(context, unsafe_allow_html=True)
                    st.write(total_questions, model.get_questions(data[i])[0][0])
                text_file.close()
        
        elif(filetype == {"audio/wav"}):
            pass
        else:
            pass