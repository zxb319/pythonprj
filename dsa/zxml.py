import enum
import re
from typing import List


def indent(s: str, indent_count=1, space_count_per_indent=4):
    rows = s.split('\n')
    rows = [rf'{" " * space_count_per_indent * indent_count}{r}' for r in rows]
    return '\n'.join(rows)


class Element:
    """
    名称 属性值
    """

    def __init__(self, tag, **attrs):
        self.tag = tag
        self.attrs = attrs
        self.children = []

    def set_attr(self, name, value):
        self.attrs[name] = value

    def append(self, child: 'Element'):
        self.children.append(child)
        return self

    def extend(self, children: List):
        for c in children:
            self.children.append(c)
        return self

    def set_text(self, text: str):
        self.children = text

    def __str__(self):
        attr_str = ' '.join(rf'{k}="{v}"' for k, v in self.attrs.items()) if self.attrs else ''
        children_str = '\n'.join(str(c) for c in self.children) if self.children else ''
        if len(self.children) == 1 and isinstance(self.children[0], str):
            if attr_str:
                return rf'''
<{self.tag} {attr_str}>{children_str}</{self.tag}>
                '''.strip()
            else:
                return rf'''
<{self.tag}>{children_str}</{self.tag}>
                                '''.strip()
        elif not attr_str and not children_str:
            return rf'''
<{self.tag}/>
'''.strip()
        elif not children_str:
            return rf'''
<{self.tag} {attr_str}/>
'''.strip()
        elif not attr_str:
            return rf'''
<{self.tag}>
{indent(children_str)}
</{self.tag}>
'''.strip()
        else:
            return rf'''
<{self.tag} {attr_str}>
{indent(children_str)}
</{self.tag}>
'''.strip()


class Xml:
    def __init__(self, root: Element, encoding='utf-8', version='1.0', **attributes):
        self.root = root
        self.attributes = {'encoding': encoding, 'version': version}
        self.attributes.update(attributes)

    def __str__(self):
        attrs_str = ' '.join(rf'{k}="{v}"' for k, v in self.attributes.items())
        if attrs_str:
            attrs_str = ' ' + attrs_str

        return rf'''
<?xml{attrs_str}?>
{self.root}
'''.strip()

    @classmethod
    def parse(cls, xml_str: str):
        return Parser(xml_str).parse()


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return rf'[{self.type} `{self.value}`]'

    class Type(enum.Enum):
        IDN = 1
        STR = 2
        LT = 3
        GT = 4
        COMMENT = 5
        ASSIGN = 6
        QUESTION = 7
        XML = 8
        WHITE = 9
        SLASH = 10
        TEXT = 11

    REGs = [
        (Type.COMMENT, re.compile(r'<!--((?!(<!--|-->)).)*-->', re.IGNORECASE | re.S)),
        (Type.IDN, re.compile(r'[a-z_][a-z_\d:.\-]*', re.IGNORECASE | re.S)),
        (Type.STR, re.compile(r'"[^"]*"', re.IGNORECASE | re.S)),
        (Type.LT, re.compile(r'<', re.IGNORECASE | re.S)),
        (Type.GT, re.compile(r'>', re.IGNORECASE | re.S)),
        (Type.ASSIGN, re.compile(r'=', re.IGNORECASE | re.S)),
        (Type.QUESTION, re.compile(r'\?', re.IGNORECASE | re.S)),
        (Type.SLASH, re.compile(r'/', re.IGNORECASE | re.S)),
        (Type.WHITE, re.compile(r'\s+', re.IGNORECASE | re.S)),
        (Type.TEXT, re.compile(r'[^<]+', re.IGNORECASE | re.S)),
    ]

    KEYs = {
        'xml': Type.XML,
    }

    @classmethod
    def get_tokens(cls, s: str):
        s = s.strip()
        pos = 0
        ret = []
        last_type = None
        while pos < len(s):
            found = False
            if last_type == Token.Type.GT:
                mat = Token.REGs[-1][-1].match(s, pos)
                if mat:
                    found = True
                    val = mat.group(0)
                    if sval := val.strip():
                        ret.append(Token(Token.Type.TEXT, sval))
                        last_type = t
                    pos += len(val)
                    continue
            for t, r in Token.REGs:
                mat = r.match(s, pos)
                if mat:
                    found = True
                    val = mat.group(0)
                    if t != Token.Type.WHITE and t != Token.Type.COMMENT:
                        if t == Token.Type.IDN and val in Token.KEYs:
                            ret.append(Token(Token.KEYs[val], val))
                        else:
                            ret.append(Token(t, val))
                        last_type = t
                    pos += len(val)
                    break
            if not found:
                raise Exception(rf'不可识别的Token:{s[pos:pos + 30]}')

        return ret


class Parser:
    def __init__(self, xml_str: str):
        self.tokens = Token.get_tokens(xml_str)
        # print(*self.tokens,sep='\n')
        self.pos = 0

    def assert_not_end(self):
        if self.pos >= len(self.tokens):
            raise Exception(rf'tokens end!')

    def has_next_token(self):
        return self.pos < len(self.tokens)

    def get_next_token(self, token_type: Token.Type = None):
        self.assert_not_end()
        cur = self.tokens[self.pos]
        if token_type and cur.type != token_type:
            raise Exception(rf'expect {token_type}!')
        self.pos += 1
        return cur

    def peek_next_token(self, count=0):
        self.pos += count
        self.assert_not_end()
        self.pos -= count
        return self.tokens[self.pos + count]

    def get_declaration(self,tag_token_type:Token.Type):
        self.get_next_token(Token.Type.LT)
        self.get_next_token(Token.Type.QUESTION)
        self.get_next_token(tag_token_type)

        attrs = {}
        cur_token = self.peek_next_token()
        while cur_token.type != Token.Type.QUESTION:
            key = self.get_next_token(Token.Type.IDN).value
            self.get_next_token(Token.Type.ASSIGN)
            value = self.get_next_token(Token.Type.STR).value[1:-1]
            attrs[key] = value

            cur_token = self.peek_next_token()

        self.get_next_token(Token.Type.QUESTION)
        self.get_next_token(Token.Type.GT)
        return attrs

    def get_element(self):
        self.get_next_token(Token.Type.LT)
        tag = self.get_next_token(Token.Type.IDN).value
        cur_token = self.peek_next_token()

        attrs = {}
        while cur_token.type not in (Token.Type.SLASH, Token.Type.GT):
            key = self.get_next_token(Token.Type.IDN).value
            self.get_next_token(Token.Type.ASSIGN)
            value = self.get_next_token(Token.Type.STR).value[1:-1]
            attrs[key] = value

            cur_token = self.peek_next_token()

        if cur_token.type == Token.Type.SLASH:
            self.get_next_token(Token.Type.SLASH)
            self.get_next_token(Token.Type.GT)
            return Element(tag, **attrs)

        self.get_next_token(Token.Type.GT)
        children = []
        cur_token = self.peek_next_token()
        next_token = self.peek_next_token(1)
        next2_token = self.peek_next_token(2)
        while not (next_token.type == Token.Type.SLASH and next2_token.type == Token.Type.IDN and next2_token.value == tag):
            if cur_token.type == Token.Type.TEXT:
                children.append(self.get_next_token(Token.Type.TEXT).value)
            elif cur_token.type == Token.Type.LT:
                children.append(self.get_element())
            else:
                raise Exception(rf'expect text or LT!')

            cur_token = self.peek_next_token()
            next_token = self.peek_next_token(1)
            next2_token = self.peek_next_token(2)

        self.get_next_token(Token.Type.LT)
        self.get_next_token(Token.Type.SLASH)
        self.get_next_token(Token.Type.IDN)
        self.get_next_token(Token.Type.GT)
        return Element(tag, **attrs).extend(children)

    def parse(self):
        self.get_next_token(Token.Type.LT)
        cur_token = self.peek_next_token()
        declarations = {}
        self.pos -= 1
        if cur_token.type == Token.Type.QUESTION:
            declarations = self.get_declaration(Token.Type.XML)
        root_element = self.get_element()

        if self.pos < len(self.tokens):
            raise Exception(rf'too many content!')
        return Xml(root_element, **declarations)


if __name__ == '__main__':
    s = '''
    
    

    '''

    print(Xml.parse(s))
