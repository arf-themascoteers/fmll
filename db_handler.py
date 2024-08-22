import sqlite3


def create_connection():
    conn = sqlite3.connect('path_data.db')
    cur = conn.cursor()
    return cur, conn


def close_connection(conn):
    conn.close()


def get_data_by_from_to_netId(f,t,n):
    cur, conn = create_connection()
    cur.execute('''
        SELECT x, y, channelId, objectId FROM path 
        WHERE networkId = ? AND timestamp BETWEEN ? AND ?
    ''', (n, f, t))
    rows = cur.fetchall()
    close_connection(conn)
    return rows


if __name__ == '__main__':
    f = 1716879591600
    t = 1716879691600
    n = "CM99V122139007597"
    r = get_data_by_from_to_netId(f,t,n)
    print(r)