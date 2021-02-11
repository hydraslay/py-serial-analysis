# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.model import Model  # noqa: E501
from swagger_server.models.sample_types import SampleTypes  # noqa: E501
from swagger_server.test import BaseTestCase


class TestModelController(BaseTestCase):
    """ModelController integration test stubs"""

    def test_get_models(self):
        """Test case for get_models

        get Model list
        """
        response = self.client.open(
            '/models',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_sample_types(self):
        """Test case for get_sample_types

        get sample type list
        """
        response = self.client.open(
            '/sample_types',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_model(self):
        """Test case for set_model

        add or update Model
        """
        body = Model()
        response = self.client.open(
            '/models',
            method='POST',
            data=json.dumps(body),
            content_type='*/*')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
