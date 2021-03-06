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
    sql = """SELECT dset.id, dset.name, dset.uid_from, dset.uid_to, gp.cnt
            from
            (
                SELECT ds.id, count(sa.uid) cnt
                FROM data_set ds 
                inner join samples sa on sa.uid > ds.uid_from and sa.uid < ds.uid_to
                group by ds.id 
            ) gp 
            inner join data_set dset on gp.id = dset.id
        """
    rows = select_execute(conn, sql)
    return {
        'data': [{
            "id": row[0],
            "name": row[1],
            "uidFrom": row[2],
            "uidTo": row[3],
            "count": row[4]
        } for row in rows],
        'query_string': sql
    }


def set_data_set(body):  # noqa: E501
    """add or update data set
    add or update data set # noqa: E501
    :param body:
    :type body: list | bytes
    :rtype: None
    """

    conn = connect()
    if body['id']:
        sql = """UPDATE data_set
            SET name=%s, uid_from=%s, uid_to=%s
            WHERE id=%s """
        with conn.cursor() as cur:
            cur.execute(sql, (body['name'],
                              body['uidFrom'],
                              body['uidTo'],
                              body['id']))
    else:
        sql = """INSERT INTO data_set ("name", "uid_from", "uid_to") 
            VALUES (%s, %s, %s) """
        with conn.cursor() as cur:
            cur.execute(sql, (body['name'],
                              body['uidFrom'],
                              body['uidTo']))
    conn.commit()

    return 'done'


def get_sample_summary(body):  # noqa: E501
    if len(body) == 0:
        return {
            'data': [],
            'query_string': 'nothing'
        }

    s = ''
    for row in body:
        if len(s) > 0:
            s = s + ', '
        s = s + """('{0}','{1}')""".format(row['from'], row['to'])

    conn = connect()
    sql = """SELECT cond.from, cond.to, count(1) "count"
        FROM (
            values {0}
        ) cond("from", "to")
        left join samples sa on cond.from <= sa.uid and cond.to >= sa.uid
        group by cond.from, cond.to
        """.format(s)

    rows = select_execute(conn, sql)
    return {
        'data': [{
            "from": row[0],
            "to": row[1],
            "count": row[2]
        } for row in rows],
        'query_string': sql
    }