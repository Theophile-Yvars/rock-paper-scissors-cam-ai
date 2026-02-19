import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode, RTCConfiguration
import av
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import os

# Config WebRTC
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Mediapipe + modèle
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
CLASS_NAMES = ["ciseau", "feuille", "pierre"]
MODEL_PATH = "gesture_model.h5"

# Chargement du modèle
model = tf.keras.models.load_model(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

# Extraction des landmarks
def extract_hand_landmarks(results):
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
    return np.zeros(21 * 3)

# Traitement vidéo
class HandProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
        self.prediction = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for lm in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, lm, mp_hands.HAND_CONNECTIONS)

            if model:
                data = extract_hand_landmarks(results).reshape(1, -1)
                pred = model.predict(data, verbose=0)[0]
                class_id = np.argmax(pred)
                conf = pred[class_id]
                self.prediction = (CLASS_NAMES[class_id], conf)
                label = f"{CLASS_NAMES[class_id]} ({conf*100:.1f}%)"
                cv2.putText(img, label, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Interface
st.title("Détection de geste en temps réel")

ctx = webrtc_streamer(
    key="gesture",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=HandProcessor,
    async_processing=True,
)

if ctx.video_processor and ctx.video_processor.prediction:
    pred, conf = ctx.video_processor.prediction
    st.markdown(f"### Geste détecté : **{pred.upper()}**")
    st.progress(min(conf, 1.0))
