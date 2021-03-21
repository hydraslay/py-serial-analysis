import json

import psycopg2


def connect():
    con = psycopg2.connect("host=" + "localhost" +
                           " port=" + "5434" +
                           " dbname=" + "ts" +
                           " user=" + "test" +
                           " password=" + "test")
    return con


def select_execute(con, sql, params=()):
    with con.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    return rows


def get_models():  # noqa: E501
    conn = connect()
    sql = """
            SELECT model, description, params, state stat
	        FROM models;
        """
    rows = select_execute(conn, sql)
    return {
        'data': [{
            "model": row[0],
            "description": row[1],
            "params": row[2],
            "stat": row[3]
        } for row in rows],
        'query_string': sql
    }


def get_sample_types():  # noqa: E501
    return 'do some magic!'


def set_model(body):  # noqa: E501
    conn = connect()
    sql = """INSERT INTO models ("model", "description", "params", "state") 
        VALUES (%s, %s, %s, %s) 
        ON CONFLICT ("model") DO UPDATE SET 
        description=%s, params=%s, state=%s
        """
    with conn.cursor() as cur:
        cur.execute(sql, (body['model'],
                          body['description'],
                          json.dumps(body['params']),
                          body['stat'],
                          body['description'],
                          json.dumps(body['params']),
                          body['stat']))
    conn.commit()
    return 'done'
