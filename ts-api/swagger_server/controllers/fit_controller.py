import connexion
import six

from swagger_server.models.fit_request import FitRequest  # noqa: E501
from swagger_server.models.fits_response import FitsResponse  # noqa: E501
from swagger_server import util


def get_fits():  # noqa: E501
    """get fit status

    get fit status # noqa: E501


    :rtype: FitsResponse
    """
    return 'do some magic!'


def set_fit(body):  # noqa: E501
    """begin or cancel a fit process

    begin or cancel a fit process # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = FitRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
