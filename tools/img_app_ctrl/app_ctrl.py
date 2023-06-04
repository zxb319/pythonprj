import time

import pyautogui as gui


time.sleep(1)
p=gui.locateCenterOnScreen(r'weixinapp.png')
gui.leftClick(x=p.x,y=p.y)

p=gui.locateCenterOnScreen(r'wenjianzhushou.png')
gui.leftClick(x=p.x,y=p.y)

p=gui.locateCenterOnScreen(r'zhongwenshurufa.png')
if not p:
    gui.hotkey('shift')
gui.typewrite('zxb ',interval=0.3)
time.sleep(1)
gui.hotkey('enter')