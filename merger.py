import pandas as pd

for s in ["A","D","O","P","PD"]:
    nm = pd.read_csv(f"nm_{s}.csv")
    jw = pd.read_csv(f"jw_{s}.csv")
    nm = nm.drop(columns=['is_holiday'])

    merged_df = pd.merge(nm, jw, on='date', how='outer').fillna(0)

    merged_df['totalNearmiss'] = merged_df['totalNearmiss'].astype(int)
    merged_df['totalVehicleNearCol'] = merged_df['totalVehicleNearCol'].astype(int)
    merged_df['totalJW'] = merged_df['totalJW'].astype(int)
    merged_df['is_holiday'] = merged_df['is_holiday'].astype(int)


    merged_df.to_csv(f"report_{s}.csv", index=False)
