# 🎮 Modern Tic-Tac-Toe Web App (Python + Flask)

A sleek, responsive, and accessible Tic-Tac-Toe web application built with **Python 3**, **Flask**, and an unbeatable **Minimax AI** engine.

---

## ✨ Features

- **Multiple Game Modes**:
  - 🤖 **AI: Unbeatable (Minimax)**: Pure game theory optimal decision tree with depth optimization.
  - 🤖 **AI: Medium**: Balanced blend of tactical play and casual difficulty.
  - 🤖 **AI: Easy**: Casual randomized moves.
  - 👥 **Pass & Play (2 Players)**: Local multiplayer on the same device.
- **Customizable Player Symbol**: Play as **X** (first turn) or **O** (second turn vs AI).
- **Interactive Audio & Visuals**:
  - Web Audio API synthesizer for moves, wins, and draws (no external audio files required, toggleable mute).
  - Pure Canvas confetti burst celebration on victory.
  - Glowing winning line animation.
- **Accessibility & Keyboard Navigable**:
  - Fully navigable using `Arrow Keys` + `Enter`/`Space`.
  - ARIA grid semantics (`role="grid"`, `role="row"`, `role="gridcell"`).
  - High contrast visual cues and screen reader announcements.
- **Round & Score Tracking**:
  - Real-time score counter for Player X, Player O / AI, and Ties.
  - Undo move support.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.9+
- Flask (`pip install -r requirements.txt`)

### 2. Run the Application
```bash
python3 app.py
```
By default, the server will start on [http://localhost:5001](http://localhost:5001).

### 3. Run the Test Suite
```bash
python3 test_game.py
python3 test_app.py
```

---

## 📂 Project Structure

```
tic-tac-toe/
├── app.py              # Flask server and REST API endpoints
├── game.py             # Core game engine & Minimax AI algorithm
├── test_game.py        # Unit tests for the game engine & Minimax
├── test_app.py         # Integration tests for Flask endpoints
├── requirements.txt    # Python dependencies
├── static/
│   ├── style.css       # Modern dark-themed CSS with animations
│   └── app.js          # Client-side controller, Web Audio, & Confetti
└── templates/
    └── index.html      # Accessible semantic HTML5 layout
```
