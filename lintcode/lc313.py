
import hashlib

a=hashlib.md5(rf'zzz'.encode()).hexdigest()

print(a)

a=hashlib.md5(rf'zxb'.encode()).hexdigest()

print(a,len(a))