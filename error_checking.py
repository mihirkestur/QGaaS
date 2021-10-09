DEBUG = 0
"""
Aim: To study the accuracy of the SpeechRecognition (Google API) python module
"""
import media_to_text
import os, glob
path_to_dataset = "dataset/nptel/wav"
path_to_ground_truth = "dataset/nptel/corrected_txt"
for audio_path in glob.glob(os.path.join(path_to_dataset, '*.wav')):
    print(media_to_text.obtain_transcript(audio_path))
    for ground_truth in glob.glob(os.path.join(path_to_ground_truth, '*.txt')):
        if(audio_path.split("/")[-1].split(".")[0] == ground_truth.split("/")[-1].split(".")[0]):
            with open(ground_truth) as f:
                gt_text = " ".join([l.rstrip() for l in f])
                if(DEBUG):print("Ground truth text ")
            f.close()