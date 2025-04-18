# title: Pyxel-Sandbox
# author: Kitayochi
# desc: sandbox
# site: https://github.com/kitayoshi47/Pyxel-Sandbox
# license: MIT
# version: 0.1

import pyxel
import time

#======================================
# 定数定義
#======================================
APP_TITLE       = "Pyxel Test"          # タイトル
SCREEN_WIDTH    = 256                   # スクリーンサイズ幅
SCREEN_HEIGHT   = 256                   # スクリーンサイズ高さ

#======================================
# ベクトル3
#======================================
class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

#======================================
# ポリゴン
#======================================
class Polygon:
    def __init__(self):
        self.p0 = Vec3(0, 0, 0)
        self.p1 = Vec3(0, 0, 0)
        self.p2 = Vec3(0, 0, 0)

    def set_point(self, n, x, y, z):
        if n == 0:
            self.p0.x = x
            self.p0.y = y
            self.p0.z = z
        if n == 1:
            self.p1.x = x
            self.p1.y = y
            self.p1.z = z
        if n == 2:
            self.p2.x = x
            self.p2.y = y
            self.p2.z = z

#======================================
# FPS計測クラス
#======================================
FPS_INTERVAL = 0.5 # FPS更新間隔
FPS_PRINT    = 1   # FPS表示(0:OFF/1:ON)
class Fps:
    def __init__(self):
        self.time_start  = 0
        self.time_prev   = 0
        self.frame_count = 0
        self.fps         = 0

    def start(self):
        self.frame_count += 1
        self.time_start = time.time() - self.time_prev

    def end(self):
        if self.time_start >= FPS_INTERVAL:
            self.fps = self.frame_count / self.time_start
            self.frame_count = 0
            self.time_prev = time.time()

    def print(self, x, y):
        if FPS_PRINT == 1:
            pyxel.text(x, y, str(self.fps)[:5], 7)

#======================================
# アプリケーションクラス
#======================================
class App:
    # 初期化
    def __init__(self):
        self.fps = Fps()
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=APP_TITLE)
        pyxel.run(self.update, self.draw)

    # 更新
    def update(self):
        self.fps.start()
        self.update_scene()
        self.fps.end()

    # 更新(実処理)
    def update_scene(self):
        #ESCキーで終了
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

    # 描画
    def draw(self):
        pyxel.cls(0)
        self.fps.print(0, 0)

App()
