#import media_to_text
import extract_text
import model

# FROM AUDIO
PATH_TO_MEDIA = "dataset/2.mp4"
"""
print("Obtaining questions for: ", PATH_TO_MEDIA)
transcript = media_to_text.obtain_transcript(PATH_TO_MEDIA)
for i in transcript:
    print("CONTEXT: ", i)
    print("QUESTION:", model.get_questions(i))
    print()

"""
# FROM TEXT IN VIDEO
print("Obtaining questions for text in video: ", PATH_TO_MEDIA)
text_from_vid = extract_text.get_text_from_vid(PATH_TO_MEDIA)
for i in text_from_vid:
    print("CONTEXT: ", i)
    print("QUESTION:", model.get_questions(i))
    print()


"""# FROM TEXT SOURCE
PATH_TO_TEXT_FILE = "data.txt"
file = open(PATH_TO_TEXT_FILE, "r")
print("Obtaining questions for text in: ", PATH_TO_TEXT_FILE)
data = " ".join(file.read().split("\n")).split(".")
for i in data[:-1]:
    print("CONTEXT: ", i)
    print("QUESTION:", model.get_questions(i))
    print()
file.close()"""
