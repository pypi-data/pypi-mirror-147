from .crud import KeycloakCRUD
from .targets import Targets
from .groups import Groups
from .roles import RolesURLBuilder
from .users import Users
from .realms import Realms, RealmURLBuilder
from .url import RestURL
from .idp import IdentityProviderURLBuilder
from .auth_flows import AuthenticationFlows, AuthenticationFlowURLBuilder
from .clients import Clients

KCResourceTypes = {
    "users": Users,
    "groups": Groups,
    "realms": Realms,
    "authentication": AuthenticationFlows,
    "clients": Clients
}

URLBuilders = {
    'roles': RolesURLBuilder,
    'authentication': AuthenticationFlowURLBuilder,
    "idp": IdentityProviderURLBuilder,
    "identity-provider": IdentityProviderURLBuilder,
    "realms": RealmURLBuilder,
}


def GenericURLBuilder(url):
    targets = Targets.makeWithURL(url)
    return targets


class KCResourceBuilder:

    def __init__(self, keycloakURL):
        self.resource_name = None
        self.realm = None
        self.url = RestURL(url=keycloakURL, resources=["auth", "admin", "realms"])

    def withName(self, name):
        self.resource_name = name
        return self

    def forRealm(self, realm):
        self.realm = realm
        return self

    def build(self, token):
        KCResourceAPI = KeycloakCRUD if not self.resource_name in KCResourceTypes else KCResourceTypes[self.resource_name]
        URLBuilder = GenericURLBuilder if not self.resource_name in URLBuilders else URLBuilders[self.resource_name]

        self.url.addResources([self.realm, self.resource_name])

        resource = KCResourceAPI()
        resource.targets = URLBuilder(str(self.url))
        resource.token = token

        return resource
