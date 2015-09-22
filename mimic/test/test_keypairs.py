"""
Tests for :mod:`nova_api` and :mod:`nova_objects`.
"""
from IPython import embed

from twisted.trial.unittest import SynchronousTestCase

from mimic.test.helpers import json_request, request
from mimic.rest.nova_api import NovaApi, NovaControlApi
from mimic.test.fixtures import APIMockHelper


class KeyPairTests(SynchronousTestCase):
    """
    Tests for keypairs
    """

    def setUp(self):
        """
        Create a :obj:`MimicCore` with :obj:`NovaApi` as the only plugin
        """
        nova_api = NovaApi(["ORD", "MIMIC"])
        self.helper = APIMockHelper(
            self, [nova_api, NovaControlApi(nova_api=nova_api)]
        )
        self.root = self.helper.root
        self.clock = self.helper.clock
        self.uri = self.helper.uri
        self.create_keypair_response, self.create_keypair_response_body = (
            self.create_keypair())
        self.keypair_name = self.create_keypair_response_body[
            'keypair']['name']

    def create_keypair(self, kp_body=None):
        if kp_body is None:
                kp_body = {
                    "keypair": {
                        "name": "setUP_test_lp",
                        "public_key": "ssh-rsa testkey/"
                    }
                }

        resp, body = self.successResultOf(json_request(
            self, self.helper.root, "POST", self.helper.uri + '/os-keypairs',
            kp_body
        ))
        return resp, body

    def get_keypairs_list(self):
        resp, body = self.successResultOf(json_request(
            self, self.helper.root, "GET", self.helper.uri + '/os-keypairs'
        ))
        return resp, body

    def test_create_keypair(self):
        kp_test_body = {
            "keypair": {
                "name": "test_lp",
                "public_key": "ssh-rsa testkey/"
            }
        }
        resp, body = self.create_keypair(kp_test_body)

        self.assertEqual(resp.code, 200)
        self.assertEqual(body['keypair']['name'], kp_test_body['keypair']['name'])

    def test_list_keypair(self):
        resp, body = self.get_keypairs_list()
        self.assertEqual(resp.code, 200)
        # embed()
        # self.assertEqual(len(body["u'keypairs"]), 1)

    def test_delete_keypair(self):
        resp = self.successResultOf(request(
            self, self.helper.root, "DELETE", self.helper.uri +
            '/os-keypairs/' + self.keypair_name
        ))

        self.assertEqual(resp.code, 202)
        # assert server is gone
