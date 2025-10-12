# 🎮 Rock Paper Scissors IA

Un jeu de Pierre-Feuille-Ciseau intelligent utilisant la vision par ordinateur pour détecter les gestes de la main en temps réel.

![Screenshot du jeu](assets/20250621_2025_Pierre%20Feuille%20Ciseau%20IA_simple_compose_01jy9vq9yzfgxt5qbadzbvtmff.png)

## 🎯 Fonctionnalités

- **Détection de gestes en temps réel** : Utilise MediaPipe pour reconnaître les gestes Pierre, Feuille, Ciseau
- **Intelligence artificielle** : IA adversaire avec sélection aléatoire des coups
- **Interface moderne** : Frontend React TypeScript avec capture webcam
- **API REST** : Backend FastAPI pour les prédictions de gestes
- **Collecte de données** : Interface Streamlit pour entraîner le modèle
- **Machine Learning** : Réseau de neurones TensorFlow pour la classification

## 🏗️ Architecture

Le projet est structuré en plusieurs composants :

```
rock-paper-scissors-cam-ai/
├── app/
│   ├── backend/          # API FastAPI
│   │   ├── main.py       # Serveur API
│   │   └── classifier.py # Classification des gestes
│   └── frontend/         # Interface React
│       └── src/
├── training/             # Entraînement du modèle
│   ├── collect_data.py   # Collecte de données
│   └── train_model.py    # Entraînement
├── models/               # Modèles entraînés
├── data/                 # Données d'entraînement
└── assets/              # Ressources multimédia
```

## 🚀 Installation

### Prérequis

- Python 3.8+
- Node.js 16+
- npm ou yarn
- Webcam fonctionnelle

### Installation des dépendances

#### Backend Python
```powershell
# Installer les dépendances Python
pip install -r requirements.txt
```

#### Frontend React
```powershell
# Naviguer vers le frontend
cd app/frontend

# Installer les dépendances Node.js
npm install
```

## 🎮 Utilisation

### 1. Collecte de données (optionnel)

Pour améliorer le modèle avec vos propres données :

```powershell
# Lancer l'interface de collecte
cd training
streamlit run collect_data.py
```

- Sélectionnez le geste à enregistrer (pierre, feuille, ciseau)
- Montrez votre geste devant la webcam
- Cliquez sur "Enregistrer" pour sauvegarder

### 2. Entraînement du modèle (optionnel)

```powershell
# Entraîner le modèle avec les nouvelles données
cd training
python train_model.py
```

### 3. Lancement de l'application

#### Démarrer le backend
```powershell
# Terminal 1 : API Backend
cd app/backend
uvicorn main:app --reload
```
L'API sera disponible sur `http://localhost:8000`

#### Démarrer le frontend
```powershell
# Terminal 2 : Interface utilisateur
cd app/frontend
npm start
```
L'application sera disponible sur `http://localhost:3000`

## 🎲 Comment jouer

1. **Autoriser l'accès webcam** : Le navigateur vous demandera l'autorisation
2. **Placer votre main** : Montrez votre geste devant la caméra
3. **Cliquer sur GO** : L'IA choisira son geste aléatoirement
4. **Voir le résultat** : Le gagnant sera affiché selon les règles classiques :
   - 🪨 Pierre bat ✂️ Ciseau
   - 📄 Feuille bat 🪨 Pierre  
   - ✂️ Ciseau bat 📄 Feuille

## 🤖 Fonctionnement technique

### Pipeline de détection
1. **Capture vidéo** : La webcam capture les images en temps réel
2. **Extraction de landmarks** : MediaPipe détecte 21 points clés de la main
3. **Vectorisation** : Les coordonnées (x,y,z) sont converties en vecteur de 63 dimensions
4. **Prédiction** : Le réseau de neurones classifie le geste
5. **Affichage** : Le résultat est affiché dans l'interface

### Modèle de Machine Learning
- **Architecture** : Réseau dense (1024→1024→1024→3 neurones)
- **Entrée** : 63 features (21 landmarks × 3 coordonnées)
- **Sortie** : Probabilités pour 3 classes (pierre, feuille, ciseau)
- **Framework** : TensorFlow/Keras
- **Régularisation** : Dropout (30%) et BatchNormalization

## 📊 Données d'entraînement

Le modèle est entraîné sur :
- **Format** : Fichiers CSV avec coordonnées des landmarks
- **Classes** : pierre, feuille, ciseau
- **Division** : 80% entraînement / 20% validation
- **Augmentation** : Collecte interactive via Streamlit

## 🛠️ Technologies utilisées

| Composant | Technologie |
|-----------|-------------|
| **Vision** | MediaPipe |
| **IA** | TensorFlow, Keras |
| **Backend** | FastAPI, uvicorn |
| **Frontend** | React 19, TypeScript |
| **Collecte** | Streamlit |
| **Processing** | OpenCV, NumPy |
| **Data Science** | scikit-learn, pandas |

## 🔧 Développement

### Structure des API

**Backend (port 8000)**
- `POST /predict` : Upload d'image pour prédiction de geste
  - Input : multipart/form-data avec fichier image
  - Output : `{"gesture": "pierre|feuille|ciseau"}`

### Scripts utiles

```powershell
# Tests du modèle
cd models
python test_model.py

# Build frontend pour production
cd app/frontend
npm run build

# Lancer les tests frontend
npm test
```

## 📝 Améliorations possibles

- [ ] Multijoueur en ligne
- [ ] Historique des parties
- [ ] Statistiques de performance
- [ ] Amélioration de la précision du modèle
- [ ] Support multi-langues
- [ ] Mode tournoi
- [ ] Gestes personnalisés

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Contact

Si vous avez des questions ou suggestions, n'hésitez pas à ouvrir une issue ou me contacter.

---

⭐ **N'oubliez pas de mettre une étoile si ce projet vous a plu !** ⭐
