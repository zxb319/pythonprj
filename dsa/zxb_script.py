import enum
import re
from typing import List


class Token:
    # @enum.unique
    class Type(enum.Enum):
        IDN = 1
        INT = 2
        FLOAT = 3
        STR = 4

        ADD = 5
        SUB = 6
        MUL = 7
        DIV = 8
        POW = 9
        MOD = 10
        FLOOR_DIV = 'floor_div'

        EQ = 11
        NE = 12
        LT = 13
        LE = 14
        GT = 15
        GE = 16

        NOT = 18
        AND = 19
        OR = 20

        LP = 21
        RP = 22
        LZ = 23
        RZ = 24
        LD = 25
        RD = 26

        WHITE = 27

        COMMA = 28
        COMMENT = 29

        ASSIGN = 34
        IF = 30
        ELIF = 31
        ELSE = 32
        WHILE = 33

        FUNC = 'func'

    TOKEN_TYPE_REGS = [
        (Type.IDN, re.compile(r'[a-z_][a-z\d_]*', re.IGNORECASE | re.S)),
        (Type.FLOAT, re.compile(r'(\d+\.\d*|\.\d+)(e[\+\-]?\d+)?', re.IGNORECASE | re.S)),
        (Type.INT, re.compile(r'\d+', re.IGNORECASE | re.S)),
        (Type.STR, re.compile(r'''\"(\\\"|[^\"])*\"''', re.IGNORECASE | re.S)),

        (Type.ADD, re.compile(r'\+', re.IGNORECASE | re.S)),
        (Type.SUB, re.compile(r'\-', re.IGNORECASE | re.S)),
        (Type.POW, re.compile(r'\*\*', re.IGNORECASE | re.S)),
        (Type.MUL, re.compile(r'\*', re.IGNORECASE | re.S)),
        (Type.FLOOR_DIV, re.compile(r'//', re.IGNORECASE | re.S)),
        (Type.DIV, re.compile(r'/', re.IGNORECASE | re.S)),
        (Type.MOD, re.compile(r'%', re.IGNORECASE | re.S)),

        (Type.EQ, re.compile(r'==', re.IGNORECASE | re.S)),
        (Type.ASSIGN, re.compile(r'=', re.IGNORECASE | re.S)),
        (Type.NE, re.compile(r'!=', re.IGNORECASE | re.S)),
        (Type.LE, re.compile(r'<=', re.IGNORECASE | re.S)),
        (Type.LT, re.compile(r'<', re.IGNORECASE | re.S)),
        (Type.GE, re.compile(r'>=', re.IGNORECASE | re.S)),
        (Type.GT, re.compile(r'>', re.IGNORECASE | re.S)),

        (Type.LP, re.compile(r'\(', re.IGNORECASE | re.S)),
        (Type.RP, re.compile(r'\)', re.IGNORECASE | re.S)),
        (Type.LZ, re.compile(r'\[', re.IGNORECASE | re.S)),
        (Type.RZ, re.compile(r'\]', re.IGNORECASE | re.S)),
        (Type.LD, re.compile(r'\{', re.IGNORECASE | re.S)),
        (Type.RD, re.compile(r'\}', re.IGNORECASE | re.S)),
        (Type.COMMA, re.compile(r',', re.IGNORECASE | re.S)),

        (Type.WHITE, re.compile(r'\s+', re.IGNORECASE | re.S)),
        (Type.COMMENT, re.compile(r'#[^\n]+', re.IGNORECASE | re.S)),

    ]

    KEYs = {
        'not': Type.NOT,
        'and': Type.AND,
        'or': Type.OR,
        'if': Type.IF,
        'elif': Type.ELIF,
        'else': Type.ELSE,
        'while': Type.WHILE,
        'func': Type.FUNC,
    }

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return rf'<{self.type}, `{self.value}`>'


def get_tokens(s: str):
    ret = []
    cp = 0
    while cp < len(s):
        found = False
        for t, r in Token.TOKEN_TYPE_REGS:
            match = r.match(s, cp)
            if match:
                found = True
                val = match.group(0)
                if t not in (Token.Type.WHITE, Token.Type.COMMENT):
                    if val in Token.KEYs:
                        ret.append(Token(Token.KEYs[val], val))
                    else:
                        ret.append(Token(t, val))
                cp += len(match.group(0))

        if not found:
            raise Exception(rf'token not recognized near: {s[cp:cp + 100]}')

    return ret


class Integer:
    def __init__(self, value):
        self.value = int(value)


class Float:
    def __init__(self, value):
        self.value = float(value)


class String:
    def __init__(self, value):
        self.value = value[1:-1]


class BinaryOperatorExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Power(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value ** self.right.value


class Multiply(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value * self.right.value


class Divide(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value / self.right.value


class FloorDivide(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value // self.right.value


class Mod(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value % self.right.value


class Negative:
    def __init__(self, expr):
        self.expr = expr

    @property
    def value(self):
        return -self.expr.value


class Add(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value + self.right.value


class Subtract(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value - self.right.value


class Less(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value < self.right.value


class LessEqual(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value <= self.right.value


class Greater(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value > self.right.value


class GreaterEqual(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value >= self.right.value


class Equal(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value == self.right.value


class NotEqual(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value != self.right.value


class Not:
    def __init__(self, expr):
        self.expr = expr

    @property
    def value(self):
        return not self.expr.value


class And(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value and self.right.value


class Or(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value or self.right.value


class FuncCall:
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    @property
    def value(self):
        # print(rf'{self.func_name}({" ".join(str(a.value) for a in self.args)})')
        if self.func_name not in Agent.context:
            raise Exception(rf'{self.func_name} undefined!')
        return Agent.context[self.func_name](*(x.value for x in self.args))


class Variable:
    def __init__(self, name):
        self.name = name

    @property
    def value(self):
        if self.name not in Agent.context:
            raise Exception(rf'{self.name} undefined!')
        return Agent.context[self.name]


class AssignStmt:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    @property
    def value(self):
        Agent.context[self.lhs] = self.rhs.value
        return Agent.context[self.lhs]


class IfBody:
    def __init__(self, cond, stmts):
        self.cond = cond
        self.stmts = stmts

    @property
    def value(self):
        r = False
        if self.cond.value:
            r = True
            for stmt in self.stmts:
                a = stmt.value
        return r


class ElseBody:
    def __init__(self, stmts):
        self.stmts = stmts

    @property
    def value(self):
        for stmt in self.stmts:
            a = stmt.value

        return True


class IfElseBody:
    def __init__(self, if_bodies, else_body=None):
        self.if_bodies = if_bodies
        self.else_body = else_body

    @property
    def value(self):
        for if_body in self.if_bodies:
            if if_body.value:
                return

        if not self.else_body:
            return
        a = self.else_body.value
        return


class WhileBody:
    def __init__(self, cond, stmts):
        self.cond = cond
        self.stmts = stmts

    @property
    def value(self):
        while self.cond.value:
            for stmt in self.stmts:
                a = stmt.value

        return


class FuncDef:
    def __init__(self, func_name, arg_names, stmts):
        self.func_name = func_name
        self.arg_names = arg_names
        self.stmts = stmts

    @property
    def value(self):
        def func(*args):
            local_context = {k: v for k, v in Agent.context.items()}
            if len(self.arg_names) != len(args):
                raise Exception(rf'{self.func_name} requires {len(self.arg_names)} args, but given {len(args)} args!')
            for k, v in zip(self.arg_names, args):
                local_context[k] = v

            pre_context = Agent.context
            Agent.context = local_context

            a = None
            for stmt in self.stmts:
                a = stmt.value

            Agent.context = pre_context
            return a

        Agent.context[self.func_name] = func
        return


class Agent:
    context = {'print': print}

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.cp = 0

    def syntax_error(self, msg):
        return Exception(rf'{msg} syntax error near: {self.cp}!')

    def assert_not_end(self):
        if self.cp >= len(self.tokens):
            raise Exception(rf'tokens end!')

    def has_next_token(self):
        return self.cp < len(self.tokens)

    def peek_next_token(self):
        self.assert_not_end()
        cur_token = self.tokens[self.cp]
        return cur_token

    def get_next_token(self):
        self.assert_not_end()
        cur_token = self.tokens[self.cp]
        self.cp += 1
        return cur_token

    def get_atomic_expr(self):
        cur_token = self.get_next_token()
        if cur_token.type == Token.Type.INT:
            return Integer(cur_token.value)
        elif cur_token.type == Token.Type.FLOAT:
            return Float(cur_token.value)
        elif cur_token.type == Token.Type.STR:
            return String(cur_token.value)
        elif cur_token.type == Token.Type.IDN:
            if not self.has_next_token():
                return Variable(cur_token.value)
            next_token = self.peek_next_token()
            if next_token.type != Token.Type.LP:
                return Variable(cur_token.value)
            self.cp += 1

            func_name = cur_token.value
            args = []
            cur_token = self.peek_next_token()
            while cur_token.type != Token.Type.RP:
                if not self.has_next_token():
                    raise self.syntax_error(rf'Token(RP) expected!')
                cur_token = self.peek_next_token()
                if cur_token.type != Token.Type.RP:
                    args.append(self.get_expr())

            self.cp += 1
            return FuncCall(func_name, args)

        elif cur_token.type == Token.Type.LP:
            e = self.get_expr()
            cur_token = self.get_next_token()
            if cur_token.type == Token.Type.RP:
                return e
            else:
                raise self.syntax_error("token(RP) expected!")
        else:
            raise self.syntax_error(rf"{cur_token} cannot recognized!")

    def get_pow_expr(self):
        a = self.get_atomic_expr()
        if not self.has_next_token():
            return a
        cur_token = self.peek_next_token()
        if cur_token.type != Token.Type.POW:
            return a
        self.cp += 1
        b = self.get_pow_expr()
        return Power(a, b)

    def get_unary_expr(self):
        cur_token = self.peek_next_token()
        if cur_token.type == Token.Type.ADD:
            self.cp += 1
            return self.get_unary_expr()
        elif cur_token.type == Token.Type.SUB:
            self.cp += 1
            return Negative(self.get_unary_expr())
        else:
            return self.get_pow_expr()

    def get_mul_expr(self):
        a = self.get_unary_expr()
        if not self.has_next_token():
            return a
        cur_token = self.peek_next_token()
        while cur_token.type in (Token.Type.MUL, Token.Type.DIV, Token.Type.FLOOR_DIV, Token.Type.MOD):
            self.cp += 1
            b = self.get_unary_expr()
            if cur_token.type == Token.Type.MUL:
                a = Multiply(a, b)
            elif cur_token.type == Token.Type.FLOOR_DIV:
                a = FloorDivide(a, b)
            elif cur_token.type == Token.Type.MOD:
                a = Mod(a, b)
            else:
                a = Divide(a, b)
            if not self.has_next_token():
                return a
            cur_token = self.peek_next_token()
        return a

    def get_add_expr(self):
        a = self.get_mul_expr()
        if not self.has_next_token():
            return a
        cur_token = self.peek_next_token()
        while cur_token.type in (Token.Type.ADD, Token.Type.SUB):
            self.cp += 1
            b = self.get_mul_expr()
            if cur_token.type == Token.Type.ADD:
                a = Add(a, b)
            else:
                a = Subtract(a, b)
            if not self.has_next_token():
                return a
            cur_token = self.peek_next_token()
        return a

    def get_cmp_expr(self):
        a = self.get_add_expr()
        if not self.has_next_token():
            return a
        cur_token = self.peek_next_token()
        while cur_token.type in (Token.Type.EQ,
                                 Token.Type.NE, Token.Type.GT, Token.Type.GE, Token.Type.LT, Token.Type.LE,):
            self.cp += 1
            b = self.get_add_expr()
            if cur_token.type == Token.Type.EQ:
                a = Equal(a, b)
            elif cur_token.type == Token.Type.NE:
                a = NotEqual(a, b)
            elif cur_token.type == Token.Type.GT:
                a = Greater(a, b)
            elif cur_token.type == Token.Type.GE:
                a = GreaterEqual(a, b)
            elif cur_token.type == Token.Type.LT:
                a = Less(a, b)
            else:
                a = LessEqual(a, b)
            if not self.has_next_token():
                return a
            cur_token = self.peek_next_token()
        return a

    def get_not_expr(self):
        cur_token = self.peek_next_token()
        if cur_token.type == Token.Type.NOT:
            self.cp += 1
            return Not(self.get_not_expr())
        return self.get_cmp_expr()

    def get_and_expr(self):
        a = self.get_not_expr()
        if not self.has_next_token():
            return a
        cur_token = self.peek_next_token()
        while cur_token.type in (Token.Type.AND,):
            self.cp += 1
            b = self.get_not_expr()
            a = And(a, b)
            if not self.has_next_token():
                return a
            cur_token = self.peek_next_token()
        return a

    def get_or_expr(self):
        a = self.get_and_expr()
        if not self.has_next_token():
            return a
        cur_token = self.peek_next_token()
        while cur_token.type in (Token.Type.OR,):
            self.cp += 1
            b = self.get_and_expr()
            a = Or(a, b)
            if not self.has_next_token():
                return a
            cur_token = self.peek_next_token()
        return a

    def get_expr(self):
        return self.get_or_expr()

    def get_assign_stmt(self):
        cur_token = self.peek_next_token()
        if cur_token.type != Token.Type.IDN:
            return self.get_expr()
        lhs = cur_token.value
        self.cp += 1
        if not self.has_next_token():
            return Variable(lhs.value)

        cur_token = self.peek_next_token()
        if cur_token.type != Token.Type.ASSIGN:
            self.cp -= 1
            return self.get_expr()

        self.cp += 1
        rhs = self.get_expr()
        return AssignStmt(lhs, rhs)

    def get_if_body(self):
        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.IF:
            raise self.syntax_error(rf'Token(IF) expected!')

        cond = self.get_expr()

        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.LD:
            raise self.syntax_error(rf'Token(LD) expected!')

        cur_token = self.peek_next_token()
        sub_bodies = []
        while cur_token.type != Token.Type.RD:
            sub_bodies.append(self.get_body())
            cur_token = self.peek_next_token()
        self.cp += 1
        return IfBody(cond, sub_bodies)

    def get_elif_body(self):
        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.ELIF:
            raise self.syntax_error(rf'Token(IF) expected!')

        cond = self.get_expr()

        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.LD:
            raise self.syntax_error(rf'Token(LD) expected!')

        cur_token = self.peek_next_token()
        sub_bodies = []
        while cur_token.type != Token.Type.RD:
            sub_bodies.append(self.get_body())
            cur_token = self.peek_next_token()
        self.cp += 1
        return IfBody(cond, sub_bodies)

    def get_else_body(self):
        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.ELSE:
            raise self.syntax_error(rf'Token(IF) expected!')

        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.LD:
            raise self.syntax_error(rf'Token(LD) expected!')

        cur_token = self.peek_next_token()
        sub_bodies = []
        while cur_token.type != Token.Type.RD:
            sub_bodies.append(self.get_body())
            cur_token = self.peek_next_token()
        self.cp += 1
        return ElseBody(sub_bodies)

    def get_if_else_body(self):
        if_body = self.get_if_body()
        if not self.has_next_token():
            return IfElseBody([if_body])
        if_bodies = [if_body]
        cur_token = self.peek_next_token()
        while cur_token.type == Token.Type.ELIF:
            if_bodies.append(self.get_elif_body())
            if not self.has_next_token():
                return IfElseBody(if_bodies)
            cur_token = self.peek_next_token()

        else_bocy = None
        if cur_token.type == Token.Type.ELSE:
            else_bocy = self.get_else_body()

        return IfElseBody(if_bodies, else_bocy)

    def get_while_body(self):
        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.WHILE:
            raise self.syntax_error(rf'Token(WHILE) expected!')
        cond = self.get_expr()
        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.LD:
            raise self.syntax_error(rf'Token(LD) expected!')
        sub_bodies = []
        cur_token = self.peek_next_token()
        while cur_token.type != Token.Type.RD:
            sub_bodies.append(self.get_body())
            if not self.has_next_token():
                return WhileBody(cond, sub_bodies)
            cur_token = self.peek_next_token()
        self.cp += 1
        return WhileBody(cond, sub_bodies)

    def get_func_body(self):
        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.FUNC:
            raise self.syntax_error(rf'Token(FUNC) expected!')
        func_name = self.get_next_token().value

        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.LP:
            raise self.syntax_error(rf'Token(LP) expected!')
        args = []
        cur_token = self.peek_next_token()
        while cur_token.type != Token.Type.RP:
            if not self.has_next_token():
                raise self.syntax_error(rf'Token(RP) expected!')

            cur_token = self.get_next_token()
            if cur_token.type == Token.Type.IDN:
                args.append(cur_token.value)
                cur_token = self.peek_next_token()
            elif cur_token.type != Token.Type.RP:
                raise self.syntax_error(rf'Token(IDN) expected!')

        self.cp += 1

        cur_token = self.get_next_token()
        if cur_token.type != Token.Type.LD:
            raise self.syntax_error(rf'Token(LD) expected!')
        sub_bodies = []
        cur_token = self.peek_next_token()
        while cur_token.type != Token.Type.RD:
            sub_bodies.append(self.get_body())
            if not self.has_next_token():
                return FuncDef(func_name, args, sub_bodies)
            cur_token = self.peek_next_token()
        self.cp += 1
        return FuncDef(func_name, args, sub_bodies)

    def get_body(self):
        cur_token = self.peek_next_token()
        if cur_token.type == Token.Type.IF:
            return self.get_if_else_body()
        elif cur_token.type == Token.Type.WHILE:
            return self.get_while_body()
        elif cur_token.type == Token.Type.FUNC:
            return self.get_func_body()
        return self.get_assign_stmt()

    def run(self):
        while self.has_next_token():
            body = self.get_body()
            a = body.value


if __name__ == '__main__':
    s = '''
    
    func sqrt(n){
        x=1
        new_x=n
        while x!=new_x{
            x=new_x
            new_x=(x+n/x)/2
        }
        x
    }
    
    func abs(n){
        ret=n
        if n<0{
            ret=-n
        }
        ret
    }
    
    func root(f lo hi){
        mi=(lo+hi)/2
        if (hi-lo)<0.000001{
            ret=mi
        }
        elif f(lo)*f(mi)<=0{
            ret=root(f lo mi)
        }else{
            ret=root(f mi hi)
        }
        ret
    }
    
    func fff(n){
        n*n-3
    }
    
    print(root(fff 0 10))
        
    '''

    tokens = get_tokens(s)
    agent = Agent(tokens)
    agent.run()
