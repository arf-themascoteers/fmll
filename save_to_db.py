import sqlite3
import requests

start = 1716771600
#end = 1716871600
end = 1723597200
token = '666f7f95ef93326dba001c82'
netid = 'CM99V122113000052'

#CM99V122139007597#amberly
#CM27V122149004668#school
#CM99V122113000052#ormond

conn = sqlite3.connect('path_data.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS path (
        networkId TEXT,
        timestamp INTEGER,
        channelId INTEGER,
        objectId INTEGER,
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
        entry = item['data'][0]
        objectId = item['data'][1]["value"]
        channelId = entry['channelId']
        for value in entry['value']:
            x, y = value[0], value[1]
            cur.execute('INSERT INTO path (networkId, timestamp, channelId, objectId, x, y) '
                        'VALUES (?, ?, ?, ?, ?,?)',
                        (netid, timestamp, channelId, objectId, x, y))

    conn.commit()

current_fcdt = start
while current_fcdt < end:
    next_tcdt = current_fcdt + 36000
    fetch_and_store(current_fcdt, next_tcdt)
    current_fcdt = next_tcdt + 1

conn.close()
