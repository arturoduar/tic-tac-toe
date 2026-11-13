"""
Flask Web Application for Tic-Tac-Toe.
"""

import os
import uuid
import time
from flask import Flask, render_template, jsonify, request, session
from game import TicTacToeGame

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24).hex())

# In-memory storage for active games: game_id -> {"game": TicTacToeGame, "scores": dict, "last_active": float}
GAMES = {}
MAX_GAMES = 1000


def clean_old_games():
    """Periodically purge games inactive for over 2 hours."""
    now = time.time()
    if len(GAMES) > MAX_GAMES:
        expired = [gid for gid, data in GAMES.items() if now - data["last_active"] > 7200]
        for gid in expired:
            del GAMES[gid]


def get_or_create_game_session():
    clean_old_games()
    game_id = session.get("game_id")
    if not game_id or game_id not in GAMES:
        game_id = str(uuid.uuid4())
        session["game_id"] = game_id
        GAMES[game_id] = {
            "game": TicTacToeGame(mode="ai_hard", human_player="X"),
            "scores": {"X": 0, "O": 0, "draw": 0},
            "last_active": time.time(),
        }
    else:
        GAMES[game_id]["last_active"] = time.time()

    return GAMES[game_id]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    session_data = get_or_create_game_session()
    game: TicTacToeGame = session_data["game"]
    data = game.to_dict()
    data["scores"] = session_data["scores"]
    return jsonify(data)


@app.route("/api/move", methods=["POST"])
def make_move():
    session_data = get_or_create_game_session()
    game: TicTacToeGame = session_data["game"]
    scores = session_data["scores"]

    payload = request.get_json(silent=True) or {}
    index = payload.get("index")

    if index is None or not isinstance(index, int):
        return jsonify({"error": "Invalid move index"}), 400

    prev_over = game.game_over
    success = game.make_move(index)

    if not success:
        return jsonify({"error": "Illegal move", "state": game.to_dict()}), 400

    # If game just ended, increment score
    if not prev_over and game.game_over and game.winner:
        if game.winner in scores:
            scores[game.winner] += 1

    data = game.to_dict()
    data["scores"] = scores
    return jsonify(data)


@app.route("/api/reset", methods=["POST"])
def reset_game():
    session_data = get_or_create_game_session()
    game: TicTacToeGame = session_data["game"]
    payload = request.get_json(silent=True) or {}
    alternate = payload.get("alternate", False)

    game.reset(alternate_starter=alternate)
    data = game.to_dict()
    data["scores"] = session_data["scores"]
    return jsonify(data)


@app.route("/api/settings", methods=["POST"])
def update_settings():
    session_data = get_or_create_game_session()
    game: TicTacToeGame = session_data["game"]
    payload = request.get_json(silent=True) or {}

    mode = payload.get("mode")
    human_player = payload.get("humanPlayer")

    game.set_settings(mode=mode, human_player=human_player)
    # Reset scores on mode change if requested
    if payload.get("resetScores"):
        session_data["scores"] = {"X": 0, "O": 0, "draw": 0}

    data = game.to_dict()
    data["scores"] = session_data["scores"]
    return jsonify(data)


@app.route("/api/undo", methods=["POST"])
def undo():
    session_data = get_or_create_game_session()
    game: TicTacToeGame = session_data["game"]
    success = game.undo_move()
    data = game.to_dict()
    data["scores"] = session_data["scores"]
    data["undoSuccess"] = success
    return jsonify(data)


@app.route("/api/reset_scores", methods=["POST"])
def reset_scores():
    session_data = get_or_create_game_session()
    session_data["scores"] = {"X": 0, "O": 0, "draw": 0}
    return jsonify({"scores": session_data["scores"]})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"Starting Tic-Tac-Toe server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
