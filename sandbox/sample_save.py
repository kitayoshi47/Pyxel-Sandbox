import pyxel
import json
import base64
import sys
import platform
try:
    from js import window
    from js import navigator
    is_web_launcher = True
except ImportError:
    is_web_launcher = False

is_run_desktop = False
is_run_web     = False

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
# Web版判定
# =====================================
def is_web_pyxel():
    return is_run_web

# =====================================
# データ変換
# =====================================
def serialize_data(data):
    # セーブデータをJSON文字列に変換する
    return json.dumps(data)

def deserialize_data(data_string):
    # JSON文字列をセーブデータに変換する
    if not data_string:
        return None
    try:
        return json.loads(data_string)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data.")
        return None

def encode_data_for_storage(data_string):
    # 文字列データをBase64でエンコード
    return base64.b64encode(data_string.encode('utf-8')).decode('utf-8')

def decode_data_from_storage(encoded_string):
    # Base64エンコードされた文字列データをデコード
    if not encoded_string:
        return ""
    try:
        # Base64デコードしてからバイト列を文字列に変換
        return base64.b64decode(encoded_string).decode('utf-8')
    except Exception as e:
        print(f"Error: Failed to decode Base64 data: {e}")
        return ""

# =====================================
# セーブ・ロード処理
# =====================================
# Web版LocalStorageのキー名
LOCALSTORAGE_KEY = "pyxel_sample_save_data"

# セーブ処理
def save_game_data(data):
    data_string = serialize_data(data)
    if data_string is None:
        print("Error: Failed to serialize save data.")
        return

    if is_web_pyxel():
        # Web版: LocalStorageに保存
        encoded_data = encode_data_for_storage(data_string)
        window.localStorage.setItem(LOCALSTORAGE_KEY, encoded_data)
        print("Game data saved to LocalStorage.")
    else:
        # デスクトップ版: pyxel.saveを使用して保存
        encoded_data = encode_data_for_storage(data_string)
        file_path = "savegame.pyxapp"
        try:
            print(f"Game data (as JSON string) would be saved to {file_path} on desktop.")
            import os
            current_dir = os.path.dirname(__file__)
            save_path = os.path.join(current_dir, file_path)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(encoded_data)
            print(f"Game data saved to {save_path}")

        except Exception as e:
            print(f"Error saving game data on desktop: {e}")

# ロード処理
def load_game_data():
    data_string = None

    if is_web_pyxel():
        # Web版: LocalStorageから読み込み
        encoded_data = window.localStorage.getItem(LOCALSTORAGE_KEY)
        if encoded_data:
            data_string = decode_data_from_storage(encoded_data)
            print("Game data loaded from LocalStorage.")
        else:
            print("No game data found in LocalStorage.")
    else:
        # デスクトップ版: ファイルから読み込み
        file_path = "savegame.pyxapp"
        try:
            print(f"Game data (as JSON string) would be loaded from {file_path} on desktop.")
            import os
            current_dir = os.path.dirname(__file__)
            load_path = os.path.join(current_dir, file_path)
            if os.path.exists(load_path):
                 with open(load_path, 'r', encoding='utf-8') as f:
                     encoded_data = f.read()
                     data_string = decode_data_from_storage(encoded_data)
            else:
                 data_string = None

        except Exception as e:
            print(f"Error loading game data on desktop: {e}")
            data_string = None

    if data_string:
        return deserialize_data(data_string)
    else:
        return None

# =====================================
# Pyxelアプリケーションテスト
# =====================================
class App:
    def __init__(self):
        global is_run_desktop
        global is_run_web
        if is_web_launcher:
            self.sys_name = navigator.userAgent.lower()
            is_run_desktop = not ("android" in self.sys_name or "iphone" in self.sys_name or "ipad" in self.sys_name)
            is_run_web = True
        else:
            self.sys_name = platform.system()
            is_run_desktop = self.sys_name == "Windows" or self.sys_name == "Darwin" or self.sys_name == "Linux"
            if self.sys_name.find("Mozilla") == -1:
                is_run_web = False

        self.score = 0
        self.player_x = 80
        self.player_y = 60
        self.items = []
        self.message = "Press S to Save, L to Load"

        # ゲーム開始時にセーブデータのロード試行
        loaded_data = load_game_data()
        if loaded_data:
            self.score = get_score(loaded_data)
            self.player_x, self.player_y = get_player_position(loaded_data)
            self.items = get_items(loaded_data)
            self.message = "Game data loaded!"
        else:
            self.message = "No save data found. Start new game."

        pyxel.init(160, 120)
        pyxel.run(self.update, self.draw)

    def update(self):
        # セーブデータの作成
        if pyxel.btnp(pyxel.KEY_S):
            data_to_save = create_save_data(self.score, self.player_x, self.player_y)
            save_game_data(data_to_save)
            self.message = "Game saved!"

        # セーブデータのロード
        if pyxel.btnp(pyxel.KEY_L):
            loaded_data = load_game_data()
            if loaded_data:
                self.score = get_score(loaded_data)
                self.player_x, self.player_y = get_player_position(loaded_data)
                self.items = get_items(loaded_data)
                self.message = "Game loaded!"
            else:
                self.message = "No save data found."

        # ゲーム状態の更新例
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
        pyxel.rect(self.player_x, self.player_y, 8, 8, 9) # プレイヤー表示
        pyxel.text(5, 15, f"Pos: ({self.player_x}, {self.player_y})", 7)
        pyxel.text(5, 25, f"Items: {', '.join(self.items)}", 7)
        pyxel.text(5, 40, self.message, 7)
        pyxel.text(5, 76, self.sys_name, 6)
        if is_run_desktop:
            pyxel.text(5, 84, "Run Desktop", 6)
        if is_run_web:
            pyxel.text(5, 92, "Run Web", 6)
        pyxel.text(5, 100, "Press S to Save, L to Load", 6)
        pyxel.text(5, 108, "Use arrow keys to move, A to add score", 6)

if __name__ == "__main__":
    App()
