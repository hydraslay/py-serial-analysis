# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.data_set import DataSet  # noqa: F401,E501
from swagger_server import util


class DataSetResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, data: List[DataSet]=None, query_string: str=None):  # noqa: E501
        """DataSetResponse - a model defined in Swagger

        :param data: The data of this DataSetResponse.  # noqa: E501
        :type data: List[DataSet]
        :param query_string: The query_string of this DataSetResponse.  # noqa: E501
        :type query_string: str
        """
        self.swagger_types = {
            'data': List[DataSet],
            'query_string': str
        }

        self.attribute_map = {
            'data': 'data',
            'query_string': 'query_string'
        }
        self._data = data
        self._query_string = query_string

    @classmethod
    def from_dict(cls, dikt) -> 'DataSetResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DataSetResponse of this DataSetResponse.  # noqa: E501
        :rtype: DataSetResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> List[DataSet]:
        """Gets the data of this DataSetResponse.


        :return: The data of this DataSetResponse.
        :rtype: List[DataSet]
        """
        return self._data

    @data.setter
    def data(self, data: List[DataSet]):
        """Sets the data of this DataSetResponse.


        :param data: The data of this DataSetResponse.
        :type data: List[DataSet]
        """

        self._data = data

    @property
    def query_string(self) -> str:
        """Gets the query_string of this DataSetResponse.


        :return: The query_string of this DataSetResponse.
        :rtype: str
        """
        return self._query_string

    @query_string.setter
    def query_string(self, query_string: str):
        """Sets the query_string of this DataSetResponse.


        :param query_string: The query_string of this DataSetResponse.
        :type query_string: str
        """

        self._query_string = query_string
