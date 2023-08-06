from httpie.plugins import AuthPlugin
from dataclasses import dataclass
import os
import configparser
import requests.auth
import requests.PreparedRequest

__version__ = '0.0.1'
__author__ = 'Ryan McCarter'
__licence__ = 'Apache 2.0'

class HttpSignatureAuthPlugin(AuthPlugin):

    name = 'Http Signature Authenticaiton'
    auth_type = 'signature'
    auth_require = False
    auth_parse = False
    prompt_password = False
    description = ''

    def get_auth(self, username: str = None, password: str = None):

        rc_path = os.path.expanduser("~/.httpsigrc")
        config = configparser.RawConfigParser()
        config.read(rc_path)
            
        rc = dict(config.items("apitest.cybersource.com"))

        key=rc.get('key')
        secret=rc.get('secret')
        algorith=rc.get('algorithm')
        headers=rc.get('headers')

        return HttpSignatureAuth(HttpSigRc(key, secret, algorith, headers))

@dataclass
class HttpSigRc:
    key: str
    secret: str
    algorith: str
    headers: str

class HttpSignatureAuth(requests.auth.AuthBase):
    def __init__(self, httpSigRc: HttpSigRc):
        self.httpSigRc = httpSigRc

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        


        request.headers['test'] = f'Test {self.httpSigRc.key}'
        return request
