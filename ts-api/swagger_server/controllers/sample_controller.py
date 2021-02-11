import connexion
import six

from swagger_server.models.samples import Samples  # noqa: E501
from swagger_server.models.samples_response import SamplesResponse  # noqa: E501
from swagger_server import util


def get_samples():  # noqa: E501
    """get Sample list

    get Sample list # noqa: E501


    :rtype: SamplesResponse
    """
    return 'do some magic!'


def set_sample_and_value_data(body):  # noqa: E501
    """add or update sample

    add or update sample # noqa: E501

    :param body: 
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [Samples.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'
