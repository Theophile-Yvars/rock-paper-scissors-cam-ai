import streamlit as st
import numpy as np
import cv2
import mediapipe as mp
import pandas as pd
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- CONFIGURATION ---
MODEL_PATH = 'models/hand_landmarker.task'
DATA_DIR = "data"

@st.cache_resource
def get_detector():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Fichier modèle introuvable à {MODEL_PATH}")
        return None
    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
        num_hands=1
    )
    return vision.HandLandmarker.create_from_options(options)

detector = get_detector()

st.title("Collecte de données - IA Gestes")
gesture = st.selectbox("Geste ?", ["pierre", "feuille", "ciseau"])
image_input = st.camera_input("Prendre une photo 📸")

# Liste des connexions standard pour la main (les 21 points MediaPipe)
CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9),
    (9, 10), (10, 11), (11, 12), (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)
]

if image_input and detector:
    file_bytes = np.asarray(bytearray(image_input.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        st.success("Main détectée ✅")
        annotated_image = frame.copy()
        h, w, _ = annotated_image.shape
        
        for hand_landmarks in result.hand_landmarks:
            # Convertir les landmarks en pixels
            points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
            
            # 1. Dessiner les traits (Lignes rouges)
            for start, end in CONNECTIONS:
                cv2.line(annotated_image, points[start], points[end], (0, 0, 255), 2)
            
            # 2. Dessiner les points (Cercles verts)
            for x, y in points:
                cv2.circle(annotated_image, (x, y), 5, (0, 255, 0), -1)
        
        st.image(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB), use_container_width=True)

        if st.button("💾 Enregistrer"):
            os.makedirs(DATA_DIR, exist_ok=True)
            data = np.array([[lm.x, lm.y, lm.z] for lm in result.hand_landmarks[0]]).flatten()
            df = pd.DataFrame([data])
            path = os.path.join(DATA_DIR, f"{gesture}_data.csv")
            df.to_csv(path, mode='a', index=False, header=not os.path.exists(path))
            st.success("Enregistré !")
    else:
        st.warning("Aucune main détectée.")