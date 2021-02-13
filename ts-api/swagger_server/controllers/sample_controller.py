import connexion
import psycopg2
import json


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


def get_samples():  # noqa: E501
    """get Sample list

    get Sample list # noqa: E501


    :rtype: SamplesResponse
    """
    conn = connect()
    sql = """
            SELECT uid, sample_data, value
            FROM public.samples
        """
    rows = select_execute(conn, sql)
    return {
        'data': [{
            "uid": row[0],
            "sample_data": row[1],
            "value": row[2]
        } for row in rows],
        'query_string': sql
    }


def set_samples(body):  # noqa: E501
    """add or update sample

    add or update sample # noqa: E501

    :param body: 
    :type body: list | bytes

    :rtype: None
    """
    # if connexion.request.is_json:
    #     body = [Samples.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501

    body = json.loads(body)

    conn = connect()
    for row in body:
        sql = """INSERT INTO samples ("uid", "sample_data", "value") 
            VALUES (%s, %s, %s) 
            ON CONFLICT ("uid") DO UPDATE SET 
            sample_data=%s, value=%s"""
        with conn.cursor() as cur:
            cur.execute(sql, (row['uid'],
                              json.dumps(row['sampleData']),
                              row['value'],
                              json.dumps(row['sampleData']),
                              row['value']))
        conn.commit()

    return 'done'
