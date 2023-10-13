import xml.etree.ElementTree as ElementTree


def get_sub_nodes(root: ElementTree.Element, tag: str):
    ret = []

    def search(r: ElementTree.Element, t: str):
        if r.tag == t:
            ret.append(r)
        for c in list(r):
            search(c, t)

    search(root, tag)
    return ret


def get_children_nodes(root: ElementTree.Element, tag: str):
    ret = []

    def search(r: ElementTree.Element, t: str):
        for c in list(r):
            if c.tag == tag:
                ret.append(c)

    search(root, tag)
    return ret


def update_sub_nodes(root: ElementTree.Element, node_tag: str, update_func):
    sub_nodes = get_sub_nodes(root, node_tag)
    for n in sub_nodes:
        update_func(n)


def update_children_nodes(node: ElementTree.Element, children_tag: str, update_func):
    children = get_children_nodes(node, children_tag)
    if children:
        for c in children:
            update_func(c)


def update_or_add_children(node: ElementTree.Element, child_tag: str, num_change_func, default_value):
    children = get_children_nodes(node, child_tag)
    if not children:
        new_node = ElementTree.Element(child_tag)
        new_node.text = str(default_value)
        node.append(new_node)
    else:
        for c in children:
            old_value = int(c.text.strip())
            new_value = num_change_func(old_value)
            c.text = str(new_value)


def modify_assets_file(ffp, tfp):
    with open(ffp, 'r', encoding='utf-8') as f:
        s = f.read()
    root = ElementTree.fromstring(s)
    assets = get_sub_nodes(root, 'Asset')

    # ret = []
    # for asset in assets:
    #     ret.extend(get_sub_nodes(asset, 'Name'))
    #
    # print(len(ret))
    # for r in ret:
    #     print(r.text)

    for a in assets:
        if get_sub_nodes(a, 'Product'):
            update_sub_nodes(a, 'WareProduction',
                             lambda node: update_or_add_children(node, 'ProductionCapacity', lambda x: x * 10, 50000))
            update_sub_nodes(a, 'WareProduction',
                             lambda node: update_or_add_children(node, 'ProductionCount', lambda x: x * 10, 10000))

            field_counts = get_sub_nodes(a, 'FarmfieldCount')
            for fc in field_counts:
                old_value = int(fc.text.strip())
                new_value = 1 if old_value >= 1 else old_value
                fc.text = str(new_value)

        names = get_sub_nodes(a, 'Name')
        name = names[0].text.strip() if names else None
        if name in ('Marketcart', 'MarketcartSouth',):
            update_sub_nodes(a, 'Transport',
                             lambda node: update_or_add_children(node, 'SlotCapacity', lambda x: x * 10, 50))

    with open(tfp, 'w', encoding='utf-8') as f:
        f.write(ElementTree.tostring(root).decode('utf-8'))


def modify_features_file(ffp, tfp):
    with open(ffp, 'r', encoding='utf-8') as f:
        s = f.read()
    root = ElementTree.fromstring(s)
    assets = get_sub_nodes(root, 'Asset')

    # ret = []
    # for asset in assets:
    #     ret.extend(get_sub_nodes(asset, 'Name'))
    #
    # print(len(ret))
    # for r in ret:
    #     print(r.text)

    for a in assets:
        value_nodes = get_sub_nodes(a, 'Value')
        for v in value_nodes:
            old_value = int(v.text.strip())
            new_value = old_value * 100
            if new_value <= -100:
                new_value = -99
            v.text = str(new_value)

        value_nodes = get_sub_nodes(a, 'ItemHonourPrice')
        for v in value_nodes:
            old_value = int(v.text.strip())
            new_value = 1 if old_value >= 1 else old_value
            v.text = str(new_value)

        value_nodes = get_sub_nodes(a, 'ItemQuality')
        for v in value_nodes:
            old_value = v.text.strip()
            new_value = 'C'
            v.text = new_value

    with open(tfp, 'w', encoding='utf-8') as f:
        f.write(ElementTree.tostring(root).decode('utf-8'))


if __name__ == '__main__':
    from_file_path = r'D:\download\3DMGAME_ANNO_1404.CHS.Green\ANNO 1404\maindata\assets - 副本.xml'
    to_file_path = r"D:\download\3DMGAME_ANNO_1404.CHS.Green\ANNO 1404\maindata\assets.xml"
    modify_assets_file(from_file_path, to_file_path)

    from_file_path = r'D:\download\3DMGAME_ANNO_1404.CHS.Green\ANNO 1404\maindata\features - 副本.xml'
    to_file_path = r'D:\download\3DMGAME_ANNO_1404.CHS.Green\ANNO 1404\maindata\features.xml'
    modify_features_file(from_file_path, to_file_path)
