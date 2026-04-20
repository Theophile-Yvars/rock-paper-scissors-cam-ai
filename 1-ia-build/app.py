import streamlit as st
import numpy as np
import cv2
import mediapipe as mp
import pandas as pd
import os
import csv
import av
import tensorflow as tf
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURATION ---
MODEL_DIR = "../models"
MODEL_PATH = os.path.join(MODEL_DIR, "gesture_model.h5")
DATA_DIR = "../data"
LANDMARKER_PATH = '../models/hand_landmarker.task'
CONNECTIONS = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15), (15, 16), (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)]

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

@st.cache_resource
def get_detector():
    options = vision.HandLandmarkerOptions(base_options=python.BaseOptions(model_asset_path=LANDMARKER_PATH), num_hands=1)
    return vision.HandLandmarker.create_from_options(options)

st.set_page_config(layout="wide")
st.title("Rock-Paper-Scissors Cam AI ✋")
tab1, tab2, tab3 = st.tabs(["📸 Data Capture", "⚙️ Training", "🎥 Test Model"])

# --- TAB 1 : CAPTURE (50/50) ---
with tab1:
    gesture = st.selectbox("Geste à enregistrer :", ["pierre", "feuille", "ciseau"])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Capture")
        image_input = st.camera_input("Prendre une photo")
    with col2:
        st.subheader("Détection")
        if image_input:
            detector = get_detector()
            frame = cv2.imdecode(np.frombuffer(image_input.read(), np.uint8), 1)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            res = detector.detect(mp_img)
            if res.hand_landmarks:
                annotated = frame.copy()
                h, w = frame.shape[:2]
                pts = [(int(lm.x * w), int(lm.y * h)) for lm in res.hand_landmarks[0]]
                for s, e in CONNECTIONS: cv2.line(annotated, pts[s], pts[e], (0, 0, 255), 2)
                for x, y in pts: cv2.circle(annotated, (x, y), 5, (0, 255, 0), -1)
                st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), use_container_width=True)
                if st.button("💾 Enregistrer"):
                    data = np.array([[lm.x, lm.y, lm.z] for lm in res.hand_landmarks[0]]).flatten()
                    pd.DataFrame([data]).to_csv(os.path.join(DATA_DIR, f"{gesture}_data.csv"), mode='a', index=False, header=False)
                    st.success("Enregistré !")

# --- TAB 2 : TRAINING + MATRICE ---
with tab2:
    if st.button("Lancer l'entraînement"):
        # Le spinner affiche la roue qui tourne et le texte pendant l'exécution
        with st.spinner("Entraînement en cours... Veuillez patienter..."):
            x, y = [], []
            for l in ['pierre', 'feuille', 'ciseau']:
                path = os.path.join(DATA_DIR, f"{l}_data.csv")
                if os.path.exists(path):
                    for row in csv.reader(open(path)): x.append([float(d) for d in row]); y.append(l)
            
            if x:
                le = LabelEncoder()
                y_enc = le.fit_transform(y)
                x_train, x_test, y_train, y_test = train_test_split(np.array(x), y_enc, test_size=0.2)
                
                model = tf.keras.Sequential([
                    tf.keras.layers.Dense(1024, activation='relu', input_shape=[63]), 
                    tf.keras.layers.Dense(3, activation='softmax')
                ])
                model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
                model.fit(x_train, y_train, epochs=50, verbose=0)
                model.save(MODEL_PATH)
                
                st.success("Entraînement terminé avec succès !")
                
                # --- MATRICE DE CONFUSION PROPRE ---
                st.subheader("Matrice de confusion")
                y_pred = np.argmax(model.predict(x_test), axis=1)
                
                fig, ax = plt.subplots(figsize=(5, 4))
                sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', 
                            xticklabels=le.classes_, yticklabels=le.classes_, ax=ax, annot_kws={"size": 10})
                
                ax.set_xlabel('Prédit')
                ax.set_ylabel('Réel')
                plt.tight_layout()
                
                st.pyplot(fig, use_container_width=False)
            else:
                st.error("Pas assez de données pour l'entraînement.")
                
# --- TAB 3 : TEST ---
class TestProcessor(VideoProcessorBase):
    def __init__(self): self.detector = get_detector(); self.model = tf.keras.models.load_model(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        if self.detector and self.model:
            res = self.detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
            if res.hand_landmarks:
                data = np.array([[lm.x, lm.y, lm.z] for lm in res.hand_landmarks[0]]).flatten().reshape(1, -1)
                label = ["ciseau", "feuille", "pierre"][np.argmax(self.model.predict(data, verbose=0)[0])]
                cv2.putText(img, label, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

with tab3:
    webrtc_streamer(key="test", video_processor_factory=TestProcessor, rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}))