import json
import math
import os.path

import androidhelper

import time

from math import radians

cur_dir = os.path.dirname(os.path.relpath(__file__))
base_loc_file_path = os.path.join(cur_dir, 'base_loc.txt')


def now_str():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def distance(loc1, loc2):
    lat1 = (90 - loc1['latitude']) * math.pi / 180
    lon1 = loc1['longitude'] * math.pi / 180

    lat2 = (90 - loc2['latitude']) * math.pi / 180
    lon2 = loc2['longitude'] * math.pi / 180

    c = math.sin(lat1) * math.sin(lat2) * math.cos(lon1 - lon2) + math.cos(lat1) * math.cos(lat2)
    return 6371004 * math.acos(c)


droid = androidhelper.Android()

droid.startSensingTimed(1, 250)

droid.startLocating()


def monitor_location(base_loc):
    threshold_distance = 50
    last_loc = None
    last_state = None
    while True:
        time.sleep(1)
        loc = droid.readLocation().result
        if loc.get('gps'):
            loc = loc['gps']
        elif loc.get('network'):
            loc = loc['network']
        else:
            continue

        if last_loc != loc:
            d = round(distance(base_loc, loc))
            print(rf'{now_str()}距离原点：{d}米，即{d // 1000}千米')
            if d < threshold_distance:
                state = 1
            else:
                state = 2

            if last_state and last_state != state:
                if last_state == 1 and state == 2:
                    msg = '你正在远离原点'
                else:
                    msg = '你正在接近原点'
                print(msg)
                droid.ttsSpeak(msg)
                droid.makeToast(msg)
                droid.vibrate(5000)

            last_state = state

        last_loc = loc


def save_base_loc():
    while True:
        time.sleep(1)
        loc = droid.readLocation().result
        if loc.get('gps'):
            loc = loc['gps']
            with open(base_loc_file_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(loc))
            print('原点设置成功！')
            return


def main():
    while True:
        opt = None
        while opt not in ('1', '2'):
            opt = input('设置原点打1，监控位置打2：')

        if opt == '1':
            save_base_loc()
        else:
            if not os.path.exists(base_loc_file_path):
                print('没有设置原点，请先设置原点！')
                continue
            with open(base_loc_file_path, 'r', encoding='utf-8') as f:
                base_loc = json.loads(f.read())
            monitor_location(base_loc)


main()

droid.stopLocating()
droid.stopSensing()