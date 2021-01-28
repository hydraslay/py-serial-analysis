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


def get_raw_data():  # noqa: E501
    """get RawData

    get RawData # noqa: E501


    :rtype: List[RawData]
    """

    conn = connect()
    rows = select_execute(conn, """
        SELECT "timestamp", open, high, low, close, volume
        FROM public.market_data
        where type = '1'
        limit 20
    """)
    return [{
        "timestamp": row[0],
        "open": row[1],
        "high": row[2],
        "low": row[3],
        "close": row[4],
        "volume": row[5]
    } for row in rows]

