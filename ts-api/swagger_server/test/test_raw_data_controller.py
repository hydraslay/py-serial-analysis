# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.raw_data import RawData  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRawDataController(BaseTestCase):
    """RawDataController integration test stubs"""

    def test_get_raw_data(self):
        """Test case for get_raw_data

        get RawData
        """
        response = self.client.open(
            '/raw',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
