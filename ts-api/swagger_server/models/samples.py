# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.raw_data import RawData  # noqa: F401,E501
from swagger_server import util


class Samples(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, uid: str=None, sample_data: List[RawData]=None, value: float=None):  # noqa: E501
        """Samples - a model defined in Swagger

        :param uid: The uid of this Samples.  # noqa: E501
        :type uid: str
        :param sample_data: The sample_data of this Samples.  # noqa: E501
        :type sample_data: List[RawData]
        :param value: The value of this Samples.  # noqa: E501
        :type value: float
        """
        self.swagger_types = {
            'uid': str,
            'sample_data': List[RawData],
            'value': float
        }

        self.attribute_map = {
            'uid': 'uid',
            'sample_data': 'sample_data',
            'value': 'value'
        }
        self._uid = uid
        self._sample_data = sample_data
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'Samples':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Samples of this Samples.  # noqa: E501
        :rtype: Samples
        """
        return util.deserialize_model(dikt, cls)

    @property
    def uid(self) -> str:
        """Gets the uid of this Samples.


        :return: The uid of this Samples.
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid: str):
        """Sets the uid of this Samples.


        :param uid: The uid of this Samples.
        :type uid: str
        """

        self._uid = uid

    @property
    def sample_data(self) -> List[RawData]:
        """Gets the sample_data of this Samples.


        :return: The sample_data of this Samples.
        :rtype: List[RawData]
        """
        return self._sample_data

    @sample_data.setter
    def sample_data(self, sample_data: List[RawData]):
        """Sets the sample_data of this Samples.


        :param sample_data: The sample_data of this Samples.
        :type sample_data: List[RawData]
        """

        self._sample_data = sample_data

    @property
    def value(self) -> float:
        """Gets the value of this Samples.


        :return: The value of this Samples.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value: float):
        """Sets the value of this Samples.


        :param value: The value of this Samples.
        :type value: float
        """

        self._value = value
