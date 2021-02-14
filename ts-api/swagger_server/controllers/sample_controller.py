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
            FROM samples
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


def get_data_sets():  # noqa: E501
    """get data set

    get data set # noqa: E501


    :rtype: DataSetResponse
    """
    conn = connect()
    sql = """
            SELECT id, name, uid_from, uid_to
            FROM data_set
        """
    rows = select_execute(conn, sql)
    return {
        'data': [{
            "id": row[0],
            "name": row[1],
            "uid_from": row[2],
            "uid_to": row[3]
        } for row in rows],
        'query_string': sql
    }


def set_data_sets(body):  # noqa: E501
    """add or update data set

    add or update data set # noqa: E501

    :param body:
    :type body: list | bytes

    :rtype: None
    """
    body = json.loads(body)

    conn = connect()
    if body['id']:
        sql = """UPDATE data_set
            SET name=%s, uid_from=%s, uid_to=%s
            WHERE id=%s """
        with conn.cursor() as cur:
            cur.execute(sql, (body['name'],
                              body['uid_from'],
                              body['uid_to'],
                              body['id']))
    else:
        sql = """INSERT INTO data_set ("name", "uid_from", "uid_to") 
            VALUES (%s, %s, %s) """
        with conn.cursor() as cur:
            cur.execute(sql, (body['name'],
                              body['uid_from'],
                              body['uid_to']))
    conn.commit()

    return 'done'
