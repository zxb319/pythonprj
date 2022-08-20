import math


class Graph:
    def __init__(self, edges: list, nodes=None, is_undirected=False):
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

        if nodes:
            self._nodes = set(nodes)
        else:
            self._nodes = set()

        for e in edges:
            self._nodes.add(e[0])
            self._nodes.add(e[1])

    def shortest_path(self, start, target):
        cache = {start}
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

    def topological_sort(self):
        in_degrees = {}
        for k, v in self._neighbours.items():
            for n in v:
                if n not in in_degrees:
                    in_degrees[n] = set()
                in_degrees[n].add(k)

        res = []
        nodes = set(n for n in self._nodes)
        changed = True
        while changed and len(nodes) > 0:
            changed = False
            cur = []
            for n in nodes:
                if n not in in_degrees:
                    changed = True
                    res.append(n)
                    cc = []
                    for k, v in in_degrees.items():
                        if n in v:
                            v.remove(n)
                            if len(v) == 0:
                                cc.append(k)

                    for nn in cc:
                        del in_degrees[nn]

                    cur.append(n)

            for n in cur:
                nodes.remove(n)

        return res if len(res) == len(self._nodes) else []


if __name__ == '__main__':
    edges = [
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 3),

    ]
    g = Graph(edges)
    res = g.topological_sort()
    print(res)
