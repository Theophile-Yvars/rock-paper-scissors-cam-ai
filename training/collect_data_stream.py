import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode, RTCConfiguration
import av
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os
import numpy as np

# Configuration WebRTC
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Variables globales
gesture = st.selectbox("Quel geste veux-tu enregistrer ?", ["pierre", "feuille", "ciseau"])
save_button = st.button("💾 Enregistrer le geste actuel")
st.warning("💡 Montre ta main devant la webcam, les landmarks vont s'afficher.")

# Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def extract_hand_landmarks(results):
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
    else:
        return np.zeros(21 * 3)

class HandLandmarkProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
        self.save_frame = False
        self.last_landmarks = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            self.last_landmarks = results

        # Si on a cliqué sur le bouton dans Streamlit
        if self.save_frame and self.last_landmarks:
            data = extract_hand_landmarks(self.last_landmarks)
            df = pd.DataFrame([data])
            filename = f"data/{gesture}_data.csv"
            if os.path.exists(filename):
                df_existing = pd.read_csv(filename, header=None)
                df = pd.concat([df_existing, df], ignore_index=True)
            df.to_csv(filename, index=False, header=False)
            self.save_frame = False
            st.success(f"Geste '{gesture}' sauvegardé dans {filename} ✅")

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Lance le streamer
ctx = webrtc_streamer(
    key="hand-landmarks",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=HandLandmarkProcessor,
    async_processing=True,
)

# Récupère l'objet vidéo et déclenche la sauvegarde
if ctx.video_processor:
    if save_button:
        ctx.video_processor.save_frame = True
