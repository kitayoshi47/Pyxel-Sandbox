import pyxel
import os
import json
import base64
import platform
try:
    from js import window
    from js import navigator
    is_web_launcher = True
except ImportError:
    is_web_launcher = False

# =====================================
# データ変換
# =====================================
# セーブデータをJSON文字列に変換
def serialize_data(data):
    return json.dumps(data)

# JSON文字列をセーブデータに変換
def deserialize_data(data_string):
    if not data_string:
        return None
    try:
        return json.loads(data_string)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data.")
        return None

# 文字列データをBase64でエンコード
def encode_data_for_storage(data_string):
    return base64.b64encode(data_string.encode('utf-8')).decode('utf-8')

# Base64エンコードされた文字列データをデコード
def decode_data_from_storage(encoded_string):
    if not encoded_string:
        return ""
    try:
        # Base64デコードしてからバイト列を文字列に変換
        return base64.b64decode(encoded_string).decode('utf-8')
    except Exception as e:
        print(f"Error: Failed to decode Base64 data: {e}")
        return ""

# =====================================
# セーブデータクラス
# =====================================
class CSaveData:
    # --------------------
    # 初期化
    # --------------------
    def __init__(self, vendor_name, app_name):
        self.save_name  = app_name + ".pyxapp_save"
        self.user_dir   = pyxel.user_data_dir(vendor_name, app_name)
        self.is_desktop = False
        self.is_browser = False
        if is_web_launcher:
            self.sys_name = navigator.userAgent.lower()
            self.is_desktop = not ("android" in self.sys_name or "iphone" in self.sys_name or "ipad" in self.sys_name)
            self.is_browser = True
        else:
            self.sys_name = platform.system()
            self.is_desktop = self.sys_name == "Windows" or self.sys_name == "Darwin" or self.sys_name == "Linux"
            if self.sys_name.find("Mozilla") == -1:
                self.is_browser = False
        print(self.is_desktop)
        print(self.is_browser)
        print(self.sys_name)

    def is_run_desktop(self):
        return self.is_desktop

    def is_run_browser(self):
        return self.is_browser

    def get_sys_name(self):
        return self.sys_name

    # --------------------
    # セーブ処理
    # --------------------
    def save(self, data):
        data_string = serialize_data(data)
        if data_string is None:
            print("Error: Failed to serialize save data.")
            return

        if self.is_browser:
            # ブラウザ版: LocalStorageに保存
            encoded_data = encode_data_for_storage(data_string)
            window.localStorage.setItem(self.save_name, encoded_data)
            print("Game data saved to LocalStorage.")
        else:
            # デスクトップ版: ファイルに保存
            encoded_data = encode_data_for_storage(data_string)
            file_path = self.user_dir + self.save_name
            try:
                print(f"Game data as string would be saved to {file_path} on desktop.")
                current_dir = os.path.dirname(__file__)
                save_path = os.path.join(current_dir, file_path)
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(encoded_data)
                print(f"Game data saved to {save_path}")

            except Exception as e:
                print(f"Error saving game data on desktop: {e}")

    # --------------------
    # ロード処理
    # --------------------
    def load(self):
        data_string = None

        if self.is_browser:
            # ブラウザ版: LocalStorageから読み込み
            encoded_data = window.localStorage.getItem(self.save_name)
            if encoded_data:
                data_string = decode_data_from_storage(encoded_data)
                print("Game data loaded from LocalStorage.")
            else:
                print("No game data found in LocalStorage.")
        else:
            # デスクトップ版: ファイルから読み込み
            file_path = self.user_dir + self.save_name
            try:
                print(f"Game data as string would be loaded from {file_path} on desktop.")
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
