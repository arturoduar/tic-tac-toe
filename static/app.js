/**
 * Frontend logic for Tic-Tac-Toe Web App.
 */

// Sound effects synthesizer via Web Audio API
class SoundFx {
  constructor() {
    this.audioCtx = null;
    this.muted = localStorage.getItem("ttt_sound_muted") === "true";
  }

  init() {
    if (!this.audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
      }
    }
    if (this.audioCtx && this.audioCtx.state === "suspended") {
      this.audioCtx.resume();
    }
  }

  toggle() {
    this.muted = !this.muted;
    localStorage.setItem("ttt_sound_muted", this.muted ? "true" : "false");
    return !this.muted;
  }

  playMove(isX) {
    if (this.muted) return;
    this.init();
    if (!this.audioCtx) return;

    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();
    osc.type = isX ? "triangle" : "sine";
    const freq = isX ? 440 : 587.33; // A4 or D5
    osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(freq * 1.5, this.audioCtx.currentTime + 0.08);

    gain.gain.setValueAtTime(0.15, this.audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + 0.12);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc.start();
    osc.stop(this.audioCtx.currentTime + 0.12);
  }

  playWin() {
    if (this.muted) return;
    this.init();
    if (!this.audioCtx) return;

    const notes = [523.25, 659.25, 783.99, 1046.5]; // C5, E5, G5, C6
    notes.forEach((freq, idx) => {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      const startTime = this.audioCtx.currentTime + idx * 0.09;

      osc.type = "sine";
      osc.frequency.setValueAtTime(freq, startTime);

      gain.gain.setValueAtTime(0.18, startTime);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.35);

      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      osc.start(startTime);
      osc.stop(startTime + 0.35);
    });
  }

  playDraw() {
    if (this.muted) return;
    this.init();
    if (!this.audioCtx) return;

    const notes = [440, 415.3, 392]; // Downward notes
    notes.forEach((freq, idx) => {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      const startTime = this.audioCtx.currentTime + idx * 0.1;

      osc.type = "triangle";
      osc.frequency.setValueAtTime(freq, startTime);

      gain.gain.setValueAtTime(0.12, startTime);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.25);

      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      osc.start(startTime);
      osc.stop(startTime + 0.25);
    });
  }

  playReset() {
    if (this.muted) return;
    this.init();
    if (!this.audioCtx) return;

    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(300, this.audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(600, this.audioCtx.currentTime + 0.08);

    gain.gain.setValueAtTime(0.08, this.audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + 0.1);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc.start();
    osc.stop(this.audioCtx.currentTime + 0.1);
  }
}

// Canvas Confetti
class Confetti {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.particles = [];
    this.animId = null;
    this.resize();
    window.addEventListener("resize", () => this.resize());
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  burst() {
    this.particles = [];
    const colors = ["#38bdf8", "#f43f5e", "#10b981", "#fbbf24", "#a855f7", "#ec4899"];
    for (let i = 0; i < 90; i++) {
      this.particles.push({
        x: this.canvas.width * (0.3 + Math.random() * 0.4),
        y: this.canvas.height * (0.3 + Math.random() * 0.2),
        vx: (Math.random() - 0.5) * 14,
        vy: (Math.random() - 0.7) * 16,
        size: Math.random() * 7 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        rotationSpeed: (Math.random() - 0.5) * 12,
        opacity: 1,
        life: 1,
      });
    }

    if (this.animId) cancelAnimationFrame(this.animId);
    this.render();
  }

  render() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.35; // Gravity
      p.vx *= 0.98; // Friction
      p.rotation += p.rotationSpeed;
      p.life -= 0.012;

      if (p.life <= 0) {
        this.particles.splice(i, 1);
        continue;
      }

      this.ctx.save();
      this.ctx.translate(p.x, p.y);
      this.ctx.rotate((p.rotation * Math.PI) / 180);
      this.ctx.fillStyle = p.color;
      this.ctx.globalAlpha = Math.max(0, p.life);
      this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
      this.ctx.restore();
    }

    if (this.particles.length > 0) {
      this.animId = requestAnimationFrame(() => this.render());
    } else {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.animId = null;
    }
  }
}

// Main Game Controller
class App {
  constructor() {
    this.sound = new SoundFx();
    this.confetti = new Confetti(document.getElementById("confettiCanvas"));
    this.state = null;
    this.isRequestInProgress = false;

    // DOM Elements
    this.cells = Array.from(document.querySelectorAll(".board-cell"));
    this.boardGrid = document.getElementById("boardGrid");
    this.gameModeSelect = document.getElementById("gameMode");
    this.symbolBtns = document.querySelectorAll(".symbol-btn");
    this.playerChoiceGroup = document.getElementById("playerChoiceGroup");
    this.statusBanner = document.getElementById("statusBanner");
    this.statusText = document.getElementById("statusText");
    this.turnDot = document.getElementById("turnDot");
    this.nameX = document.getElementById("nameX");
    this.nameO = document.getElementById("nameO");
    this.scoreX = document.getElementById("scoreX");
    this.scoreO = document.getElementById("scoreO");
    this.scoreTies = document.getElementById("scoreTies");
    this.cardX = document.getElementById("cardX");
    this.cardO = document.getElementById("cardO");
    this.soundToggle = document.getElementById("soundToggle");
    this.soundIcon = document.getElementById("soundIcon");
    this.btnResetRound = document.getElementById("btnResetRound");
    this.btnUndo = document.getElementById("btnUndo");
    this.btnResetScores = document.getElementById("btnResetScores");

    this.initEvents();
    this.initSoundButton();
    this.fetchState();
  }

  initSoundButton() {
    this.soundIcon.textContent = this.sound.muted ? "🔇" : "🔊";
    this.soundToggle.setAttribute("aria-label", this.sound.muted ? "Sound muted" : "Sound enabled");
  }

  initEvents() {
    // Cell clicks
    this.cells.forEach((cell) => {
      cell.addEventListener("click", () => {
        const idx = parseInt(cell.dataset.index, 10);
        this.makeMove(idx);
      });
    });

    // Keyboard navigation in grid
    this.boardGrid.addEventListener("keydown", (e) => {
      const activeElement = document.activeElement;
      if (!activeElement || !activeElement.classList.contains("board-cell")) return;
      const currentIdx = parseInt(activeElement.dataset.index, 10);
      let nextIdx = currentIdx;

      switch (e.key) {
        case "ArrowRight":
          nextIdx = (currentIdx + 1) % 9;
          break;
        case "ArrowLeft":
          nextIdx = (currentIdx - 1 + 9) % 9;
          break;
        case "ArrowDown":
          nextIdx = (currentIdx + 3) % 9;
          break;
        case "ArrowUp":
          nextIdx = (currentIdx - 3 + 9) % 9;
          break;
        case "Enter":
        case " ":
          e.preventDefault();
          this.makeMove(currentIdx);
          return;
        default:
          return;
      }
      e.preventDefault();
      const targetCell = this.cells[nextIdx];
      if (targetCell) targetCell.focus();
    });

    // Game mode select
    this.gameModeSelect.addEventListener("change", () => {
      const mode = this.gameModeSelect.value;
      this.updatePlayerChoiceVisibility(mode);
      this.updateSettings({ mode, resetScores: false });
    });

    // Human player symbol toggle
    this.symbolBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const symbol = btn.dataset.symbol;
        this.symbolBtns.forEach((b) => {
          b.classList.toggle("active", b === btn);
          b.setAttribute("aria-checked", b === btn ? "true" : "false");
        });
        this.updateSettings({ humanPlayer: symbol, resetScores: false });
      });
    });

    // Sound toggle button
    this.soundToggle.addEventListener("click", () => {
      const isUnmuted = this.sound.toggle();
      this.soundIcon.textContent = isUnmuted ? "🔊" : "🔇";
      this.soundToggle.setAttribute("aria-label", isUnmuted ? "Sound enabled" : "Sound muted");
      if (isUnmuted) this.sound.playReset();
    });

    // Reset Round button
    this.btnResetRound.addEventListener("click", () => {
      this.sound.playReset();
      this.resetRound(true);
    });

    // Undo button
    this.btnUndo.addEventListener("click", () => {
      this.undoMove();
    });

    // Reset Scores button
    this.btnResetScores.addEventListener("click", () => {
      this.resetScores();
    });
  }

  updatePlayerChoiceVisibility(mode) {
    if (mode === "pvp") {
      this.playerChoiceGroup.style.display = "none";
    } else {
      this.playerChoiceGroup.style.display = "flex";
    }
  }

  async fetchState() {
    try {
      const res = await fetch("/api/state");
      const data = await res.json();
      this.applyState(data);
    } catch (err) {
      console.error("Error fetching state:", err);
    }
  }

  async makeMove(index) {
    if (this.isRequestInProgress || !this.state) return;
    if (this.state.gameOver || this.state.board[index] !== "") return;

    // Check if it's the human's turn in vs AI
    const isAi = this.state.mode !== "pvp";
    if (isAi && this.state.currentPlayer !== this.state.humanPlayer) {
      return;
    }

    this.isRequestInProgress = true;
    const playerWhoMoved = this.state.currentPlayer;

    try {
      const res = await fetch("/api/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index }),
      });

      if (!res.ok) {
        const err = await res.json();
        console.warn("Move rejected:", err);
        return;
      }

      const data = await res.json();
      this.sound.playMove(playerWhoMoved === "X");
      this.applyState(data, index);
    } catch (err) {
      console.error("Move request failed:", err);
    } finally {
      this.isRequestInProgress = false;
    }
  }

  async resetRound(alternate = false) {
    try {
      const res = await fetch("/api/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ alternate }),
      });
      const data = await res.json();
      this.applyState(data);
    } catch (err) {
      console.error("Reset round failed:", err);
    }
  }

  async updateSettings(settings) {
    try {
      const res = await fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
      });
      const data = await res.json();
      this.sound.playReset();
      this.applyState(data);
    } catch (err) {
      console.error("Updating settings failed:", err);
    }
  }

  async undoMove() {
    try {
      const res = await fetch("/api/undo", {
        method: "POST",
      });
      const data = await res.json();
      this.applyState(data);
    } catch (err) {
      console.error("Undo failed:", err);
    }
  }

  async resetScores() {
    try {
      const res = await fetch("/api/reset_scores", {
        method: "POST",
      });
      const data = await res.json();
      if (data.scores) {
        this.scoreX.textContent = data.scores.X || 0;
        this.scoreO.textContent = data.scores.O || 0;
        this.scoreTies.textContent = data.scores.draw || 0;
      }
    } catch (err) {
      console.error("Reset scores failed:", err);
    }
  }

  applyState(data, lastMovedIndex = null) {
    const prevState = this.state;
    this.state = data;

    // Sync select dropdown if changed
    if (this.gameModeSelect.value !== data.mode) {
      this.gameModeSelect.value = data.mode;
      this.updatePlayerChoiceVisibility(data.mode);
    }

    // Sync symbol buttons
    this.symbolBtns.forEach((btn) => {
      const isHuman = btn.dataset.symbol === data.humanPlayer;
      btn.classList.toggle("active", isHuman);
      btn.setAttribute("aria-checked", isHuman ? "true" : "false");
    });

    // Update names in scorecards
    const isAi = data.mode !== "pvp";
    if (isAi) {
      if (data.humanPlayer === "X") {
        this.nameX.textContent = "You (X)";
        this.nameO.textContent = "AI (O)";
      } else {
        this.nameX.textContent = "AI (X)";
        this.nameO.textContent = "You (O)";
      }
    } else {
      this.nameX.textContent = "Player X";
      this.nameO.textContent = "Player O";
    }

    // Update scores
    if (data.scores) {
      this.scoreX.textContent = data.scores.X;
      this.scoreO.textContent = data.scores.O;
      this.scoreTies.textContent = data.scores.draw;
    }

    // Update Board Cells
    data.board.forEach((val, idx) => {
      const cell = this.cells[idx];
      const prevVal = cell.textContent.trim();
      cell.className = "board-cell"; // reset classes

      if (val === "X") {
        cell.classList.add("cell-x");
        cell.textContent = "✕";
        cell.setAttribute("aria-label", `Row ${Math.floor(idx / 3) + 1}, Column ${(idx % 3) + 1}, X`);
      } else if (val === "O") {
        cell.classList.add("cell-o");
        cell.textContent = "○";
        cell.setAttribute("aria-label", `Row ${Math.floor(idx / 3) + 1}, Column ${(idx % 3) + 1}, O`);
      } else {
        cell.textContent = "";
        cell.setAttribute("aria-label", `Row ${Math.floor(idx / 3) + 1}, Column ${(idx % 3) + 1}, Empty`);
      }

      // Pop-in animation for newly placed cell
      if (val && !prevVal) {
        cell.classList.add("cell-pop");
      }
    });

    // Highlight winning line if game over
    if (data.winningLine) {
      data.winningLine.forEach((idx) => {
        this.cells[idx].classList.add("cell-win");
      });
    }

    // Active scorecard indicator
    this.cardX.classList.toggle("active-turn", !data.gameOver && data.currentPlayer === "X");
    this.cardO.classList.toggle("active-turn", !data.gameOver && data.currentPlayer === "O");

    // Status Banner & Turn Dot
    this.statusBanner.className = "status-banner";
    if (data.gameOver) {
      this.turnDot.style.display = "none";
      if (data.winner === "draw") {
        this.statusBanner.classList.add("draw-banner");
        this.statusText.textContent = "Game ended in a Draw! 🤝";
        if (!prevState || !prevState.gameOver) {
          this.sound.playDraw();
        }
      } else {
        this.statusBanner.classList.add("win-banner");
        const winnerLabel = isAi
          ? data.winner === data.humanPlayer
            ? "You win! 🎉"
            : "AI wins! 🤖"
          : `Player ${data.winner} wins! 🎉`;
        this.statusText.textContent = winnerLabel;

        if (!prevState || !prevState.gameOver) {
          this.sound.playWin();
          this.confetti.burst();
        }
      }
    } else {
      this.turnDot.style.display = "inline-block";
      this.turnDot.className = "turn-indicator-dot " + (data.currentPlayer === "O" ? "dot-o" : "");
      const isCurrentHuman = !isAi || data.currentPlayer === data.humanPlayer;
      const turnLabel = isAi
        ? isCurrentHuman
          ? `Your turn (${data.currentPlayer})`
          : `AI thinking (${data.currentPlayer})...`
        : `Player ${data.currentPlayer}'s turn`;
      this.statusText.textContent = turnLabel;
    }
  }
}

// Start app when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  window.tttApp = new App();
});
