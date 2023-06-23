class Stack {
    data = []

    push(val) {
        this.data.push(val)
    }

    pop() {
        if (this.data.length === 0) {
            throw 'Stack is empty!'
        }
        return this.data.pop()
    }

    length() {
        return this.data.length
    }

    to_string() {
        return this.data.join(', ')
    }
}

function to_decimal(num_str, base) {
    let digit_map = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'a': 10,
        'b': 11,
        'c': 12,
        'd': 13,
        'e': 14,
        'f': 15,
    }
    let ret = 0
    f = 1
    for (let i = num_str.length - 1; i >= 0; i--) {
        c = num_str[i].toLowerCase()
        ret += digit_map[c] * f
        f *= base
    }
    return ret
}

function from_decimal(num, base) {
    let digit_map = {
        0:'0',
        1:'1',
        2:'2',
        3:'3',
        4:'4',
        5:'5',
        6:'6',
        7:'7',
        8:'8',
        9:'9',
        10:'a',
        11:'b',
        12:'c',
        13:'d',
        14:'e',
        15:'f',
    }
    let digits = new Stack()
    while (num > 0) {
        digits.push(digit_map[num % base])
        num = Math.floor(num / base)
    }
    let ret = []
    while (digits.length() > 0) {
        ret.push(digits.pop())
    }
    return ret.join('')

}

function convert_num(num_str, from_base, to_base) {
    let dec = to_decimal(num_str, from_base)
    return from_decimal(dec, to_base)
}

function req(){
    let xhr=new XMLHttpRequest()
    xhr.open()
}

function test() {
    let s='zhangxinbo_shijihong_jiaohui_'
    var reg=/_/gi
    let a=s.split(reg)
    console.log(a)
}