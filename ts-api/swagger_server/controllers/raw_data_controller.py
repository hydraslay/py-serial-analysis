import connexion
import six

from swagger_server.models.raw_data import RawData  # noqa: E501
from swagger_server import util
import psycopg2
import os
import pandas as pd
from dateutil.parser import parse


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


def get_raw_data(interval, start, end):  # noqa: E501
    """get RawData

    get RawData # noqa: E501


    :rtype: List[RawData]
    """

    conn = connect()
    rows = select_execute(conn, """
        SELECT "timestamp", open, high, low, close, volume
        FROM public.market_data
        where type = '{interval}' and timestamp>={start} and timestamp<={end}
        order by "timestamp" ASC
    """.format_map({
        'interval': interval,
        'start': start,
        'end': end
    }))
    return [{
        "timestamp": row[0],
        "open": row[1],
        "high": row[2],
        "low": row[3],
        "close": row[4],
        "volume": row[5]
    } for row in rows]


def get_market_break_point():
    conn = connect()
    rows = select_execute(conn, """
        select dt.date
        from
            (
                select to_char(i::date, 'YYYY/MM/DD') as date 
                from generate_series('2020-02-01', CURRENT_DATE, '1 day'::interval) i
            ) dt
            left outer join
            (
                SELECT type, to_char(to_timestamp("timestamp"), 'YYYY/MM/DD') as ymd
                FROM public.market_data
                where type ='5'
                group by type, ymd
            ) raw on dt.date=raw.ymd
            where raw.ymd is null
            order by dt.date
        """)
    return [{
        "timestamp": row[0]
    } for row in rows]
