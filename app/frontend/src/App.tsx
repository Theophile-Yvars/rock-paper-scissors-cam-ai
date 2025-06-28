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

  const emojiMap: Record<'pierre' | 'feuille' | 'ciseau', string> = {
      pierre: '🪨',
      feuille: '📄',
      ciseau: '✂️',
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
                <AIAvatar />
            </div>
            <div className="App-versus">
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ marginTop: 8, fontSize: '2rem' }}>
                    {aiChoice ? emojiMap[aiChoice] : '❓'}
                  </div>
                </div>
                <div>
                    <h2>VS</h2>
                </div>
                <div>

                </div>
            </div>
            <div className="App-player">
                <WebcamCapture />
            </div>
        </div>
    </div>
  );
}

export default App;
