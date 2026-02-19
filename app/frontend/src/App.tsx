import React, { useState, useEffect } from 'react';
import './App.css';
import WebcamCapture from "./webcam/WebcamCapture";
import AIAvatar from "./aiavatar/AIAvatar";

type Choice = 'pierre' | 'feuille' | 'ciseau' | null;

function App() {
  const [aiChoice, setAiChoice] = useState<Choice>(null);
  const [playerChoice, setPlayerChoice] = useState<Choice>(null);
  const [countdown, setCountdown] = useState<number | null>(null);
  const [winner, setWinner] = useState<string | null>(null);

  const emojiMap: Record<'pierre' | 'feuille' | 'ciseau', string> = {
    pierre: '🪨',
    feuille: '📄',
    ciseau: '✂️',
  };

  // Fonction pour générer un choix aléatoire de l'IA
  const generateAIChoice = (): Choice => {
    const choices: Choice[] = ['pierre', 'feuille', 'ciseau'];
    return choices[Math.floor(Math.random() * choices.length)];
  };

  // Déterminer le gagnant
  const determineWinner = (player: Choice, ai: Choice) => {
    if (!player || !ai) return null;
    if (player === ai) return "Égalité";
    if (
      (player === 'pierre' && ai === 'ciseau') ||
      (player === 'feuille' && ai === 'pierre') ||
      (player === 'ciseau' && ai === 'feuille')
    ) return "Vous avez gagné";
    return "Vous avez perdu";
  };

  // Lancer le compte à rebours
  const handleAIPlay = () => {
    if (!playerChoice) {
      alert("Montrez votre geste à la webcam avant de jouer !");
      return;
    }

    setCountdown(3);
    setWinner(null);
    setAiChoice(null);

    const countdownInterval = setInterval(() => {
      setCountdown(prev => {
        if (prev && prev > 1) return prev - 1;
        clearInterval(countdownInterval);
        const ai = generateAIChoice();
        setAiChoice(ai);
        setWinner(determineWinner(playerChoice, ai));
        return null;
      });
    }, 1000);
  };

  return (
    <div className="App">
      <div className="App-title">
        <h1>Rock Paper Scissors Battle</h1>
        <button className="App-title-button" onClick={handleAIPlay} style={{ marginTop: 12 }}>
          GO
        </button>
      </div>

      <div className="App-content">
        <div className="App-ai">
          <div className="ai-container">
            <AIAvatar />
          </div>
          <div className="emoji-overlay">
            {countdown ? countdown : aiChoice ? emojiMap[aiChoice] : '❓'}
          </div>
        </div>

        <div className="App-versus">
          <h2>VS</h2>
          <div style={{ marginTop: 20, fontSize: '1.5rem', color: '#F6EBDB' }}>
            {winner}
          </div>
        </div>

        
        <div className="App-player">
          <div className="video-container">
            <WebcamCapture onGestureDetected={setPlayerChoice} />
          </div>
          <div className="emoji-overlay">
            {playerChoice ? emojiMap[playerChoice] : '❓'}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
