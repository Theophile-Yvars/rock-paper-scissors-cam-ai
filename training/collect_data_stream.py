import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode, RTCConfiguration
import av
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os

# Configuration WebRTC
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Affichage info
st.warning("💡 Montre ta main devant la webcam, les landmarks vont s'afficher.")
st.markdown("### Choisis un geste à enregistrer 👇")

# Gestion des boutons
gesture_clicked = None
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✊ Pierre"):
        gesture_clicked = "pierre"
with col2:
    if st.button("✋ Feuille"):
        gesture_clicked = "feuille"
with col3:
    if st.button("✌️ Ciseau"):
        gesture_clicked = "ciseau"

# Fonction d'extraction des landmarks
def extract_hand_landmarks(results):
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
    else:
        return np.zeros(21 * 3)

# Classe de traitement vidéo
class HandLandmarkProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
        self.save_gesture = None
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

        if self.save_gesture and self.last_landmarks:
            data = extract_hand_landmarks(self.last_landmarks)
            df = pd.DataFrame([data])
            filename = f"data/{self.save_gesture}_data.csv"
            if os.path.exists(filename):
                df_existing = pd.read_csv(filename, header=None)
                df = pd.concat([df_existing, df], ignore_index=True)
            df.to_csv(filename, index=False, header=False)
            st.success(f"Geste '{self.save_gesture}' sauvegardé ✅")
            self.save_gesture = None

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Lancement de la capture vidéo
ctx = webrtc_streamer(
    key="hand-landmarks",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=HandLandmarkProcessor,
    async_processing=True,
)

# Déclenchement de la sauvegarde via les boutons
if ctx.video_processor:
    if gesture_clicked:
        ctx.video_processor.save_gesture = gesture_clicked
