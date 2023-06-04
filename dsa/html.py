class Html:
    def __init__(self, title='标题', *parts):
        self.title = title
        self.parts = list(parts)

    def append(self, part):
        self.parts.append(part)

    def __str__(self):
        body = '\n'.join(str(p) for p in self.parts)
        res = rf'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{self.title}</title>
            </head>
            <body>
            {body}
            </body>
            </html>
        '''

        return res


class Table:
    def __init__(self, head=None, *rows):
        self.head = head
        self.rows = list(rows)

    def set_head(self, row):
        self.head = row

    def append(self, row):
        self.rows.append(row)

    def __str__(self):
        body = '\n'.join(str(r) for r in self.rows)
        res = rf'''
            <table border="1">
            {self.head if self.head else ''}
            {body}
            </table>
        '''
        return res


class Row:
    def __init__(self, *cols):
        self.cols = []
        for c in cols:
            if isinstance(c, Col):
                self.cols.append(c)
            else:
                self.cols.append(Col(c))

    def append(self, col):
        if isinstance(col, Col):
            self.cols.append(col)
        else:
            self.cols.append(Col(col))

    def __str__(self):
        body = ''.join(str(c) for c in self.cols)
        res = rf'''
        <tr>{body}</tr>
        '''

        return res


class HeadRow(Row):
    def __init__(self, *cols):
        super().__init__(*cols)
        self.cols = []
        for c in cols:
            if isinstance(c, Col):
                self.cols.append(c)
            else:
                self.cols.append(HeadCol(c))

    def append(self, col):
        if isinstance(col, Col):
            self.cols.append(col)
        else:
            self.cols.append(HeadCol(col))


class Col:
    def __init__(self, part):
        self.part = part

    def __str__(self):
        f = 'td'
        return rf'<{f} style="text-align:center;">{str(self.part)}</{f}>'


class HeadCol(Col):
    def __str__(self):
        f = 'th'
        return rf'<{f} style="text-align:center;">{str(self.part)}</{f}>'


class Href:
    def __init__(self, text, ref):
        self.text = text
        self.ref = ref

    def __str__(self):
        return rf'<a href="{self.ref}">{self.text}</a>'


class Form:
    def __init__(self, action, method, *parts):
        self.action = action
        self.method = method
        self.part = list(parts)

    def append(self, part):
        self.part.append(part)

    def __str__(self):
        body = '\n'.join(str(p) for p in self.part)

        res = rf'''
            <form action="{self.action}" method="{self.method}">
                {body}
            </form>
        '''

        return res


class FormText:
    def __init__(self, name, value=''):
        self.name = name
        self.value = value

    def __str__(self):
        return rf'''
            <input type="text" name="{self.name}" value="{self.value}">
        '''


class FormSubmit:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return rf'''
            <input type="submit" value="{self.value}">
        '''


class Br:
    def __str__(self):
        return '<br>'


class Label:
    def __init__(self,text):
        self.text=text

    def __str__(self):
        return rf'<label>{self.text}</label>'