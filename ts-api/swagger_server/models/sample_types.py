# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class SampleTypes(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, type: str=None, description: str=None):  # noqa: E501
        """SampleTypes - a model defined in Swagger

        :param type: The type of this SampleTypes.  # noqa: E501
        :type type: str
        :param description: The description of this SampleTypes.  # noqa: E501
        :type description: str
        """
        self.swagger_types = {
            'type': str,
            'description': str
        }

        self.attribute_map = {
            'type': 'type',
            'description': 'description'
        }
        self._type = type
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'SampleTypes':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SampleTypes of this SampleTypes.  # noqa: E501
        :rtype: SampleTypes
        """
        return util.deserialize_model(dikt, cls)

    @property
    def type(self) -> str:
        """Gets the type of this SampleTypes.


        :return: The type of this SampleTypes.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this SampleTypes.


        :param type: The type of this SampleTypes.
        :type type: str
        """

        self._type = type

    @property
    def description(self) -> str:
        """Gets the description of this SampleTypes.


        :return: The description of this SampleTypes.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this SampleTypes.


        :param description: The description of this SampleTypes.
        :type description: str
        """

        self._description = description
