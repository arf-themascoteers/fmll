import sqlite3


def create_connection():
    conn = sqlite3.connect('path_data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return cur, conn


def close_connection(conn):
    conn.close()


def get_data_by_from_to_netId(f,t,n):
    cur, conn = create_connection()
    cur.execute('''
        SELECT x, y, channelId, objectId, timestamp FROM path 
        WHERE networkId = ? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp
    ''', (n, f, t))
    rows = cur.fetchall()
    close_connection(conn)
    return rows

def get_data_by_netId(n):
    cur, conn = create_connection()
    cur.execute('''
        SELECT x, y, channelId, objectId, timestamp FROM path 
        WHERE networkId = ?
        ORDER BY timestamp
    ''', (n,))
    rows = cur.fetchall()
    close_connection(conn)
    return rows


if __name__ == '__main__':
    n = "CM99V122139007597"
    r = get_data_by_netId(n)
    print(r[0]["x"])