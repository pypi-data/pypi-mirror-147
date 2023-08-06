import requests, json, time
from .rest import RestURL


def craft_error_message(resp, url):
    code = resp.status_code

    if code in [404]:
        raise Exception("Server Error: " + str(code), resp.text, " URL: ", str(url))

    if code in [503, 500]:
        raise Exception("Server Error: " + str(code), " URL: ", str(url))

    if code == 401:
        raise Exception("Server returned 401: Unauthorized. Please check username or password.")

    json_data = resp.json()
    error_message = json_data["error"] + "--" + json_data["error_description"]
    raise Exception("Error: " + str(code) + " \n for URL:" + str(url) + " \n Response: " + error_message)


def elapsed_time(time2):
    return (time.time() - time2)

class Token:
    def __init__(self, payload=None, well_known=None):

        self.token = payload['access_token']
        self.refresh_token = payload['refresh_token']
        self.expiring = int(payload['expires_in'])
        self.well_known = well_known
        self.start_time = time.time()
        self.payload = payload

    def expired(self):
        if elapsed_time(self.start_time) >= (self.expiring - 10): # If current time is above expiring time minus 10 seconds we ask for a new token.
            return True

        return False


    def refresh(self):
        token_endpoint = self.well_known['token_endpoint']

        body = {
            "client_id": "admin-cli",
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        resp = requests.post(token_endpoint, data=body)

        if resp.status_code != 200:
            craft_error_message(resp, token_endpoint)

        return Token(payload=resp.json(), well_known=self.well_known)

    def __str__(self):
        return str(self.payload)

    def __repr__(self):
        return str(self.payload)

class OpenID:
    def __check_params(self, params):
        expected_params = ['password', 'username', 'grant_type', 'client_id']

        for param in expected_params:
            if param not in params:
                raise Exception("Missing parameter on OpenId class: ", param)


    # Retrieves the Well Known Endpoint: https://openid.net/specs/openid-connect-discovery-1_0.html
    @staticmethod
    def discover(url, realm):
        discovery_url = RestURL(url, ['auth', 'realms', realm, '.well-known', 'openid-configuration'])

        resp = requests.get(url=str(discovery_url))

        if resp.status_code == 200:
            return resp.json()

        OpenID.validate_http_response(resp, discovery_url)

    def __init__(self, credentials, url=None):
        self.__check_params(credentials)

        self.credentials = credentials
        self.realm = self.credentials['realm']
        self.token = None
        self.urlObject = None

        if url:
            self.urlObject = url

    @staticmethod
    def createAdminClient(username, password):
        __props = {
            "client_id": "admin-cli",
            "grant_type": "password",
            "realm": "master",
            "username": username,
            "password": password
        }

        return OpenID(__props)

    def getToken(self, target_url=None):
        if not target_url and not self.urlObject:
            raise Exception('URL Not Found: Make sure you provide a URL before invoking the service')

        url = target_url if target_url else self.urlObject
        well_known = OpenID.discover(url, self.realm)
        resp = requests.post(well_known['token_endpoint'], data=self.credentials)

        if resp.status_code == 200:
            payload = resp.json()
            self.token = Token(payload=payload,  well_known=well_known)
            return self.token
        else:
            craft_error_message(resp, url)
