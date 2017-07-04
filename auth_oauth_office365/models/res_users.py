import logging
import werkzeug.urls
import simplejson
import requests
import ast
import base64

from odoo.http import request
from odoo.exceptions import AccessDenied
from odoo import models, fields

_logger = logging.getLogger(__name__)

class res_users(models.Model):
    _inherit = 'res.users'

    def _auth_oauth_o365_rpc(self, endpoint, access_token, client_id, client_secret, state, context=None):
        url = endpoint
        redirect_uri = request.httprequest.url_root + 'auth_oauth/signin'

        params = {'code': access_token, 'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'authorization_code', 'redirect_uri': redirect_uri, 'state': state}
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = werkzeug.url_encode(params)
        response = requests.post(url, headers=headers, data=data)
        return simplejson.loads(response.text)


    def _auth_oauth_validate365(self, provider, access_token, client_id, client_secret, state):
        """ return the validation data corresponding to the access token """
        oauth_provider = self.env['auth.oauth.provider'].browse(provider)

        validation = self._auth_oauth_o365_rpc(oauth_provider.validation_endpoint, access_token, client_id, client_secret, state)

        if validation.get("error"):
            raise Exception(validation['error'])
        if oauth_provider.data_endpoint:
            data = self._auth_oauth_rpc(oauth_provider.data_endpoint, access_token)
            validation.update(data)
        return validation


    def auth_oauth(self, provider, params):
        # Advice by Google (to avoid Confused Deputy Problem)
        # if validation.audience != OUR_CLIENT_ID:
        #   abort()
        # else:
        #   continue with the process
        access_token = params.get('code')
        state = params.get('state')

        oauth_provider = self.env['auth.oauth.provider'].browse(provider)
        o365auth_provider_id = self.env.ref('auth_oauth_office365.provider_office365').id

        if oauth_provider.id == o365auth_provider_id:
            validation = self._auth_oauth_validate365(provider, access_token, oauth_provider.client_id, oauth_provider.client_secret, state)
        else:
            validation = self._auth_oauth_validate(provider, access_token)

        # required check
        if not validation.get('user_id'):
            # Workaround: facebook does not send 'user_id' in Open Graph Api
            if validation.get('id'):
                validation['user_id'] = validation['id']
            else:
                id_token = validation.get('id_token', False)
                if id_token:
                    segments = validation['id_token'].split('.')
                    if (len(segments) != 3):
                        raise Exception('Wrong number of segments in token: %s' % id_token)

                    # extract email (/username) from id_token
                    b64string = segments[1]
                    b64string = b64string.encode('ascii')
                    padded = b64string + '=' * (4 - len(b64string) % 4)
                    padded = base64.urlsafe_b64decode(padded)
                    vd = ast.literal_eval(padded)
                    _u = {'user_id': vd['email']}
                    validation.update(_u)
                else:
                    raise AccessDenied()

        # move access token to params
        access_token = validation.get('access_token')
        if access_token:
            params['access_token'] = access_token

        # retrieve and sign in user
        login = self._auth_oauth_signin(provider, validation, params)
        if not login:
            raise AccessDenied()
        # return user credentials
        return (self.env.cr.dbname, login, access_token)
