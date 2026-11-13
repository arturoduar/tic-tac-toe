"""
Integration tests for the Flask web endpoints.
"""

import unittest
from app import app, GAMES


class TestTicTacToeApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        GAMES.clear()

    def test_index_route(self):
        # We haven't created index.html yet, but we will test after templates are added
        pass

    def test_api_state(self):
        res = self.client.get("/api/state")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("board", data)
        self.assertEqual(len(data["board"]), 9)
        self.assertIn("scores", data)
        self.assertEqual(data["mode"], "ai_hard")

    def test_api_settings_pvp(self):
        res = self.client.post(
            "/api/settings",
            json={"mode": "pvp", "humanPlayer": "X", "resetScores": True},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["mode"], "pvp")
        self.assertEqual(data["scores"], {"X": 0, "O": 0, "draw": 0})

    def test_api_move(self):
        self.client.post("/api/settings", json={"mode": "pvp"})
        res = self.client.post("/api/move", json={"index": 0})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["board"][0], "X")
        self.assertEqual(data["currentPlayer"], "O")

    def test_api_invalid_move(self):
        self.client.post("/api/settings", json={"mode": "pvp"})
        self.client.post("/api/move", json={"index": 0})
        # Move on already occupied cell
        res = self.client.post("/api/move", json={"index": 0})
        self.assertEqual(res.status_code, 400)

    def test_api_reset(self):
        self.client.post("/api/settings", json={"mode": "pvp"})
        self.client.post("/api/move", json={"index": 0})
        res = self.client.post("/api/reset", json={"alternate": False})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["board"], [""] * 9)


if __name__ == "__main__":
    unittest.main()
