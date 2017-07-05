import werkzeug
from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo.exceptions import AccessDenied
# from odoo.addons.web_oauth_o365.models.auth_oauth import _list_providers
from odoo.addons.auth_oauth.controllers.main import OAuthLogin
import logging
_logger = logging.getLogger(__name__)


class office_365_auth(http.Controller):
    def get_state(self, provider):
        redirect = request.params.get('redirect') or 'web'

        # TODO # replace protocol part of URL with base url protocol
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        base_url_root = base_url.split(':')[0]

        if not redirect.startswith(('//', 'http://', 'https://')):
            redirect = '%s%s' % (request.httprequest.url_root, redirect[1:] if redirect[0] == '/' else redirect)
        state = dict(
            d=request.session.db,
            p=provider['id'],
            r=werkzeug.url_quote_plus(redirect),
        )
        token = request.params.get('token')
        if token:
            state['t'] = token
        return state

    @http.route('/web_outlook_plugin/<db>/Home.html', type='http', auth="none")
    def Home(self, db, **kw):
        # registry = RegistryManager.get(db)
        # with registry.cursor() as cr:
        #     irc_obj = registry.get('ir.config_parameter')
        return request.render('web_outlook_plugin.outlook_home_view', {})

    @http.route('/web_outlook_plugin/<db>/login', type='http', auth="none")
    def office_365_auth_web_login(self, db, redirect=None, **kw):
        if db and db not in http.db_filter([db]):
            db = None
            # TODO HANDLE THIS!!
        request.session.db = db
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = SUPERUSER_ID  # TODO: Security issue?
        values = request.params.copy()
        if not redirect:
            redirect = '/web?' + request.httprequest.query_string
        values['redirect'] = redirect
        values['db'] = db
        try:
            values['databases'] = http.db_list()
        except AccessDenied:
            values['databases'] = None

        providers = OAuthLogin.list_providers(self)
        values['providers'] = providers

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(
                request.session.db,
                request.params['login'],
                request.params['password'])
            if uid is not False:
                s_redirect = "/web_outlook_plugin/%s/TaskPane.html" % db
                return http.redirect_with_hash(s_redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
        if request.env.ref('web.ologin', False):
            return request.render('web.ologin', values)
        else:
            return request.render('web.ologin', values)
            # probably not an odoo compatible database
            error = 'Unable to login on database %s' % request.session.db
            return werkzeug.utils.redirect('/web/database/selector?error=%s' % error, 303)

    @http.route('/web_outlook_plugin/<db>/selectlead', type='http', auth="user")
    def selectlead(self, db, **kw):
        if not request.uid:
            return werkzeug.utils.redirect('/web_outlook_plugin/%s/login' % db)
        _logger.info(
            'selectlead: db:%s, method: %s, uid:%s',
            request.session.db, request.httprequest.method, request.uid)
        return werkzeug.utils.redirect('/web/database/selector?error=%s' % "xxxx", 303)

    @http.route('/web_outlook_plugin/<db>/sendmessage', type='http', auth="user")
    def sendmessage(self, db, body, redirect=None, **kw):
        _logger.info("web_login: db:%s, body:%s", db, body)
