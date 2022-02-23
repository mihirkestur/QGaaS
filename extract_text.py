import pytesseract
import cv2
from difflib import SequenceMatcher
import re 

LOG = 0
"""
Input : Path to video
Output: List of texts

Begin

    video = cv2.VideoCapture(path)
    texts = []
    frame = video.read()
    sliding_window = 1
    similarity_threshold = 0.4
    previous_text = pytesseract.image_to_string(frame)

    while frames in video exist:
        frame = video.read()
        current_text = pytesseract.image_to_string(frame)
        if similar(previous_text, current_text) <= similarity_threshold:
            texts.append(previous_text)
        previous_text = current_text

    if similar(previous_text, current_text) <= similarity_threshold:
            texts.append(previous_text)
    
    return texts
    
End

function similar(string_1, string_2):
    return ratio of similarity
"""
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_text_from_vid(path):
    print("Extracting text from video....")
    
    video = cv2.VideoCapture(path)

    content = []
    frame_num = 0
    sliding_window = 50
    similarity_threshold = 0.4

    ret, frame = video.read()
    #frame = frame[int(0.10*frame.shape[0]):int(0.9*frame.shape[0])]
    remove_newline = " ".join(pytesseract.image_to_string(frame).split("\n"))
    remove_esc = "".join(remove_newline.split("\x0c"))
    prev_content = remove_esc

    while(True):
        ret, frame = video.read()
        if(frame is not None):
            pass
            #frame = frame[int(0.10*frame.shape[0]):int(0.9*frame.shape[0])]
        frame_num += 1
        if(frame_num%sliding_window!=0):
            pass
        elif(ret):
            remove_newline = " ".join(pytesseract.image_to_string(frame).split("\n"))
            remove_esc = "".join(remove_newline.split("\x0c"))
            curr_content = remove_esc
            similarity = similar(prev_content, curr_content)
            if(LOG):
                with open("logs.csv", "a") as f:
                    f.write(f"{frame_num},{similarity}\n")
            if(similarity<=similarity_threshold):
                prev_content = re.sub('[^A-Za-z0-9]+', ' ', prev_content)
                content.append(prev_content)
            prev_content = curr_content
        else:
            break

    similarity = similar(prev_content, curr_content)
    if(LOG):
        with open("logs.csv", "a") as f:
            f.write(f"{frame_num},{similarity}\n")
    if(similarity<=similarity_threshold):
        prev_content = re.sub('[^A-Za-z0-9]+', ' ', prev_content)
        content.append(prev_content)
    
    video.release()
    cv2.destroyAllWindows()
    if(LOG):
        f.close()
    #print(content)
    return content

"""texts = get_text_from_vid("dataset/13.mp4")

for i in range(len(texts)):
    print("Slide ", i+1, ": ", texts[i])"""