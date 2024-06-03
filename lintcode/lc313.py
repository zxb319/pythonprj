import re

s = '1234567890'
mat = re.search(r'^\d+$', s)

print(mat)
