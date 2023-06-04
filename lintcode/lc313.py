import time

import pyautogui
pyautogui.FAILSAFE=False
time.sleep(5)
pyautogui.typewrite('0123456789',interval=1)