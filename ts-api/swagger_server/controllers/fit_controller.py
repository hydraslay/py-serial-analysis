import connexion
import psycopg2
import json
import os
from swagger_server.fit.pre import start_fit, start_predict
import zipfile


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
    # start_fit()

    # zip
    zipf = zipfile.ZipFile(os.path.join('tmp', 'model.zip'), 'w', zipfile.ZIP_DEFLATED)
    zipdir(os.path.join('tmp', 'model'), zipf)
    zipf.close()

    start_predict()
    # upload to s3
    return 'do some magic!'
