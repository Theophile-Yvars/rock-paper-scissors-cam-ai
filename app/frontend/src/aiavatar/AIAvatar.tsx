import React, { useEffect, useRef, useState } from 'react';

interface AIAvatarProps {
  choice: 'pierre' | 'feuille' | 'ciseau' | null;
}

const emojiMap: Record<string, string> = {
  pierre: '🪨',
  feuille: '📄',
  ciseau: '✂️',
};

const AIAvatar: React.FC<AIAvatarProps> = ({ choice }) => {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      const deltaX = Math.floor(Math.random() * 7 - 3);
      const deltaY = Math.floor(Math.random() * 7 - 3);
      setPosition({ x: deltaX, y: deltaY });
    }, 100);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div
        style={{
          width: 128,
          height: 128,
          border: '2px solid #1e293b',
          borderRadius: 12,
          overflow: 'hidden',
          backgroundColor: '#0f172a',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <img
          src="/assets/opponent-picture.png" // doit être dans le dossier `public/assets`
          alt="AI Adversary"
          style={{
            transform: `translate(${position.x}px, ${position.y}px)`,
            transition: 'transform 0.1s linear',
            width: '80%',
            height: '80%',
          }}
        />
      </div>
      {choice && (
        <div style={{ marginTop: 8, fontSize: '2rem' }}>
          {emojiMap[choice]}
        </div>
      )}
    </div>
  );
};

export default AIAvatar;
