import React, { useState } from 'react';
import './App.css';
import WebcamCapture from "./webcam/WebcamCapture";
import AIAvatar from "./aiavatar/AIAvatar";

type Choice = 'pierre' | 'feuille' | 'ciseau' | null;

function App() {
  const [aiChoice, setAiChoice] = useState<Choice>(null);

  const handleAIPlay = () => {
    const choices: Choice[] = ['pierre', 'feuille', 'ciseau'];
    const randomChoice = choices[Math.floor(Math.random() * choices.length)];
    setAiChoice(randomChoice);
  };

  return (
    <div className="App">
        <div className="App-title">
            <h1>ROCK PAPER SCISSORS BATTLE</h1>
        </div>
        <div className="App-content">
            <div className="App-ai">
                <AIAvatar choice={aiChoice} />
                <button onClick={handleAIPlay}>Lancer l'IA</button>
            </div>
            <div className="App-player">
                <WebcamCapture />
            </div>
        </div>
    </div>
  );
}

export default App;
