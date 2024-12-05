@echo off
pyxel package sandbox sandbox/sandbox_main.py
pyxel app2html package/sandbox.pyxapp
move sandbox.pyxapp package
move sandbox.html package
pause
