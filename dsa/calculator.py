class Token:
    TYPE_NUM=0
    TYPE_ADD=1
    TYPE_SUB=2
    TYPE_MUL=3
    TYPE_DIV=4
    TYPE_LEFT_PAR=5
    TYPE_RIGHT_PAR=6
    TYPE_EOF=7
    TYPE_POW=8

    def __init__(self,type,val):
        self.type=type
        self.val=val

    def __str__(self):
        return f'Token({self.type},{self.val})'

    def __repr__(self):
        return str(self)

class _TokenState:
    START = 0
    NUM_INT = 1
    NUM_INT_POINT = 2
    NUM_INT_POINT_INT = 3
    NUM_INT_POINT_INT_E = 4
    NUM_INT_POINT_INT_E_SIGN = 5
    NUM_INT_POINT_INT_E_SIGN_INT = 6
    NUM_POINT = 7
    OP_ADD=81
    OP_SUB=82
    OP_DIV=83
    OP_LEFT_PAR=84
    OP_RIGHT_PAR=85
    OP_MUL = 9
    OP_POW = 10

    ACCEPTABLE_STATES = {
        NUM_INT:Token.TYPE_NUM,
        NUM_INT_POINT:Token.TYPE_NUM,
        NUM_INT_POINT_INT:Token.TYPE_NUM,
        NUM_INT_POINT_INT_E_SIGN_INT:Token.TYPE_NUM,
        OP_ADD:Token.TYPE_ADD,
        OP_SUB:Token.TYPE_SUB,
        OP_DIV:Token.TYPE_DIV,
        OP_LEFT_PAR:Token.TYPE_LEFT_PAR,
        OP_RIGHT_PAR:Token.TYPE_RIGHT_PAR,
        OP_MUL:Token.TYPE_MUL,
        OP_POW:Token.TYPE_POW
    }

    @staticmethod
    def char_type(c: str):
        if '0' <= c <= '9':
            return 'D'
        elif c.isspace():
            return ' '
        elif c == 'e':
            return 'E'
        else:
            return c

    TRANSFER_MAP = {
        START: {
            ' ': START,
            'D': NUM_INT,
            '.': NUM_POINT,
            '+': OP_ADD,
            '-': OP_SUB,
            '/': OP_DIV,
            '(': OP_LEFT_PAR,
            ')': OP_RIGHT_PAR,
            '*': OP_MUL,
        },

        NUM_INT: {
            'D': NUM_INT,
            '.': NUM_INT_POINT,
            'E': NUM_INT_POINT_INT_E
        },

        NUM_INT_POINT: {
            'D': NUM_INT_POINT_INT,
            'E': NUM_INT_POINT_INT_E,
        },

        NUM_INT_POINT_INT: {
            'D': NUM_INT_POINT_INT,
            'E': NUM_INT_POINT_INT_E,
        },

        NUM_INT_POINT_INT_E: {
            '+': NUM_INT_POINT_INT_E_SIGN,
            '-': NUM_INT_POINT_INT_E_SIGN,
            'D': NUM_INT_POINT_INT_E_SIGN_INT,
        },

        NUM_INT_POINT_INT_E_SIGN: {
            'D': NUM_INT_POINT_INT_E_SIGN_INT
        },

        NUM_INT_POINT_INT_E_SIGN_INT: {
            'D': NUM_INT_POINT_INT_E_SIGN_INT
        },

        NUM_POINT: {
            'D': NUM_INT_POINT_INT
        },

        OP_MUL: {
            '*': OP_POW
        },

    }


class Expr:
    _op_func={
        Token.TYPE_ADD:lambda a,b:a+b,
        Token.TYPE_SUB:lambda a,b:a-b,
    }
    def __init__(self,*args):
        self._args=args

    @property
    def val(self):
        if len(self._args)==1:
            return self._args[0].val
        else:
            return Expr._op_func[self._args[1].type](self._args[0].val,self._args[2].val)

class Term:
    _op_func={
        Token.TYPE_MUL:lambda a,b:a*b,
        Token.TYPE_DIV:lambda a,b:a/b
    }

    def __init__(self,*args):
        self._args=args

    @property
    def val(self):
        if len(self._args)==1:
            return self._args[0].val
        else:
            return Term._op_func[self._args[1].type](self._args[0].val,self._args[2].val)

class Factor:
    _op_func={
        Token.TYPE_ADD:lambda a:a,
        Token.TYPE_SUB:lambda a:-a
    }
    def __init__(self,*args):
        self._args=args

    @property
    def val(self):
        if len(self._args)==1:
            return float(self._args[0].val)
        elif len(self._args)==2:
            return Factor._op_func[self._args[0].type](self._args[1].val)
        else:
            return self._args[1].val


class Calculator:
    def __init__(self):
        self._exp_str = ''
        self._cur_pos = 0

    def _get_next_token(self):
        res = []
        state = _TokenState.START
        for i in range(self._cur_pos, len(self._exp_str)):
            cur_char = self._exp_str[i]
            char_type = _TokenState.char_type(cur_char)
            if state not in _TokenState.TRANSFER_MAP or char_type not in _TokenState.TRANSFER_MAP[state]:
                if state in _TokenState.ACCEPTABLE_STATES:
                    self._cur_pos = i
                    return Token(_TokenState.ACCEPTABLE_STATES[state],''.join(res))
                else:
                    raise Exception('not valid expression!')

            state = _TokenState.TRANSFER_MAP[state][char_type]
            if char_type != ' ':
                res.append(cur_char)

        if len(res) > 0:
            if state in _TokenState.ACCEPTABLE_STATES:
                self._cur_pos = len(self._exp_str)
                return Token(_TokenState.ACCEPTABLE_STATES[state],''.join(res))
            else:
                raise Exception('not valid expression!')
        else:
            return Token(Token.TYPE_EOF,''.join(res))

    def calculator(self, exp: str):
        self._exp_str = exp
        self._cur_pos = 0
        token = self._get_next_token()
        stack=[]
        while True:
            print(stack)
            if len(stack)==1 and type(stack[-1])==Expr and token.type==Token.TYPE_EOF:
                return stack[-1].val

            if len(stack)>=3 and type(stack[-3])==Token and stack[-3].type==Token.TYPE_LEFT_PAR and type(stack[-2])==Expr and type(stack[-1])==Token and stack[-1].type==Token.TYPE_RIGHT_PAR:
                right_par=stack.pop()
                expr=stack.pop()
                left_par=stack.pop()
                stack.append(Factor(left_par,expr,right_par))
            elif len(stack)>=3 and type(stack[-3])==Term and type(stack[-2])==Token and stack[-2].type in(Token.TYPE_MUL,Token.TYPE_DIV) and type(stack[-1])==Factor \
                    and token.type in(Token.TYPE_ADD,Token.TYPE_SUB,Token.TYPE_MUL,Token.TYPE_DIV,Token.TYPE_EOF,Token.TYPE_RIGHT_PAR):
                factor=stack.pop()
                op=stack.pop()
                term=stack.pop()
                stack.append(Term(term,op,factor))
            elif len(stack)>=3 and type(stack[-3])==Expr and type(stack[-2])==Token and stack[-2].type in(Token.TYPE_ADD,Token.TYPE_SUB) and type(stack[-1])==Term \
                    and token.type in(Token.TYPE_ADD,Token.TYPE_SUB,Token.TYPE_EOF,Token.TYPE_RIGHT_PAR):
                term=stack.pop()
                op=stack.pop()
                expr=stack.pop()
                stack.append(Expr(expr,op,term))

            elif len(stack)>=2 and type(stack[-2])==Token and stack[-2].type in (Token.TYPE_ADD,Token.TYPE_SUB) and type(stack[-1])==Factor:
                factor=stack.pop()
                op=stack.pop()
                stack.append(Factor(op,factor))
            elif len(stack)>=1 and type(stack[-1])==Token and stack[-1].type==Token.TYPE_NUM:
                num=stack.pop()
                stack.append(Factor(num))


            elif len(stack)>=1 and type(stack[-1])==Factor and token.type in(Token.TYPE_ADD,Token.TYPE_SUB,Token.TYPE_MUL,Token.TYPE_DIV,Token.TYPE_EOF,Token.TYPE_RIGHT_PAR):
                factor=stack.pop()
                stack.append(Term(factor))


            elif len(stack)>=1 and type(stack[-1])==Term and token.type in (Token.TYPE_ADD,Token.TYPE_SUB,Token.TYPE_EOF,Token.TYPE_RIGHT_PAR):
                term=stack.pop()
                stack.append(Expr(term))

            else:
                if token.type!=Token.TYPE_EOF:
                    stack.append(token)
                    token = self._get_next_token()


if __name__ == '__main__':
    exp = '1-2*3'
    c = Calculator()
    v=c.calculator(exp)
    print(v)