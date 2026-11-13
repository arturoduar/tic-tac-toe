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

## 🚀 Running Locally

### Option A: Standard Python
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python3 app.py
   ```
3. Open [http://localhost:5001](http://localhost:5001).

### Option B: Docker
1. Build and run with Docker:
   ```bash
   docker build -t tic-tac-toe .
   docker run -p 8080:8080 -e PORT=8080 tic-tac-toe
   ```
   Or using Docker Compose:
   ```bash
   docker compose up --build
   ```
2. Open [http://localhost:8080](http://localhost:8080).

---

## ☁️ Cloud Deployment

The included `Dockerfile` follows cloud container standards (Cloud Native / 12-Factor App):
- Uses `gunicorn` with worker and thread pooling for concurrency.
- Reads dynamic `$PORT` from environment (required by Cloud Run, Render, Railway, Heroku, etc.).
- Runs as a non-root user (`appuser`) for cloud security compliance.

### Deploy to Google Cloud Run
```bash
# Authenticate & configure project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build & deploy directly from source
gcloud run deploy tic-tac-toe \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy to Railway / Render / Fly.io
1. Push this repository to GitHub or GitLab.
2. Link the repository in **Railway** or **Render**:
   - Both automatically detect the `Dockerfile` and configure port mapping via `$PORT`.
3. For **Fly.io**:
   ```bash
   fly launch
   fly deploy
   ```

### Deploy to AWS (App Runner or ECS)
1. Tag and push image to Amazon ECR:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
   docker build -t tic-tac-toe .
   docker tag tic-tac-toe:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/tic-tac-toe:latest
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/tic-tac-toe:latest
   ```
2. Deploy via AWS App Runner pointing to the ECR image (Port 8080).

---

## 🧪 Testing

Run unit & integration test suites:
```bash
python3 test_game.py
python3 test_app.py
```

---

## 📂 Project Structure

```
tic-tac-toe/
├── Dockerfile          # Production container specification (Python 3.12-slim + Gunicorn)
├── .dockerignore       # Docker build exclusions
├── docker-compose.yml  # Docker Compose config for local container testing
├── app.py              # Flask server and REST API endpoints
├── game.py             # Core game engine & Minimax AI algorithm
├── test_game.py        # Unit tests for the game engine & Minimax
├── test_app.py         # Integration tests for Flask endpoints
├── requirements.txt    # Python dependencies (Flask, Gunicorn)
├── static/
│   ├── style.css       # Modern dark-themed CSS with animations
│   └── app.js          # Client-side controller, Web Audio, & Confetti
└── templates/
    └── index.html      # Accessible semantic HTML5 layout
```
