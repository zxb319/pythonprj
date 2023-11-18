import re
import os


def bigger(num):
    # if num >= 50:
    #     return num * 5
    # new_num = num * 5
    #
    # if new_num <= 100:
    #     return new_num
    # else:
    #     return 100

    return num


def keep(num):
    return num


def smaller(num):
    new_num = 1
    return new_num


def modify(line, current, comment, change_func):
    if comment:
        original = re.search(r'original is ([0-9]+)$', comment).group(1)
    else:
        original = current

    new = change_func(int(original))

    ret = re.sub(rf'=\s*{current}\s*;', rf'= {new};', line, re.IGNORECASE)
    if comment:
        return ret
    return ret + rf' // original is {original}'


def modify_create_count(file_path):
    file_name = os.path.basename(file_path)
    if re.search(r'rawmaterial(wood|stone|iron|coal|herb|onion|blueberry|mushroom|root)', file_name, re.IGNORECASE):
        change_func = bigger
    else:
        change_func = bigger

    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            reg = r'\s*int\s*_lowCreateCount\s*=\s*([0-9]+)\s*;\s*(//.+)?$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                line = modify(line, mat.group(1), mat.group(2), change_func)

            reg = r'\s*int\s*_highCreateCount\s*=\s*([0-9]+)\s*;\s*(//.+)?$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                line = modify(line, mat.group(1), mat.group(2), change_func)

            reg = r'\s*int\s*_weight\s*=\s*([0-9]+)\s*;\s*(//.+)?$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                line = modify(line, mat.group(1), mat.group(2), smaller)

            lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(rf'{os.path.basename(file_path)} success!')


def modify_raw_materials_create_counts(folder_path):
    for fn in os.listdir(folder_path):
        file_path = os.path.join(folder_path, fn)
        if fn.lower().startswith('rawmaterial'):
            modify_create_count(file_path)


if __name__ == '__main__':
    # file_path=rf"D:\download\BanishedKit_1.0.7.170910\resource\Template\RawMaterialAle.rsc"
    # modify_create_count(file_path)
    folder_path = os.path.realpath(r'D:\download\BanishedKit_1.0.7.170910\resource\Template')
    modify_raw_materials_create_counts(folder_path)
