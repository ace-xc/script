# 删除excel中存在某个关键字的所有行，例如JOIN
import pandas as pd

df = pd.read_excel("test.xlsx")
df = df[~df['sql'].str.contains('JOIN', na=False)]
df.to_excel("test.xlsx", index=False)
