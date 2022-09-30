import re

regexes=[
    r'[0-9]{4}-1[0-2]',
    r'[0-9]{4}-0[1-9]',
    r'[0-9]{4}-[1-9]',
    r'[0-9]{4}1[0-2]',
    r'[0-9]{4}0[1-9]',
    r'1[0-2]',
    r'0[1-9]',
    r'[1-9]',
]
ex=rf'^({"|".join(regexes)})$'
print(ex)
a = [x for x in re.split(r'[\s,|]+', '8 2022-9 2022111') if re.search(ex,x)]

for i in a:
    print(i)
