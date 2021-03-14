# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.model import Model  # noqa: F401,E501
from swagger_server import util


class ModelListResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, data: List[Model]=None, query_string: str=None):  # noqa: E501
        """ModelListResponse - a model defined in Swagger

        :param data: The data of this ModelListResponse.  # noqa: E501
        :type data: List[Model]
        :param query_string: The query_string of this ModelListResponse.  # noqa: E501
        :type query_string: str
        """
        self.swagger_types = {
            'data': List[Model],
            'query_string': str
        }

        self.attribute_map = {
            'data': 'data',
            'query_string': 'query_string'
        }
        self._data = data
        self._query_string = query_string

    @classmethod
    def from_dict(cls, dikt) -> 'ModelListResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ModelListResponse of this ModelListResponse.  # noqa: E501
        :rtype: ModelListResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> List[Model]:
        """Gets the data of this ModelListResponse.


        :return: The data of this ModelListResponse.
        :rtype: List[Model]
        """
        return self._data

    @data.setter
    def data(self, data: List[Model]):
        """Sets the data of this ModelListResponse.


        :param data: The data of this ModelListResponse.
        :type data: List[Model]
        """

        self._data = data

    @property
    def query_string(self) -> str:
        """Gets the query_string of this ModelListResponse.


        :return: The query_string of this ModelListResponse.
        :rtype: str
        """
        return self._query_string

    @query_string.setter
    def query_string(self, query_string: str):
        """Sets the query_string of this ModelListResponse.


        :param query_string: The query_string of this ModelListResponse.
        :type query_string: str
        """

        self._query_string = query_string
