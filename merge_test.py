import pandas as pd


def merge_csv(output_csv):
    df1 = pd.DataFrame({
        'id': [1, 2, 3],
        'x': [10, 20, 30]
    })

    df2 = pd.DataFrame({
        'id': [2, 3, 4],
        'y': [200, 300, 400]
    })

    merged_df = pd.merge(df1, df2, on='id', how='outer').fillna(0)
    merged_df.to_csv(output_csv, index=False)


# Example usage
merge_csv('output.csv')