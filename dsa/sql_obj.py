class Table:
    __tablename__ = ''


    def __init__(self, **kwargs):
        self.kwargs = kwargs


class Column:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return (self, '=', other)

    def in_(self, items):
        return (self, 'in', items)

    def __str__(self):
        return self.name


class Test1(Table):
    __tablename__ = 'test1'
    id = Column(name='id')
    name = Column(name='name')


class Sql:
    def __init__(self):
        self.cols = []
        self.table = None
        self.joins = []
        self.wheres = []

    def select(self, *cols):
        self.cols = cols
        return self

    def from_(self, table):
        self.table = table.__tablename__
        return self

    def where(self, cond):
        self.wheres.append(cond)
        return self

    def __str__(self):
        return rf'''
            select {','.join(str(x) for x in self.cols)}
            from {self.table}
            where {' and '.join(rf"{x[0]} {x[1]} '{x[2]}'" for x in self.wheres)}
        '''


if __name__ == '__main__':
    sql = Sql().select(Test1.name, Test1.id).from_(Test1).where(Test1.name.in_('zxb') )
    print(str(sql))
