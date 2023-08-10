from typing import Iterable, Dict, Any, Union


class PySQL:
    def __init__(self):
        self._records = []
        self._cols = set()
        self._computed_cols = dict()
        self._filters = []
        self._group_cols = []
        self._group_computed_cols = {}
        self._having_filters = []

    def select(self, *cols, **kwargs):
        self._cols = cols
        self._computed_cols = kwargs
        return self

    def from_(self, records: Iterable):
        self._records = list(records)
        return self

    def where(self, filter_func):
        self._filters.append(filter_func)
        return self

    def group_by(self, *cols, **kwargs):
        self._group_cols = cols
        self._group_computed_cols = kwargs
        return self

    def having(self, filter_func):
        self._having_filters.append(filter_func)
        return self

    def result(self):
        res = self._records
        if self._filters:
            res = (r for r in self._records if all(f(r) for f in self._filters))

        if self._group_cols or self._group_computed_cols:
            group_col_names = [c for c in self._group_cols]
            new_res = []
            group_data = {}
            for r in res:
                key = [r[c] for c in self._group_cols]
                for k, v in sorted(self._group_computed_cols.items()):
                    group_col_names.append(k)
                    if hasattr(v, '__call__'):
                        key.append(v(r))
                    else:
                        key.append(r[v])
                key = tuple(key)

                if key not in group_data:
                    group_data[key] = []
                group_data[key].append(r)
            for k, v in group_data.items():
                cur = {k: v for k, v in zip(group_col_names, k)}
                cur['-'] = v
                new_res.append(cur)

            res = new_res

            if self._having_filters:
                res = (r for r in res if all(f(r['-']) for f in self._having_filters))

        new_res = []
        for r in res:
            cur = {c: r[c] for c in self._cols}
            for k, v in self._computed_cols.items():
                if self._group_cols or self._group_computed_cols:
                    cur[k] = v(r['-']) if hasattr(v, '__call__') else r[v]
                else:
                    cur[k] = v(r) if hasattr(v, '__call__') else r[v]
            new_res.append(cur)

        return new_res


if __name__ == '__main__':
    ds = [
        {'name': 'aaa', 'age': 1},
        {'name': 'aaa', 'age': 2},
        {'name': 'bbb', 'age': 3},
        {'name': 'bbb', 'age': 4},
        {'name': 'ccc', 'age': 5},
        {'name': 'ccc', 'age': 6},
        {'name': 'ccc', 'age': 7},

    ]

    ret = PySQL().from_(ds).where(lambda x: x['name'] > 'aaa').group_by(name='name').select(
        age_sum=lambda r: sum(x['age'] for x in r), name='name', count=lambda r: len(r)
    ).result()
    print(ret)
    ret = PySQL().from_(ret).select(cnt=lambda x: x['count']).result()
    print(ret)
