# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Rock Paper Scissors AI project that uses computer vision to detect hand gestures and play against an AI opponent. It consists of multiple components: a machine learning pipeline for training gesture recognition models, a data collection system, a FastAPI backend for predictions, and a React TypeScript frontend for the game interface.

## Common Development Commands

### Data Collection & Training
```powershell
# Collect training data using Streamlit interface
cd training
streamlit run collect_data.py

# Alternative data collection command
training\run_collect_data.bat

# Train the gesture recognition model
cd training
python train_model.py
```

### Backend Development
```powershell
# Run FastAPI backend server
cd app\backend
uvicorn main:app --reload

# Backend runs on http://localhost:8000 by default
# API endpoint: POST /predict for gesture prediction
```

### Frontend Development
```powershell
# Install frontend dependencies
cd app\frontend
npm install

# Run React development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Full Application
```powershell
# Note: run.bat in root references main.py which doesn't exist
# The project appears to have separate frontend/backend that need to be run independently
```

## Architecture Overview

### Core Components

**Machine Learning Pipeline:**
- `training/collect_data.py`: Streamlit app for collecting hand gesture training data using MediaPipe
- `training/train_model.py`: Neural network training script that processes collected data and saves to `models/gesture_model.h5`
- Data stored in CSV format in `data/` directory (pierre_data.csv, feuille_data.csv, ciseau_data.csv)

**Backend API (`app/backend/`):**
- `main.py`: FastAPI server with CORS middleware and single `/predict` endpoint
- `classifier.py`: Gesture classification using MediaPipe for hand landmark extraction and TensorFlow for prediction
- Model expects 63-dimensional feature vectors (21 hand landmarks × 3 coordinates each)

**Frontend Game (`app/frontend/`):**
- React TypeScript application with webcam integration
- `WebcamCapture.tsx`: Captures video stream and prepares frames for gesture recognition
- `AIAvatar.tsx`: AI opponent component
- `App.tsx`: Main game interface coordinating player vs AI gameplay

### Data Flow
1. MediaPipe extracts 21 hand landmarks (63 features: x,y,z coordinates)
2. Training data collected via Streamlit interface, stored as CSV files
3. Neural network (1024→1024→1024→3 dense layers) trained on landmark features
4. Backend API loads trained model, processes webcam frames via MediaPipe
5. Frontend captures video, sends frames to backend, receives gesture predictions
6. Game logic determines winner between player gesture and random AI choice

### Key Technologies
- **Computer Vision**: MediaPipe for hand landmark detection
- **ML Framework**: TensorFlow/Keras for gesture classification  
- **Backend**: FastAPI with CORS support
- **Frontend**: React 19 with TypeScript, Create React App
- **Data Collection**: Streamlit for interactive training data gathering

## Development Notes

### Model Training
- The neural network expects exactly 63 input features (MediaPipe hand landmarks)
- Three gesture classes: "pierre" (rock), "feuille" (paper), "ciseau" (scissors)
- Training uses 80/20 split with stratification
- Model saved as H5 format in `models/gesture_model.h5`

### API Integration
- Backend expects image uploads via multipart/form-data
- Frontend webcam capture currently commented out (line 26 in WebcamCapture.tsx)
- CORS configured to allow all origins for development

### File Structure
- `data/`: CSV files containing training data
- `models/`: Trained model files (.h5 format)
- `training/`: Data collection and model training scripts
- `app/backend/`: FastAPI server and classification logic  
- `app/frontend/`: React TypeScript game interface
- `assets/`: Game assets and media files

### Dependencies
Key Python packages: mediapipe, tensorflow, fastapi, streamlit, opencv-python, numpy, scikit-learn
Frontend: React 19, TypeScript, testing libraries via Create React App