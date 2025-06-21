import streamlit as st
import numpy as np
import cv2
import mediapipe as mp
import pandas as pd
import os

st.set_page_config(page_title="Collecte de données", layout="centered")
st.title("📊 Collecte de données - Pierre Feuille Ciseau")

# Détecteur de main
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Geste sélectionné
gesture = st.selectbox("Quel geste veux-tu enregistrer ?", ["pierre", "feuille", "ciseau"])

# Capture vidéo en direct
image = st.camera_input("Montre le geste devant la caméra 📸")

def extract_hand_landmarks(results):
    """
    Extrait les coordonnées x, y, z des 21 landmarks de la main.
    Retourne un tableau aplati de 63 valeurs (21 * 3).
    """
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
    else:
        return np.zeros(21 * 3)

if image is not None:
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        st.success("Main détectée ✅")
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        st.image(frame_rgb, channels="RGB")

        if st.button("💾 Enregistrer ce geste"):
            data = extract_hand_landmarks(results)
            df = pd.DataFrame([data])
            filename = f"data/{gesture}_data.csv"

            # Append au fichier existant ou créer
            if os.path.exists(filename):
                df_existing = pd.read_csv(filename, header=None)
                df_combined = pd.concat([df_existing, df], ignore_index=True)
                df_combined.to_csv(filename, index=False, header=False)
            else:
                df.to_csv(filename, index=False, header=False)

            st.success(f"Geste '{gesture}' enregistré dans {filename}")
    else:
        st.warning("Aucune main détectée ❌")
