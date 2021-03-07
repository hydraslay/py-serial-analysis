# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.fit import Fit  # noqa: F401,E501
from swagger_server import util


class FitsResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, data: List[Fit]=None, query_string: str=None):  # noqa: E501
        """FitsResponse - a model defined in Swagger

        :param data: The data of this FitsResponse.  # noqa: E501
        :type data: List[Fit]
        :param query_string: The query_string of this FitsResponse.  # noqa: E501
        :type query_string: str
        """
        self.swagger_types = {
            'data': List[Fit],
            'query_string': str
        }

        self.attribute_map = {
            'data': 'data',
            'query_string': 'query_string'
        }
        self._data = data
        self._query_string = query_string

    @classmethod
    def from_dict(cls, dikt) -> 'FitsResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FitsResponse of this FitsResponse.  # noqa: E501
        :rtype: FitsResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> List[Fit]:
        """Gets the data of this FitsResponse.


        :return: The data of this FitsResponse.
        :rtype: List[Fit]
        """
        return self._data

    @data.setter
    def data(self, data: List[Fit]):
        """Sets the data of this FitsResponse.


        :param data: The data of this FitsResponse.
        :type data: List[Fit]
        """

        self._data = data

    @property
    def query_string(self) -> str:
        """Gets the query_string of this FitsResponse.


        :return: The query_string of this FitsResponse.
        :rtype: str
        """
        return self._query_string

    @query_string.setter
    def query_string(self, query_string: str):
        """Sets the query_string of this FitsResponse.


        :param query_string: The query_string of this FitsResponse.
        :type query_string: str
        """

        self._query_string = query_string