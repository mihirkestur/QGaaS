DEBUG = 0
# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import moviepy.editor as mp
from pydub.utils import make_chunks

"""
input: path to Audio/Video file
output: Transcript (text)
"""
def obtain_transcript(path):
    # create a speech recognition object
    r = sr.Recognizer()
    # Check if its audio or video file
    file_extension = path.split('/')[-1].split('.')
    if(file_extension[1] == "mp4"):
        file_extension[1] = "wav"
        file_extension = ".".join(file_extension)
        wav_path = path.split('/')
        wav_path[-1] = file_extension
        wav_path = '/'.join(wav_path)
        # Convert video to audio
        clip = mp.VideoFileClip(path) 
        clip.audio.write_audiofile(wav_path)
        # open the audio file using pydub
        sound = AudioSegment.from_wav(wav_path)  
        os.remove(wav_path) 
    elif(file_extension[1] == "wav"):
        sound = AudioSegment.from_wav(path) 

    """
    Splitting the large audio file into chunks and apply speech recognition on each of these chunks
    """
    #chunks = make_chunks(sound, 10000)
    
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 1000,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=1000,
    )
    
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error with file:", str(e))
            else:
                text = f"{text.capitalize()}. "
                if(DEBUG):
                    print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text