import pytesseract
import cv2
from difflib import SequenceMatcher
import re 

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_text_from_vid(path):
    print("Extracting text from video....")
    
    video = cv2.VideoCapture(path)

    content = []
    frame_num = 0

    ret, frame = video.read()
    remove_newline = " ".join(pytesseract.image_to_string(frame).split("\n"))
    remove_esc = "".join(remove_newline.split("\x0c"))
    prev_content = remove_esc

    while(True):
        ret, frame = video.read()
        frame_num += 1
        if(frame_num%100!=0):
            pass
        elif (ret):
            remove_newline = " ".join(pytesseract.image_to_string(frame).split("\n"))
            remove_esc = "".join(remove_newline.split("\x0c"))
            curr_content = remove_esc
            if(similar(prev_content, curr_content)<=0.5):
                prev_content = re.sub('[^A-Za-z0-9]+', ' ', prev_content)
                content.append(prev_content)
            prev_content = curr_content
        else:
            break
    video.release()
    cv2.destroyAllWindows()

    return content