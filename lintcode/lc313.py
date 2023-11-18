import os

folder_path=rf'D:\Program Files (x86)\Steam\steamapps\common\Settlement Survival\Settlement Survival_Data\StreamingAssets\zipConfig'

for f in os.listdir(folder_path):
    fp=os.path.join(folder_path,f)
    if os.path.isdir(fp):
        continue
    with open(fp,'r',encoding='utf-8') as ff:
        if '法令' in ff.read():
            print(f)