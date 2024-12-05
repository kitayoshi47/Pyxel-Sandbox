# title: Pyxel-Sandbox
# author: Kitayochi
# desc: sandbox
# site: https://github.com/kitayoshi47/Pyxel-Sandbox
# license: MIT
# version: 0.1

import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.text(46, 41, "Hello, Pyxel (^-^)", pyxel.frame_count % 16)
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)
App()
