# title: Pyxel-Sandbox
# author: Kitayochi
# desc: sandbox
# site: https://github.com/kitayoshi47/Pyxel-Sandbox
# license: MIT
# version: 0.1

import pyxel
import time

APP_TITLE       = "Pyxel Test"          #タイトル
SCREEN_WIDTH    = 256                   #スクリーンサイズ幅
SCREEN_HEIGHT   = 256                   #スクリーンサイズ高さ
FPS_INTERVAL    = 0.5                   #FPS更新間隔

class App:
    #初期化
    def __init__(self):
        self.time_start  = 0
        self.time_prev   = 0
        self.frame_count = 0
        self.fps         = 0
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=APP_TITLE)
        pyxel.run(self.update, self.draw)

    #フレーム計測開始
    def frame_start(self):
        self.frame_count += 1
        self.time_start = time.time() - self.time_prev
        return

    #フレーム計測終了
    def frame_end(self):
        if self.time_start >= FPS_INTERVAL:
            self.fps = self.frame_count / self.time_start
            self.frame_count = 0
            self.time_prev = time.time()
        return

    #更新
    def update(self):
        self.frame_start()
        self.update_scene()
        self.frame_end()
        return

    #更新(実処理)
    def update_scene(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        return

    #描画
    def draw(self):
        pyxel.cls(0)
        pyxel.text(0, 0, str(self.fps)[:5], 7)
        return
App()
