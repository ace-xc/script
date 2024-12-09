import pandas as pd

df = pd.read_excel("data.xlsx")

df_unique = df.drop_duplicates(subset='SQL')

df_unique.to_excel("data.xlsx", index=False)