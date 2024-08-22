import sqlite3
import requests

start = 1718845200
end = 1718855200
token = '666f7f95ef93326dba001c82'
netid = 'CM99V122139007597'

conn = sqlite3.connect('path_data.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS path (
        timestamp INTEGER,
        channelId INTEGER,
        x INTEGER,
        y INTEGER
    )
''')

def fetch_and_store(fcdt, tcdt):
    url = f'https://app.alphax.cloud/getPathData?token={token}&netid={netid}&fcdt={fcdt}&tcdt={tcdt}'
    print(url)
    response = requests.get(url)
    data = response.json()

    if 'pathData' not in data:
        return

    for item in data['pathData']:
        timestamp = item['timestamp']
        cur.execute('SELECT 1 FROM path WHERE timestamp = ?', (timestamp,))
        if cur.fetchone():
            continue

        for entry in item['data']:
            channelId = entry['channelId']
            if channelId == 253:
                continue
            for value in entry['value']:
                x, y = value[0], value[1]
                cur.execute('INSERT INTO path (timestamp, channelId, x, y) VALUES (?, ?, ?, ?)', (timestamp, channelId, x, y))

    conn.commit()

current_fcdt = start
while current_fcdt < end:
    next_tcdt = current_fcdt + 3600
    fetch_and_store(current_fcdt, next_tcdt)
    current_fcdt = next_tcdt + 1

conn.close()
