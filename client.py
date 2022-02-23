print("\nLoading dependencies....")
import media_to_text
import extract_text
import model
print("Finished loading dependencies!\n")

Q_NO = 1

# FROM AUDIO
PATH_TO_MEDIA = "dataset/1.mp4"

# FROM TEXT IN VIDEO
print("Obtaining questions for TEXT IN VIDEO: ", PATH_TO_MEDIA)
text_from_vid = extract_text.get_text_from_vid(PATH_TO_MEDIA)
for i in text_from_vid:
    print("CONTEXT: ", i)
    print(f"QUESTION {Q_NO} :", model.get_questions(i))
    Q_NO += 1
    print()

print("------------------------------------------------------------------------------")

print("Obtaining questions for AUDIO: ", PATH_TO_MEDIA)
transcript = media_to_text.obtain_transcript(PATH_TO_MEDIA)
for i in transcript:
    print("CONTEXT: ", i)
    print(f"QUESTION {Q_NO} :", model.get_questions(i))
    Q_NO += 1
    print()

print("------------------------------------------------------------------------------")

# FROM TEXT SOURCE
PATH_TO_TEXT_FILE = "data.txt"
file = open(PATH_TO_TEXT_FILE, "r")
print("Obtaining questions for text in file: ", PATH_TO_TEXT_FILE)
data = " ".join(file.read().split("\n")).split(".")
for i in data[:-1]:
    print("CONTEXT: ", i)
    print(f"QUESTION {Q_NO} :", model.get_questions(i))
    Q_NO += 1
    print()
file.close()
