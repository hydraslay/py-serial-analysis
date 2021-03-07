# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class FitRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: float=None, data_set: float=None):  # noqa: E501
        """FitRequest - a model defined in Swagger

        :param id: The id of this FitRequest.  # noqa: E501
        :type id: float
        :param data_set: The data_set of this FitRequest.  # noqa: E501
        :type data_set: float
        """
        self.swagger_types = {
            'id': float,
            'data_set': float
        }

        self.attribute_map = {
            'id': 'id',
            'data_set': 'data_set'
        }
        self._id = id
        self._data_set = data_set

    @classmethod
    def from_dict(cls, dikt) -> 'FitRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FitRequest of this FitRequest.  # noqa: E501
        :rtype: FitRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> float:
        """Gets the id of this FitRequest.


        :return: The id of this FitRequest.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id: float):
        """Sets the id of this FitRequest.


        :param id: The id of this FitRequest.
        :type id: float
        """

        self._id = id

    @property
    def data_set(self) -> float:
        """Gets the data_set of this FitRequest.


        :return: The data_set of this FitRequest.
        :rtype: float
        """
        return self._data_set

    @data_set.setter
    def data_set(self, data_set: float):
        """Sets the data_set of this FitRequest.


        :param data_set: The data_set of this FitRequest.
        :type data_set: float
        """

        self._data_set = data_set