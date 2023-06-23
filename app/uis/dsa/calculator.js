let TokenRegMap = {
    NUM: /^\d+\.?\d*/,
    LP: /^\(/,
    RP: /^\)/,
    COMMA: /^\,/,
    ADD: /^\+/,
    SUB: /^\-/,
    MUL: /^\*/,
    DIV: /^\//,
    IDN: /^[a-z_][a-z_0-9]*/i,
    WHITE: /^\s+/,
}

let TokenTypes ={}
for(t in TokenRegMap){
    TokenTypes[t]=t
}

class Token {
    constructor(type, value) {
        this.type = type;
        this.value = value;
    }

    to_string() {
        return `(${this.type},${this.value})`
    }
}

function isWhilte(s) {
    return /^\s+$/.test(s)
}

function get_tokens(s) {
    let ret = []
    while (s.length > 0) {
        for (const t in TokenRegMap) {
            let reg = TokenRegMap[t]
            reg = reg.exec(s)
            if (reg !== null) {
                ret.push({type: t, value: reg[0]})
                s = s.substr(reg.length)
                break
            }

        }
    }
    return ret
}

class Num{
    constructor(value) {
        this._value=Number(value)
    }
    value(){
        return this._value
    }
}

class Neg{
    constructor(exp) {
        this._exp=exp
    }

    value(){
        return -exp.value()
    }
}

class Pos{
    constructor(exp) {
        this._exp=exp
    }

    value(){
        return this._value
    }
}

function test() {
    console.log(new Neg(1).value())
}