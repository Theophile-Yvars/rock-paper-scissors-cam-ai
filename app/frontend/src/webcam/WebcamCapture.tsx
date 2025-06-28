// src/WebcamCapture.tsx
import React, { useRef, useEffect } from 'react';
import axios from 'axios';

const WebcamCapture = () => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
      if (videoRef.current) videoRef.current.srcObject = stream;
    });

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
          formData.append("file", blob, "frame.jpg");
          //const res = await axios.post("http://localhost:8000/predict", formData);
          //console.log(res.data);
        }, 'image/jpeg');
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <video ref={videoRef} autoPlay playsInline />;
};

export default WebcamCapture;
