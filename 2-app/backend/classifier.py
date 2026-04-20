import mediapipe as mp
import numpy as np
import tensorflow as tf
import cv2

class Classifier():
    def __init__(self, pathModel):
        print("Initializing Classifier")
        # Charger le modèle entraîné (.h5)
        self.model = tf.keras.models.load_model(pathModel)
        # Initialiser MediaPipe Hands
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
        # Labels (à adapter à ton entraînement)
        self.labels = ["pierre", "feuille", "ciseau"]


    def extract_hand_landmarks(self, image: np.ndarray):
        """
        Utilise MediaPipe pour extraire les landmarks d'une main sur une image BGR.
        Retourne un tableau (63,) ou None si aucune main détectée.
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            keypoints = []
            for lm in hand_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])
            return np.array(keypoints)  # (63,)
        return None


    def predict_gesture(self, image: np.ndarray) -> str:
        """
        Reçoit une image (BGR), détecte la main avec MediaPipe, extrait les keypoints,
        et prédit le geste avec le modèle.
        """
        keypoints = self.extract_hand_landmarks(image)

        if keypoints is None:
            return "aucune main détectée"

        # Mise en forme pour le modèle : (1, 63)
        input_data = keypoints.reshape(1, -1)

        # Prédiction
        prediction = self.model.predict(input_data)
        predicted_class = np.argmax(prediction)
        return self.labels[predicted_class]
