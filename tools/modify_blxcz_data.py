import re
import os


def bigger(mul):
    def inner(num):
        new_num = num * mul
        return new_num

    return inner


def keep(num):
    return num


def smaller(num):
    new_num = 1
    return new_num


def modify(line, current, comment, change_func):
    if comment:
        original = re.search(r'^<!--original is ([0-9]+)-->$', comment).group(1)
    else:
        original = current

    new = change_func(int(original))

    ret = re.sub(rf'>{current}<', rf'>{new}<', line, re.IGNORECASE)
    # if comment:
    #     return ret
    # return ret + rf' <!--original is {original}-->'
    return ret


def modify_capacity(file_path):
    lines = []
    modified_count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            reg = r'^\s*<CellStorageLimit>([0-9]+)</CellStorageLimit>\s*(<!--.+-->)?\s*$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                line = modify(line, mat.group(1), mat.group(2), bigger(1000))
                modified_count += 1

            lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(rf'{os.path.basename(file_path)} success, 修改了{modified_count}处')


def modify_building_product_count(file_path):
    lines = []
    modified_count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            reg = r'^\s*<UnEducated>([0-9]+)</UnEducated>\s*(<!--.+-->)?\s*$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                line = modify(line, mat.group(1), mat.group(2), bigger(100))
                modified_count += 1

            reg = r'^\s*<Educated>([0-9]+)</Educated>\s*(<!--.+-->)?\s*$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                line = modify(line, mat.group(1), mat.group(2), bigger(100))
                modified_count += 1

            lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(rf'{os.path.basename(file_path)} success, 修改了{modified_count}处')


def modify_animal_product_count(file_path):
    lines = []
    modified_count = 0
    in_produce = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]

            if in_produce not in (0, 1):
                raise Exception(rf'product标签有嵌套！')

            reg = r'^\s*<Produce>\s*(<!--.+-->)?\s*$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                in_produce += 1

            if in_produce == 1:
                reg = r'^\s*<Lower>([0-9]+)</Lower>\s*(<!--.+-->)?\s*$'
                mat = re.search(reg, line, re.IGNORECASE)
                if mat:
                    line = modify(line, mat.group(1), mat.group(2), bigger(100))
                    modified_count += 1

                reg = r'^\s*<Upper>([0-9]+)</Upper>\s*(<!--.+-->)?\s*$'
                mat = re.search(reg, line, re.IGNORECASE)
                if mat:
                    line = modify(line, mat.group(1), mat.group(2), bigger(100))
                    modified_count += 1

            reg = r'^\s*</Produce>\s*(<!--.+-->)?\s*$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                in_produce -= 1

            lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(rf'{os.path.basename(file_path)} success, 修改了{modified_count}处')


def modify_resource_product_count(file_path):
    lines = []
    modified_count = 0
    in_produce = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]

            if in_produce not in (0, 1):
                raise Exception(rf'product标签有嵌套！')

            reg = r'^\s*<FinishRes>\s*(<!--.+-->)?\s*$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                in_produce += 1

            if in_produce == 1:
                reg = r'^\s*<Lower>([0-9]+)</Lower>\s*(<!--.+-->)?\s*$'
                mat = re.search(reg, line, re.IGNORECASE)
                if mat:
                    line = modify(line, mat.group(1), mat.group(2), bigger(100))
                    modified_count += 1

                reg = r'^\s*<Upper>([0-9]+)</Upper>\s*(<!--.+-->)?\s*$'
                mat = re.search(reg, line, re.IGNORECASE)
                if mat:
                    line = modify(line, mat.group(1), mat.group(2), bigger(100))
                    modified_count += 1

            reg = r'^\s*</FinishRes>\s*(<!--.+-->)?\s*$'
            mat = re.search(reg, line, re.IGNORECASE)
            if mat:
                in_produce -= 1

            lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(rf'{os.path.basename(file_path)} success, 修改了{modified_count}处')


if __name__ == '__main__':
    file_path = os.path.realpath(
        r"D:\Program Files (x86)\Steam\steamapps\common\Settlement Survival\Settlement Survival_Data\StreamingAssets\zipConfig\Building.xml")
    modify_capacity(file_path)
    modify_building_product_count(file_path)

    file_path = os.path.realpath(
        r"D:\Program Files (x86)\Steam\steamapps\common\Settlement Survival\Settlement Survival_Data\StreamingAssets\zipConfig\Animal.xml")
    modify_animal_product_count(file_path)

    file_path = os.path.realpath(
        r"D:\Program Files (x86)\Steam\steamapps\common\Settlement Survival\Settlement Survival_Data\StreamingAssets\zipConfig\ResAttribute.xml")
    modify_resource_product_count(file_path)
