# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class DataSet(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: float=None, name: str=None, uid_from: str=None, uid_to: str=None, count: float=None):  # noqa: E501
        """DataSet - a model defined in Swagger

        :param id: The id of this DataSet.  # noqa: E501
        :type id: float
        :param name: The name of this DataSet.  # noqa: E501
        :type name: str
        :param uid_from: The uid_from of this DataSet.  # noqa: E501
        :type uid_from: str
        :param uid_to: The uid_to of this DataSet.  # noqa: E501
        :type uid_to: str
        :param count: The count of this DataSet.  # noqa: E501
        :type count: float
        """
        self.swagger_types = {
            'id': float,
            'name': str,
            'uid_from': str,
            'uid_to': str,
            'count': float
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'uid_from': 'uid_from',
            'uid_to': 'uid_to',
            'count': 'count'
        }
        self._id = id
        self._name = name
        self._uid_from = uid_from
        self._uid_to = uid_to
        self._count = count

    @classmethod
    def from_dict(cls, dikt) -> 'DataSet':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DataSet of this DataSet.  # noqa: E501
        :rtype: DataSet
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> float:
        """Gets the id of this DataSet.


        :return: The id of this DataSet.
        :rtype: float
        """
        return self._id

    @id.setter
    def id(self, id: float):
        """Sets the id of this DataSet.


        :param id: The id of this DataSet.
        :type id: float
        """

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this DataSet.


        :return: The name of this DataSet.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this DataSet.


        :param name: The name of this DataSet.
        :type name: str
        """

        self._name = name

    @property
    def uid_from(self) -> str:
        """Gets the uid_from of this DataSet.


        :return: The uid_from of this DataSet.
        :rtype: str
        """
        return self._uid_from

    @uid_from.setter
    def uid_from(self, uid_from: str):
        """Sets the uid_from of this DataSet.


        :param uid_from: The uid_from of this DataSet.
        :type uid_from: str
        """

        self._uid_from = uid_from

    @property
    def uid_to(self) -> str:
        """Gets the uid_to of this DataSet.


        :return: The uid_to of this DataSet.
        :rtype: str
        """
        return self._uid_to

    @uid_to.setter
    def uid_to(self, uid_to: str):
        """Sets the uid_to of this DataSet.


        :param uid_to: The uid_to of this DataSet.
        :type uid_to: str
        """

        self._uid_to = uid_to

    @property
    def count(self) -> float:
        """Gets the count of this DataSet.


        :return: The count of this DataSet.
        :rtype: float
        """
        return self._count

    @count.setter
    def count(self, count: float):
        """Sets the count of this DataSet.


        :param count: The count of this DataSet.
        :type count: float
        """

        self._count = count
