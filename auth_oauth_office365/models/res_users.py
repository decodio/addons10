# -*- coding: utf-8 -*-
import logging
import ast
import base64

from odoo.exceptions import AccessDenied
from odoo import models, fields

_logger = logging.getLogger(__name__)

class res_users(models.Model):
    _inherit = 'res.users'

    def _auth_oauth_validate365(self, provider, id_token):
        """ return the validation data corresponding to the access token """
        oauth_provider = self.env['auth.oauth.provider'].browse(provider)
        validation = {}

        if id_token:
            segments = id_token.split('.')
            if (len(segments) != 3):
                raise Exception('Wrong number of segments in token: %s' % id_token)

            # extract email (/username) from id_token
            b64string = segments[1]
            b64string = b64string.encode('ascii')
            padded = b64string + '=' * (4 - len(b64string) % 4)
            padded = base64.urlsafe_b64decode(padded)
            vd = ast.literal_eval(padded)
            _u = {'user_id': vd['email']}

            # TODO insert something else since we don't get access_token?
            _v = {'access_token': vd['email']}
            _aud = vd['aud']

            # check appid vs provider client_id
            # TODO insert additional checks?
            if oauth_provider.client_id == _aud:
                validation.update(_u)
                validation.update(_v)

        return validation


    def auth_oauth(self, provider, params):
        # Advice by Google (to avoid Confused Deputy Problem)
        # if validation.audience != OUR_CLIENT_ID:
        #   abort()
        # else:
        #   continue with the process
        access_token = params.get('code')

        oauth_provider = self.env['auth.oauth.provider'].browse(provider)
        o365auth_provider_id = self.env.ref('auth_oauth_office365.provider_office365').id

        # extract data from 'id_token' for Office 365
        if oauth_provider.id == o365auth_provider_id:
            id_token = params.get('id_token', False)
            validation = self._auth_oauth_validate365(provider, id_token)
        else:
            validation = self._auth_oauth_validate(provider, access_token)

        # required check
        if not validation.get('user_id'):
            # Workaround: facebook does not send 'user_id' in Open Graph Api
            if validation.get('id'):
                validation['user_id'] = validation['id']
            else:
                raise AccessDenied()

        if not params.get('access_token', False):
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
