import React, { useRef, useEffect } from 'react';
import axios from 'axios';
import './WebcamCapture.css';

type Choice = 'pierre' | 'feuille' | 'ciseau';
type WebcamCaptureProps = {
  onGestureDetected: (gesture: Choice) => void;
};

const WebcamCapture: React.FC<WebcamCaptureProps> = ({ onGestureDetected }) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    // Démarrage de la webcam
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      if (videoRef.current) videoRef.current.srcObject = stream;
    });

    // Capture et envoi du flux toutes les secondes
    const interval = setInterval(async () => {
      if (!videoRef.current) return;

      const canvas = document.createElement('canvas');
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext('2d');

      if (ctx) {
        ctx.drawImage(videoRef.current, 0, 0);

        canvas.toBlob(async (blob) => {
          if (!blob) return;

          const formData = new FormData();
          formData.append('file', blob, 'frame.jpg');

          try {
            const res = await axios.post<{ gesture: string }>(
              'http://localhost:8000/predict',
              formData
            );

            let detectedGesture = res.data.gesture as Choice;
            if (detectedGesture === "ciseau") detectedGesture = "pierre";
            else if (detectedGesture === "pierre") detectedGesture = "ciseau";
            console.log("Geste détecté:", detectedGesture);
            onGestureDetected(detectedGesture); // envoie le geste au parent
          } catch (err) {
            console.error('Erreur lors de la détection du geste:', err);
          }
        }, 'image/jpeg');
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [onGestureDetected]);

  return (
    <div className="webcam-container">
      <video ref={videoRef} autoPlay playsInline className="webcam-video" />
    </div>
  );
};

export default WebcamCapture;
