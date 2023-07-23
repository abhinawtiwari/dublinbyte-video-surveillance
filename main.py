import streamlit as st
import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np
import time 
import base64

st.title('DublinByte Video Surveillance')
placeholder = st.empty()
placeholder_audio = st.empty()


ZONE_POLYGON = np.array([
    [0, 0],
    [0.5, 0],
    [0.5, 1],
    [0, 1]
])

################################################################
# Code for voice configurations
import os

from google.cloud import texttospeech 
from google.cloud import texttospeech_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "key.json"
client = texttospeech_v1.TextToSpeechClient()
voice = texttospeech_v1.VoiceSelectionParams(
    language_code="hi-IN", ssml_gender=texttospeech.SsmlVoiceGender.MALE
)
audio_config = texttospeech_v1.AudioConfig(
    audio_encoding=texttospeech_v1.AudioEncoding.MP3
)
################################################################

# def parse_arguments() -> argparse.Namespace:
def parse_arguments():
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone, 
        color=sv.Color.green(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )

    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        # 41 for cup
        detections = detections[detections.class_id == 41]
        # labels = [
        #     f"{model.model.names[class_id]} {confidence:0.2f}"
        #     for _, confidence, class_id, _
        #     in detections
        # ]
        labels = []
        for _, confidence, class_id, _ in detections:
            labels.append(model.model.names[class_id])

        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )

        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)      
        
        # cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            break
        
        count_o = len(detections)
        print("count of cups: ", count_o)
        placeholder.text(f"No. of cups: {count_o}")
        quote = f"{count_o} cups"
        response = client.synthesize_speech(
            input=texttospeech_v1.SynthesisInput(text=quote), voice=voice, audio_config=audio_config
        )

        # placeholder_audio.audio(response.audio_content, format="mp3")
        # play the audio
        # Convert the audio content to base64.
        audio_content = base64.b64encode(response.audio_content).decode()

        # Play the audio on its own.
        placeholder_audio.markdown(
            f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{audio_content}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(5)
        placeholder.empty()
        placeholder_audio.empty()


if __name__ == "__main__":
    main()