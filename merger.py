import pandas as pd

nm = pd.read_csv("nm_PD.csv")
jw = pd.read_csv("jw_PD.csv")

merged_df = pd.merge(nm, jw, on='date', how='outer').fillna(0)
merged_df.to_csv("output.csv", index=False)
