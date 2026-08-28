const screens = Array.from(document.querySelectorAll('.screen'));
const screen1Button = document.getElementById('go-to-screen2');
const screen3Button = document.getElementById('go-to-screen4');
const backButtons = document.querySelectorAll('.back-btn');
const scoreLabel = document.getElementById('score');
const gameArea = document.getElementById('game-area');
const envelope = document.getElementById('envelope');
const paperCard = document.getElementById('paperCard');
const messageCanvas = document.getElementById('messageCanvas');

let currentScreen = 1;
let gameIntervalId = null;
let gameActive = false;
let score = 0;

function setScreen(screenNumber) {
  currentScreen = screenNumber;
  screens.forEach((screen) => {
    const shouldShow = screen.id === `screen${screenNumber}`;
    screen.classList.toggle('hidden', !shouldShow);
  });

  if (screenNumber === 2) {
    startGame();
  } else {
    stopGame();
  }
}

function sparkleConfetti(options = {}) {
  if (typeof confetti === 'function') {
    confetti({
      particleCount: 80,
      spread: 80,
      startVelocity: 45,
      colors: ['#ff6b8a', '#ffd166', '#37c9bf', '#ff9f1c', '#ff5d8f', '#ffd8e8'],
      ...options,
    });
  }
}

function startGame() {
  stopGame();
  score = 0;
  gameActive = true;
  scoreLabel.textContent = 'Hearts Caught: 0/5';
  gameArea.innerHTML = '';

  spawnHeart();
  gameIntervalId = window.setInterval(() => {
    if (gameActive) {
      spawnHeart();
    }
  }, 1200);
}

function stopGame() {
  gameActive = false;
  if (gameIntervalId) {
    clearInterval(gameIntervalId);
    gameIntervalId = null;
  }
  if (gameArea) {
    gameArea.innerHTML = '';
  }
}

function spawnHeart() {
  if (!gameActive || !gameArea) return;

  const heart = document.createElement('button');
  heart.type = 'button';
  heart.className = 'heart-chip';
  heart.setAttribute('aria-label', 'heart');
  heart.textContent = '❤️';

  const maxX = Math.max(0, gameArea.clientWidth - 54);
  const maxY = Math.max(0, gameArea.clientHeight - 54);
  const x = Math.random() * maxX;
  const y = Math.random() * maxY;

  heart.style.left = `${x}px`;
  heart.style.top = `${y}px`;

  heart.addEventListener('click', (event) => {
    event.stopPropagation();
    if (!heart.classList.contains('clicked')) {
      heart.classList.add('clicked');
      setTimeout(() => heart.remove(), 220);
      score += 1;
      scoreLabel.textContent = `Hearts Caught: ${score}/5`;
      sparkleConfetti({
        particleCount: 24,
        spread: 45,
        origin: {
          x: (x + 27) / Math.max(1, gameArea.clientWidth),
          y: (y + 27) / Math.max(1, gameArea.clientHeight),
        },
      });

      if (score >= 5) {
        completeGame();
      }
    }
  });

  gameArea.appendChild(heart);
}

function completeGame() {
  stopGame();
  sparkleConfetti({
    particleCount: 180,
    spread: 120,
    startVelocity: 38,
    origin: { y: 0.6 },
  });
  window.setTimeout(() => {
    setScreen(3);
  }, 1500);
}

function renderPixelatedMessage() {
  if (!messageCanvas) return;

  const ctx = messageCanvas.getContext('2d');
  const buffer = document.createElement('canvas');
  buffer.width = 180;
  buffer.height = 260;
  const bufferCtx = buffer.getContext('2d');

  bufferCtx.fillStyle = '#fffdfd';
  bufferCtx.fillRect(0, 0, buffer.width, buffer.height);
  bufferCtx.fillStyle = '#8a67c7';
  bufferCtx.font = 'bold 26px Nunito';
  bufferCtx.textAlign = 'center';
  bufferCtx.textBaseline = 'middle';

  const lines = [
    'HAPPY BIRTHDAY',
    'MY LOVE',
    'You make every day',
    'feel so special.',
    'I hope your heart',
    'stays as warm as',
    'your smile.',
    'Love you always 💜'
  ];

  lines.forEach((line, index) => {
    const y = 60 + index * 28;
    bufferCtx.fillText(line, buffer.width / 2, y);
  });

  ctx.imageSmoothingEnabled = false;
  ctx.clearRect(0, 0, messageCanvas.width, messageCanvas.height);
  ctx.drawImage(buffer, 0, 0, messageCanvas.width, messageCanvas.height);
}

function openEnvelope() {
  if (!envelope || envelope.classList.contains('open')) return;
  envelope.classList.add('open');
  envelope.classList.add('hide');
  paperCard?.classList.add('show');
  renderPixelatedMessage();
  sparkleConfetti({
    particleCount: 120,
    spread: 90,
    startVelocity: 40,
    origin: { y: 0.4 },
  });
}

screen1Button?.addEventListener('click', () => {
  setScreen(2);
});

screen3Button?.addEventListener('click', () => {
  setScreen(4);
});

backButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const target = Number(button.dataset.target);
    if (!Number.isNaN(target)) {
      setScreen(target);
    }
  });
});

envelope?.addEventListener('click', openEnvelope);
envelope?.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    openEnvelope();
  }
});

window.addEventListener('load', () => {
  setScreen(1);
  window.setTimeout(() => {
    sparkleConfetti({
      particleCount: 160,
      spread: 100,
      startVelocity: 48,
      origin: { y: 0.7 },
    });
  }, 220);
});
