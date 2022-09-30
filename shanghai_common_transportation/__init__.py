def get_subway_info(file_path):
    edges = []
    station_line_map = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            r = [x for x in line.split() if x]
            for i in range(1, len(r) - 1):
                edges.append((r[i], r[i + 1]))

            for i in range(1, len(r)):
                if r[i] not in station_line_map:
                    station_line_map[r[i]] = set()
                station_line_map[r[i]].add(r[0])

            line = f.readline()

    return edges, station_line_map


def add_line_info_for_path(path, station_line_map):
    lines = [station_line_map[path[0]]]

    for i in range(1, len(path)):
        s = path[i]
        ls = station_line_map[s].intersection(station_line_map[path[i - 1]])
        lines.append(ls)

    lines[0] = lines[0].intersection(station_line_map[path[1]])
    return list(zip(path, lines))


if __name__ == '__main__':
    edges, station_line_map = get_subway_info('subway_info')
    from dsa.graph import Graph

    g = Graph(edges, is_undirected=True)

    # for e,v in g._neighbours.items():
    #     print(e,v)

    min_dist, path = g.shortest_path('金运路', '浦电路')

    res = add_line_info_for_path(path, station_line_map)
    for r in res:
        print(*r)
    print(min_dist)
