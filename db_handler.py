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
        SELECT x, y, channelId FROM path 
        WHERE networkId = ? AND timestamp BETWEEN ? AND ?
    ''', (n, f, t))
    rows = cur.fetchall()
    return rows