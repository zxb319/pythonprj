import math


class Graph:
    def __init__(self, edges: list, is_undirected=False):
        self._neighbours = {}
        for e in edges:
            if e[0] not in self._neighbours:
                self._neighbours[e[0]] = {}
            self._neighbours[e[0]][e[1]] = 1 if len(e) == 2 else e[2]

        if is_undirected:
            for e in edges:
                if e[1] not in self._neighbours:
                    self._neighbours[e[1]] = {}
                self._neighbours[e[1]][e[0]] = 1 if len(e) == 2 else e[2]

    def shortest_path(self, start, target):
        cache={start}
        neighbours = {k: v for k, v in self._neighbours[start].items()}
        previous_node = {k: start for k in neighbours}
        cur = min(neighbours.items(), key=lambda x: x[1])
        del neighbours[cur[0]]
        while cur[0] != target:
            cache.add(cur[0])
            cur_neighbours = self._neighbours[cur[0]]
            for cn, v in cur_neighbours.items():
                if cn in cache:
                    continue
                new_dist = cur[1] + v
                old_dist = neighbours.get(cn, math.inf)
                if new_dist < old_dist:
                    neighbours[cn] = new_dist
                    previous_node[cn] = cur[0]

            cur = min(neighbours.items(), key=lambda x: x[1])
            del neighbours[cur[0]]

        path = [cur[0]]
        min_dist = cur[1]
        c = cur[0]
        while c in previous_node:
            path.append(previous_node[c])
            c = previous_node[c]

        return min_dist, list(reversed(path))


def get_subway_info(file_path):
    edges = []
    station_line_map = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        line=f.readline()
        while line:
            r = [x for x in line.split() if x]
            for i in range(1, len(r) - 1):
                edges.append((r[i], r[i + 1]))

            for i in range(1, len(r)):
                if r[i] not in station_line_map:
                    station_line_map[r[i]] = set()
                station_line_map[r[i]].add(r[0])

            line=f.readline()

    return edges, station_line_map


if __name__ == '__main__':
    edges, station_line_map = get_subway_info('subway_info')
    g = Graph(edges, True)

    # for e,v in g._neighbours.items():
    #     print(e,v)

    min_dist, path = g.shortest_path('金运路', '封浜')

    for x in path:
        print(x,station_line_map[x])
    print(min_dist)
