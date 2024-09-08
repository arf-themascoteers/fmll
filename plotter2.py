import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_bar_chart(csv_file, loc, filename):
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df['date'])

    bar_width = 0.2
    indices = np.arange(len(df))

    plt.figure(figsize=(len(df) * 0.3, 6))

    plt.bar(indices, df['totalNearmiss'], width=bar_width, label='Nearmiss',
            color=np.where(df['is_holiday'] == 1, 'lightcoral', 'blue'))
    plt.bar(indices + bar_width, df['totalVehicleNearCol'], width=bar_width, label='Vehicle near misses',
            color=np.where(df['is_holiday'] == 1, 'lightgreen', 'green'))
    plt.bar(indices + 2 * bar_width, df['totalJW'], width=bar_width, label='Jaywalking',
            color=np.where(df['is_holiday'] == 1, 'lightpink', 'red'))

    plt.xlabel('Date')
    plt.ylabel('Counts')

    xticks_indices = np.arange(0, len(df), 7)
    plt.xticks(xticks_indices + bar_width, df['date'].dt.strftime('%Y-%m-%d').iloc[xticks_indices], rotation=45)

    plt.legend()
    plt.tight_layout()
    filename = f"{filename}.png"
    dest = os.path.join(loc, filename)
    plt.savefig(dest)

loc = r"C:\Users\kisho\OneDrive - Web Mascot Pty Ltd\Desktop\fmll2"

for f in os.listdir(loc):
    if f.startswith("report_") and f.endswith(".csv"):
        plot_bar_chart(os.path.join(loc, f),loc, f)
