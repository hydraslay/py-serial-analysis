# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Model(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, model: str=None, description: str=None, params: str=None):  # noqa: E501
        """Model - a model defined in Swagger

        :param model: The model of this Model.  # noqa: E501
        :type model: str
        :param description: The description of this Model.  # noqa: E501
        :type description: str
        :param params: The params of this Model.  # noqa: E501
        :type params: str
        """
        self.swagger_types = {
            'model': str,
            'description': str,
            'params': str
        }

        self.attribute_map = {
            'model': 'model',
            'description': 'description',
            'params': 'params'
        }
        self._model = model
        self._description = description
        self._params = params

    @classmethod
    def from_dict(cls, dikt) -> 'Model':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Model of this Model.  # noqa: E501
        :rtype: Model
        """
        return util.deserialize_model(dikt, cls)

    @property
    def model(self) -> str:
        """Gets the model of this Model.


        :return: The model of this Model.
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model: str):
        """Sets the model of this Model.


        :param model: The model of this Model.
        :type model: str
        """

        self._model = model

    @property
    def description(self) -> str:
        """Gets the description of this Model.


        :return: The description of this Model.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this Model.


        :param description: The description of this Model.
        :type description: str
        """

        self._description = description

    @property
    def params(self) -> str:
        """Gets the params of this Model.


        :return: The params of this Model.
        :rtype: str
        """
        return self._params

    @params.setter
    def params(self, params: str):
        """Sets the params of this Model.


        :param params: The params of this Model.
        :type params: str
        """

        self._params = params
