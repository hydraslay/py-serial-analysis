import connexion
import six

from swagger_server.models.model import Model  # noqa: E501
from swagger_server.models.sample_types import SampleTypes  # noqa: E501
from swagger_server import util


def get_models():  # noqa: E501
    """get Model list

    get Model list # noqa: E501


    :rtype: Model
    """
    return 'do some magic!'


def get_sample_types():  # noqa: E501
    """get sample type list

    get sample type list # noqa: E501


    :rtype: SampleTypes
    """
    return 'do some magic!'


def set_model(body):  # noqa: E501
    """add or update Model

    add or update Model # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Model.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
