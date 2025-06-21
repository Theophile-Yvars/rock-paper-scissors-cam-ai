import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.set_page_config(page_title="Pierre Feuille Ciseaux AI", layout="centered")

st.title("✋ Pierre - Feuille - Ciseaux 🤖")
st.write("Montre un geste à la caméra, et l'IA devinera !")

# --- Détecteur de main MediaPipe ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# --- Capture image depuis webcam ---
image = st.camera_input("Fais ton geste devant la caméra 📸")

if image is not None:
    # Lire l'image comme tableau NumPy
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Détection des mains
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        st.success("Main détectée ✅")

        # Dessiner les points
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        st.image(frame_rgb, channels="RGB", caption="Geste détecté")

        # (Optionnel) Afficher les coordonnées d’un point clé
        landmark_0 = results.multi_hand_landmarks[0].landmark[0]
        st.write(f"Coordonnées du poignet : x={landmark_0.x:.2f}, y={landmark_0.y:.2f}")
    else:
        st.warning("Aucune main détectée ❌")
