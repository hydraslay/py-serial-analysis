# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.fit_request import FitRequest  # noqa: E501
from swagger_server.models.fits_response import FitsResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFitController(BaseTestCase):
    """FitController integration test stubs"""

    def test_get_fits(self):
        """Test case for get_fits

        get fit status
        """
        response = self.client.open(
            '/fit',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_fit(self):
        """Test case for set_fit

        begin or cancel a fit process
        """
        body = FitRequest()
        response = self.client.open(
            '/fit',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
