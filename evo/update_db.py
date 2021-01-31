import psycopg2
import os
import pandas as pd
from dateutil.parser import parse

interval = '5'

def connect():
    con = psycopg2.connect("host=" + "localhost" +
                           " port=" + "5434" +
                           " dbname=" + "ts" +
                           " user=" + "test" +
                           " password=" + "test")
    return con


def select_execute(con, sql):
    with con.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    return rows


if __name__ == '__main__':
    con = connect()

    # list_product = ['1', '5', '15']
    # for item in list_product:

    filename = os.path.join(os.path.dirname(__file__), 'data', 'USDJPY{i}.csv'.format_map({'i': interval}))
    df = pd.read_csv(filename, header=None, delimiter=',')
    for df_row in df.iterrows():
        row = df_row[1]
        ts = parse(row[0] + ' ' + row[1])
        sql = """INSERT INTO market_data ("type", "timestamp", "open", "high", "low", "close", "volume") 
            VALUES (%s, round(%s, 6), round(%s, 6), round(%s, 6), round(%s, 6), round(%s, 6), round(%s, 6)) 
            ON CONFLICT ("type", "timestamp") DO UPDATE SET 
              open=round(%s, 6), high=round(%s, 6), low=round(%s, 6), close=round(%s, 6), volume=round(%s, 6)"""
        with con.cursor() as cur:
            cur.execute(sql, (
                interval,
                ts.timestamp(),
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            ))
        con.commit()
