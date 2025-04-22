import pyxel
import json
import base64
import sys

# --- セーブデータ構造の定義例 ---
# ここにゲームの状態などを定義します。
# JSONでシリアライズ可能なデータ型（辞書、リスト、数値、文字列、ブール値、None）を使用してください。
def create_save_data(score, player_x, player_y):
    return {
        "score": score,
        "player_position": {"x": player_x, "y": player_y},
        "items": ["item_a", "item_b"],
    }

# セーブデータから値を読み出すヘルパー関数
def get_score(data):
    return data.get("score", 0)

def get_player_position(data):
    pos = data.get("player_position", {"x": 0, "y": 0})
    return pos["x"], pos["y"]

def get_items(data):
    return data.get("items", [])

# --- 環境判定 ---
# pyxel.evalが存在するかどうかでWeb版かどうかを判定します。
# これはPyxel Webの内部実装に依存する可能性があるので、将来的に変わる可能性もあります。
def is_web_pyxel():
    return hasattr(pyxel, 'eval')

# --- データ変換 ---
def serialize_data(data):
    """セーブデータをJSON文字列に変換する"""
    return json.dumps(data)

def deserialize_data(data_string):
    """JSON文字列をセーブデータに変換する"""
    if not data_string:
        return None # データがない場合はNoneを返す
    try:
        return json.loads(data_string)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data.")
        return None

def encode_data_for_storage(data_string):
    """文字列データをBase64でエンコードする"""
    # バイト列に変換してからBase64エンコード
    return base64.b64encode(data_string.encode('utf-8')).decode('utf-8')

def decode_data_from_storage(encoded_string):
    """Base64エンコードされた文字列データをデコードする"""
    if not encoded_string:
        return "" # 空文字列の場合はそのまま返す
    try:
        # Base64デコードしてからバイト列を文字列に変換
        return base64.b64decode(encoded_string).decode('utf-8')
    except Exception as e:
        print(f"Error: Failed to decode Base64 data: {e}")
        return ""

# --- セーブ・ロード処理 ---

# Web版LocalStorageのキー名（アプリケーションごとにユニークな名前にする）
LOCALSTORAGE_KEY = "my_pyxel_game_save_data"

def save_game_data(data):
    """
    ゲームデータをセーブします。
    実行環境に応じて適切な方法を選択します。
    """
    data_string = serialize_data(data)
    if data_string is None:
        print("Error: Failed to serialize save data.")
        return

    if is_web_pyxel():
        # Web版: LocalStorageに保存
        encoded_data = encode_data_for_storage(data_string)
        # JavaScriptを使ってLocalStorageに保存
        # LocalStorage.setItem(key, value)
        pyxel.eval(f'localStorage.setItem("{LOCALSTORAGE_KEY}", "{encoded_data}");')
        print("Game data saved to LocalStorage.")
    else:
        # デスクトップ版: pyxel.saveを使用
        file_path = "savegame.pyxapp"
        try:
            print(f"Game data (as JSON string) would be saved to {file_path} on desktop.")

            import os
            current_dir = os.path.dirname(__file__)
            save_path = os.path.join(current_dir, file_path)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(data_string)
            print(f"Game data saved to {save_path}")

        except Exception as e:
            print(f"Error saving game data on desktop: {e}")

def load_game_data():
    """
    ゲームデータをロードします。
    実行環境に応じて適切な方法を選択します。
    データが見つからない場合はNoneを返します。
    """
    data_string = None

    if is_web_pyxel():
        # Web版: LocalStorageから読み込み
        # JavaScriptを使ってLocalStorageから読み込み
        # LocalStorage.getItem(key)
        encoded_data = pyxel.eval(f'localStorage.getItem("{LOCALSTORAGE_KEY}");')
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
                     data_string = f.read()
            else:
                 data_string = None


        except Exception as e:
            print(f"Error loading game data on desktop: {e}")
            data_string = None # エラー時はデータなしとする


    if data_string:
        return deserialize_data(data_string)
    else:
        return None # データがないか、デコードに失敗した場合はNone

# --- Pyxelアプリケーションの例 ---

class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.score = 0
        self.player_x = 80
        self.player_y = 60
        self.items = []
        self.message = "Press S to Save, L to Load"

        # ゲーム開始時にセーブデータをロードしてみる
        loaded_data = load_game_data()
        if loaded_data:
            self.score = get_score(loaded_data)
            self.player_x, self.player_y = get_player_position(loaded_data)
            self.items = get_items(loaded_data)
            self.message = "Game data loaded!"
        else:
            self.message = "No save data found. Start new game."


        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_S):
            # セーブデータの作成
            data_to_save = create_save_data(self.score, self.player_x, self.player_y)
            save_game_data(data_to_save)
            self.message = "Game saved!"

        if pyxel.btnp(pyxel.KEY_L):
            # セーブデータのロード
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
        pyxel.rect(self.player_x, self.player_y, 8, 8, 9) # プレイヤーの表示
        pyxel.text(5, 15, f"Pos: ({self.player_x}, {self.player_y})", 7)
        pyxel.text(5, 25, f"Items: {', '.join(self.items)}", 7)

        pyxel.text(5, 40, self.message, 7)

        pyxel.text(5, 100, "Press S to Save, L to Load", 6)
        pyxel.text(5, 108, "Use arrow keys to move, A to add score", 6)


if __name__ == "__main__":
    # デスクトップ版で実行する場合、このスクリプト自体を直接実行します。
    # Web版として出力するには、通常 pyxel app.py --html output_dir のようにコマンドを使用します。
    # Web版として出力後、生成されたindex.htmlを開いてください。
    App()
