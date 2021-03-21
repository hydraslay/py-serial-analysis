import os
import zipfile
import psycopg2
from swagger_server.fit.pre import start_fit, start_predict
from sklearn.datasets import make_multilabel_classification

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


def zipdir(path, ziph):
    # ziph is zipfile handle
    depth = len(path.split(os.sep)) - 1
    for root, dirs, files in os.walk(path):
        arc_path = os.sep.join(root.split(os.sep)[depth:])
        for file in files:
            ziph.write(os.path.join(root, file), os.path.join(arc_path, file))


def get_fits():  # noqa: E501

    return 'do some magic!'


def set_fit(body):  # noqa: E501
    conn = connect()
    sql = '''
        SELECT sample_data, value, uid 
        FROM data_set ds, samples sa
        where ds.uid_from < sa.uid and ds.uid_to > sa.uid and ds.id=%s'''
    rows = select_execute(conn, sql, tuple([int(body['dataSet'])]))
    dataset_x = []
    dataset_y = []
    vol = []
    for row in rows:
        price = []
        vols = []
        prev_high = 0
        prev_low = 0
        for i, tick in enumerate(row[0]):
            if i > 0:
                price.append(tick['high'] - prev_high)
                price.append(tick['low'] - prev_low)
                vols.append(tick['volume'])
            prev_high = tick['high']
            prev_low = tick['low']
        dataset_x.append(price)
        dataset_y.append([row[1]])
        vol.append(vols)

    start_fit(dataset_x, dataset_y, vol)

    # zip
    zipf = zipfile.ZipFile(os.path.join('tmp', 'model.zip'), 'w', zipfile.ZIP_DEFLATED)
    zipdir(os.path.join('tmp', 'model'), zipf)
    zipf.close()

    start_predict()
    # upload to s3
    return 'do some magic!'
