# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.samples import Samples  # noqa: E501
from swagger_server.models.samples_response import SamplesResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSampleController(BaseTestCase):
    """SampleController integration test stubs"""

    def test_get_samples(self):
        """Test case for get_samples

        get Sample list
        """
        response = self.client.open(
            '/samples',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_sample_and_value_data(self):
        """Test case for set_sample_and_value_data

        add or update sample
        """
        body = [Samples()]
        response = self.client.open(
            '/samples',
            method='POST',
            data=json.dumps(body),
            content_type='*/*')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
