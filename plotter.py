import pandas as pd
import matplotlib.pyplot as plt


def plot_bar_chart(csv_file):
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    plt.bar(df['date'], df['totalVehicleNearCol'])
    plt.xlabel('Date')
    plt.ylabel('Near misses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


plot_bar_chart("nm_PD.csv")