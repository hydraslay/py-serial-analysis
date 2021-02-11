# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.samples import Samples  # noqa: F401,E501
from swagger_server import util


class SamplesResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, data: List[Samples]=None, query_string: str=None):  # noqa: E501
        """SamplesResponse - a model defined in Swagger

        :param data: The data of this SamplesResponse.  # noqa: E501
        :type data: List[Samples]
        :param query_string: The query_string of this SamplesResponse.  # noqa: E501
        :type query_string: str
        """
        self.swagger_types = {
            'data': List[Samples],
            'query_string': str
        }

        self.attribute_map = {
            'data': 'data',
            'query_string': 'query_string'
        }
        self._data = data
        self._query_string = query_string

    @classmethod
    def from_dict(cls, dikt) -> 'SamplesResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SamplesResponse of this SamplesResponse.  # noqa: E501
        :rtype: SamplesResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> List[Samples]:
        """Gets the data of this SamplesResponse.


        :return: The data of this SamplesResponse.
        :rtype: List[Samples]
        """
        return self._data

    @data.setter
    def data(self, data: List[Samples]):
        """Sets the data of this SamplesResponse.


        :param data: The data of this SamplesResponse.
        :type data: List[Samples]
        """

        self._data = data

    @property
    def query_string(self) -> str:
        """Gets the query_string of this SamplesResponse.


        :return: The query_string of this SamplesResponse.
        :rtype: str
        """
        return self._query_string

    @query_string.setter
    def query_string(self, query_string: str):
        """Sets the query_string of this SamplesResponse.


        :param query_string: The query_string of this SamplesResponse.
        :type query_string: str
        """

        self._query_string = query_string
