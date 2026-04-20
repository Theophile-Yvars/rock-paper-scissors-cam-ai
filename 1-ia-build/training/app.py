import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
import csv
import cv2
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- CONFIGURATION ---
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "gesture_model.h5")
DATA_DIR = "data"
os.makedirs(MODEL_DIR, exist_ok=True)

if 'page' not in st.session_state:
    st.session_state.page = 'train'
if 'cm' not in st.session_state:
    st.session_state.cm = None
if 'labels' not in st.session_state:
    st.session_state.labels = None

# --- LOGIQUE D'ENTRAÎNEMENT ---
def run_training():
    x, y = [], []
    for label in ['pierre', 'feuille', 'ciseau']:
        path = os.path.join(DATA_DIR, f"{label}_data.csv")
        if os.path.exists(path):
            with open(path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in reader:
                    data = [float(d) for d in ','.join(row).split(',')]
                    x.append(data)
                    y.append(label)
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    x_train, x_test, y_train, y_test = train_test_split(np.array(x), y_encoded, test_size=0.2, random_state=42)
    
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(1024, activation='relu', input_shape=[63]),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=50, verbose=0)
    
    model.save(MODEL_PATH)
    y_pred = np.argmax(model.predict(x_test), axis=1)
    
    st.session_state.cm = confusion_matrix(y_test, y_pred)
    st.session_state.labels = le.classes_
    st.session_state.page = 'results'

# --- LOGIQUE DE TEST ---
class HandProcessor(VideoProcessorBase):
    def __init__(self):
        # Initialisation avec l'API Tasks (plus stable)
        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path='models/hand_landmarker.task'),
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.model = tf.keras.models.load_model(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
        self.class_names = ["ciseau", "feuille", "pierre"]
        self.connections = [
            (0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15),
            (15, 16), (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)
        ]

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        results = self.detector.detect(mp_image)

        if results.hand_landmarks and self.model:
            for hand_landmarks in results.hand_landmarks:
                # 1. Convertir tous les points en coordonnées pixels
                points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
                
                # 2. Dessiner les lignes (les connexions)
                for start_idx, end_idx in self.connections:
                    cv2.line(img, points[start_idx], points[end_idx], (255, 0, 0), 2) # Bleu en BGR
                
                # 3. Dessiner les points (les cercles)
                for x, y in points:
                    cv2.circle(img, (x, y), 5, (0, 255, 0), -1) # Vert
                
                # 4. Prédiction
                data = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks]).flatten().reshape(1, -1)
                pred = self.model.predict(data, verbose=0)[0]
                label = f"{self.class_names[np.argmax(pred)]}"
                cv2.putText(img, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- PAGES ---
if st.session_state.page == 'train':
    st.title("Entraînement")
    if st.button("Lancer l'entraînement"):
        with st.spinner("Apprentissage en cours..."):
            run_training()
            st.rerun()

elif st.session_state.page == 'results':
    st.title("Matrice de Confusion")
    fig, ax = plt.subplots()
    sns.heatmap(st.session_state.cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=st.session_state.labels, yticklabels=st.session_state.labels)
    st.pyplot(fig)
    if st.button("Tester le modèle"):
        st.session_state.page = 'test'
        st.rerun()

elif st.session_state.page == 'test':
    st.title("Test en temps réel")
    webrtc_streamer(key="test", video_processor_factory=HandProcessor, 
                    rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}))
    if st.button("Retour aux résultats"):
        st.session_state.page = 'results'
        st.rerun()