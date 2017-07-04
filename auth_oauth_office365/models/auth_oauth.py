# -*- coding: utf-8 -*-
from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.http import request
import simplejson
import werkzeug.utils
import uuid

def _list_providers(self):
    try:
        providers = request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
    except Exception:
        providers = []
    o365auth_provider_id = request.env.ref('auth_oauth_office365.provider_office365').id

    for provider in providers:
        return_url = request.httprequest.url_root + 'auth_oauth/signin'
        state = self.get_state(provider)

        _response_type = 'token'

        # use 'id_token' for Office 365
        if provider['id'] == o365auth_provider_id:
            _response_type = 'id_token'

        params = dict(
            response_type=_response_type,
            client_id=provider['client_id'],
            redirect_uri=return_url,
            scope=provider['scope'],
            state=simplejson.dumps(state),
        )

        # must provide 'nonce' value
        if provider['id'] == o365auth_provider_id:
            params['nonce'] = str(uuid.uuid4())

        provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'], werkzeug.url_encode(params))
    return providers

OAuthLogin.list_providers = _list_providers


