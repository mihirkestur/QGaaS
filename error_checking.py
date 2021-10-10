"""
Aim: To study the accuracy of the SpeechRecognition (Google API) python module
"""
DEBUG = 0
import media_to_text
import os, glob
from jiwer import wer
from difflib import SequenceMatcher

def compareStr(str1,str2):
    return SequenceMatcher(None, str1, str2).ratio()

def compareSetint(str1,str2):
    s1=set(str1.split())
    s2=set(str2.split())
    return len(s1.intersection(s2))/len(s1)

path_to_dataset = "dataset/nptel/wav"
path_to_ground_truth = "dataset/nptel/corrected_txt"
total_error_wer = 0
total_error_cmp = 0
total_samples = 0
# For each sample
for audio_path in glob.glob(os.path.join(path_to_dataset, '*.wav')):
    transcript = (media_to_text.obtain_transcript(audio_path)).upper()
    total_samples += 1
    print("currently running ", total_samples)
    # Finding ground truth
    for ground_truth in glob.glob(os.path.join(path_to_ground_truth, '*.txt')):
        if(audio_path.split("/")[-1].split(".")[0] == ground_truth.split("/")[-1].split(".")[0]):
            # If found compare and output accuracy
            with open(ground_truth) as f:
                gt_text = (" ".join([l.rstrip() for l in f])).upper()
                try:
                    wer_error = wer(gt_text, transcript)
                    total_error_wer += wer_error
                    est1=compareStr(gt_text,transcript)
                    est2=compareSetint(gt_text,transcript)
                    total_error_cmp += 1-est1
                except Exception as e:
                    print(e)
                
                if(DEBUG):
                    print(gt_text,"\n",transcript)
                    print("Estimated errors:\nWords predicted perfectly : {}\nError rate : {}\nWER : {}\n".format(est2,1-est1,wer_error))
            f.close()
    if(total_samples == 10):
        break
print("Total error rate is (wer)",(total_error_wer/total_samples)*100)
print("Total error rate is (cmp)",(total_error_cmp/total_samples)*100)