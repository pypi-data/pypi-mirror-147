import unittest, time
from kcapi import OpenID, Keycloak
from .testbed import TestBed 

WRONG_URL =  'https://sso-wrong-cvaldezr-stage.apps.sandbox-m2.ll9k.p1.openshiftapps.com'


def test_kc(that, kc):
    adm = kc.admin()
    realms = adm.all()
    that.assertTrue(len(realms) > 0, "We should get some realms from the server.")

    kc_resource= kc.build('clients', 'master')
    clients = kc_resource.all()
    that.assertTrue(len(clients) > 0, "We should get some clients from the server.")

    poly_roles = kc.build('roles', 'master')
    roles = poly_roles.all()
    that.assertTrue(len(roles) > 0, "We should get some roles from the server.")

class Testing_OpenID(unittest.TestCase):
    def test_oidc_ctor(self): 
        try:
            OpenID({"client_id":"admin-cli"}, WRONG_URL)
        except Exception as E:
            self.assertEqual("password" in str(E), True)

        try:
            OpenID({"client_id":"admin-cli", "realm": "my_realm", "password": "xxx"}, WRONG_URL)
        except Exception as E:
            self.assertEqual("username" in str(E), True)

        self.assertRaises(Exception, lambda: OpenID({"client_id":"admin-cli"})) 

    def test_oidc_login_on_wrong_url(self):
        oid_client = OpenID({
            "client_id": "admin-cli",
            "username": "6OPtWY33", 
            "password":"I6gglTeDLlmmpLYoAAUMcFQqNOMjw5dA", 
            "grant_type":"password",
            "realm" : "master"
            }, WRONG_URL)
        
        self.assertRaises(Exception, lambda: oid_client.getToken()) 

    def test_oidc_login_on_wrong_password(self):
        oid_client = OpenID({
            "client_id": "admin-cli",
            "username": "6OPtWY33", 
            "password":"I6gglTeDLlmmpLYoAAUMcFQqNOMjw5dA", 
            "grant_type":"password",
            "realm" : "master"
            }, self.ENDPOINT)

        try:
            oid_client.getToken()
        except Exception as E:
            self.assertEqual("Unauthorized" in str(E), True)


    def test_oidc_login(self):
        oid_client = OpenID({
            "client_id": "admin-cli",
            "username": self.testbed.USER, 
            "password": self.testbed.PASSWORD, 
            "grant_type":"password",
            "realm" : "master"
            }, self.ENDPOINT)

        token = oid_client.getToken()

        self.assertIsNotNone(token)
        self.assertTrue(len(str(token)) > 0)


    def testing_admin_instantiation(self):
        oid_client = OpenID({
            "client_id": "admin-cli",
            "username": self.testbed.USER,
            "password": self.testbed.PASSWORD,
            "grant_type": "password",
            "realm": "master"
        }, self.ENDPOINT)

        token = oid_client.getToken()
        kc = Keycloak(token, self.ENDPOINT)

        test_kc(self, kc)


    def testing_admin_instantiation_with_token_refresh(self):
        oid_client = OpenID({
            "client_id": "admin-cli",
            "username": self.testbed.USER,
            "password": self.testbed.PASSWORD,
            "grant_type": "password",
            "realm": "master"
        }, self.ENDPOINT)

        token = oid_client.getToken()

        new_kc = Keycloak.instantiate_with_refresh_token(refresh_token=str(token.refresh_token), url=self.ENDPOINT)
        test_kc(self, new_kc)


    def testing_admin_instantiation_with_string_request(self):
        oid_client = OpenID({
            "client_id": "admin-cli",
            "username": self.testbed.USER,
            "password": self.testbed.PASSWORD,
            "grant_type": "password",
            "realm": "master"
        }, self.ENDPOINT)

        token = oid_client.getToken()

        json_kc = Keycloak.instantiate_with_raw_json(json_string=str(token), url=self.ENDPOINT)
        test_kc(self, json_kc)



    @classmethod
    def setUpClass(self):
        self.testbed = TestBed()
        self.kc = self.testbed.getKeycloak()
        self.realm = self.testbed.REALM 
        self.master_realm = self.testbed.getAdminRealm()
        self.ENDPOINT = self.testbed.ENDPOINT
        self.USER = self.testbed.USER
        self.PASSWORD = self.testbed.PASSWORD

if __name__ == '__main__':
    unittest.main()
