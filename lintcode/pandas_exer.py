
import pandas as pd

s=pd.Series(range(10,0,-1))
print(s)

print(s.values)

print(s.index)


df=pd.DataFrame({
    'name':["zxb",'jh','jsj'],
    'age':[32,26,34]
})

print(df)

df=pd.read_csv('a.csv')
print(df)

