#import library
import speech_recognition as sr
import moviepy.editor as mp

clip = mp.VideoFileClip(r"part2.mp4") 
 
clip.audio.write_audiofile(r"part2.wav")

r = sr.Recognizer()
audio = sr.AudioFile("part2.wav")
with audio as source:
    audio_file = r.record(source)
result = r.recognize_google(audio_file)
print(result)