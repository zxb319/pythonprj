import pandas as pd

df = pd.DataFrame(data={
    'a': [1, pd.NA, 3],
    'b': ['q', 'w', 'e']
})

df['c'] = df.apply(lambda x: x['b'] if pd.isna(x['a']) else x['b'] * 2, axis=1)


df.groupby(by='').apply()