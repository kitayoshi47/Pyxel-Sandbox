import pyxel
import sys_save

# =====================================
# セーブデータ構造定義
# =====================================
def create_save_data(score, player_x, player_y):
    return {
        "score": score,
        "player_position": {"x": player_x, "y": player_y},
        "items": ["item_a", "item_b"],
    }

# =====================================
# セーブデータから値を読み出す
# =====================================
def get_score(data):
    return data.get("score", 0)

def get_player_position(data):
    pos = data.get("player_position", {"x": 0, "y": 0})
    return pos["x"], pos["y"]

def get_items(data):
    return data.get("items", [])

# =====================================
# テストアプリケーション
# =====================================
class App:
    def __init__(self):
        pyxel.init(160, 120)

        self.save_data = sys_save.CSaveData("Kitayochi", "TestApp")
        self.score     = 0
        self.player_x  = 80
        self.player_y  = 60
        self.items     = []
        self.message   = "Press S to Save, L to Load"

        # ゲーム開始時にセーブデータのロード試行
        loaded_data = self.save_data.load()
        if loaded_data:
            self.score = get_score(loaded_data)
            self.player_x, self.player_y = get_player_position(loaded_data)
            self.items = get_items(loaded_data)
            self.message = "Game data loaded!"
        else:
            self.message = "No save data found. Start new game."

        pyxel.run(self.update, self.draw)

    def update(self):
        # セーブデータの作成
        if pyxel.btnp(pyxel.KEY_S):
            data_to_save = create_save_data(self.score, self.player_x, self.player_y)
            self.save_data.save(data_to_save)
            self.message = "Game saved!"

        # セーブデータのロード
        if pyxel.btnp(pyxel.KEY_L):
            loaded_data = self.save_data.load()
            if loaded_data:
                self.score = get_score(loaded_data)
                self.player_x, self.player_y = get_player_position(loaded_data)
                self.items = get_items(loaded_data)
                self.message = "Game loaded!"
            else:
                self.message = "No save data found."

        # ゲーム状態の更新
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 1, 159)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 1, 0)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y = min(self.player_y + 1, 119)
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = max(self.player_y - 1, 0)
        if pyxel.btnp(pyxel.KEY_A):
            self.score += 10

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.rect(self.player_x, self.player_y, 8, 8, 9)
        pyxel.text(5, 15, f"Pos: ({self.player_x}, {self.player_y})", 7)
        pyxel.text(5, 25, f"Items: {', '.join(self.items)}", 7)
        pyxel.text(5, 40, self.message, 7)
        pyxel.text(5, 76, self.save_data.get_sys_name(), 6)
        if self.save_data.is_run_desktop():
            pyxel.text(5, 84, "Run Desktop", 6)
        if self.save_data.is_run_browser():
            pyxel.text(5, 92, "Run Browser", 6)
        pyxel.text(5, 100, "Press S to Save, L to Load", 6)
        pyxel.text(5, 108, "Use arrow keys to move, A to add score", 6)
App()
