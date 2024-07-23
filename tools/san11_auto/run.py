import os.path
import time

import pyautogui as pag


def find_icon(icon_fp):
    return pag.locateOnScreen(icon_fp, confidence=0.9)


def try_find(icon_fp, times=1, interval=0.5):
    tryed = 0
    while tryed < times:
        print(rf'开始识别{icon_fp}')
        loc = find_icon(icon_fp)
        time.sleep(interval)
        if loc:
            return loc
        else:
            tryed += 1


def try_find_and_click(icon_fp, times=10, interval=0.5):
    tryed = 0
    while tryed < times:
        print(rf'开始识别{icon_fp}')
        loc = find_icon(icon_fp)
        time.sleep(interval)
        if loc:
            pag.moveTo(loc, duration=interval)
            pag.click()
            pag.move(100,-100, duration=interval)
            return
        else:
            tryed += 1
    raise Exception(rf'cannot find {icon_fp}')


if __name__ == '__main__':
    icon_dir = os.path.dirname(os.path.relpath(__file__))
    time.sleep(5)
    while True:

        while not try_find(os.path.join(icon_dir, 'icons', 'yes_btn.png')):
            try_find_and_click(os.path.join(icon_dir, 'icons', 'next_btn.png'))

        try_find_and_click(os.path.join(icon_dir, 'icons', 'yes_btn.png'))
