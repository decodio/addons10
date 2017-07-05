import werkzeug
from openerp import http
from openerp.http import request
from openerp.modules.module import get_module_path
from openerp.modules.registry import RegistryManager
from openerp import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


class office_365_auth(http.Controller):

    @http.route('/web_outlook_plugin/Manifest/Manifest.xml', type='http', auth="none")
    def Manifest(self):
        mimetype = 'application/xml;charset=utf-8'
        mod_path = get_module_path('web_outlook_plugin')
        path = mod_path + '/static/src/xml/outlook_plugin-manifest.xml'
        contents = open(path).read()

        # replace URL in XML template with current base url
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        base_url = base_url.replace("http://", "")
        base_url = base_url.replace("https://", "")
        content = contents.replace("localhost:8443", base_url)
        return request.make_response(content, [('Content-Type', mimetype)])

    @http.route('/web_outlook_plugin/<db>/Manifest.xml', type='http', auth="none")
    def Manifest(self, req, db, **kw):
        mimetype = 'application/xml;charset=utf-8'
        registry = RegistryManager.get(db)
        with registry.cursor() as cr:
            irc_obj = registry.get('ir.config_parameter')
            mod_path = get_module_path('web_outlook_plugin')
            path = mod_path + '/static/src/xml/outlook_plugin-manifest.xml'
            contents = open(path).read()
            # replace URL in XML template with current base url
            base_url = irc_obj.get_param(cr, SUPERUSER_ID, 'web.base.url')
            _logger.info("base_url: db:%s, url:%s",  db, base_url)
            base_url = base_url.replace("http://", "")
            base_url = base_url.replace("https://", "")
            content = contents.replace("localhost:8443", base_url)
            content = content.replace("<db>", db)
        return request.make_response(content, [('Content-Type', mimetype)])


        # def check_email(self, req, db):
        #     context = {}
        #     email = req.jsonrequest.get('email')
        #     if not email:
        #         return {"status": -1}
        #
        #     registry = RegistryManager.get(db)
        #
        #     with registry.cursor() as cr:
        #         try:
        #             p = registry.get('res.partner')
        #             p_id = p.search(cr, openerp.SUPERUSER_ID, [('email', '=', email)])
        #             if len(p_id) == 0:  # email not found
        #                 return {"status": 0}
        #             else:
        #                 return {"status": 1}
        #         except Exception, e:
        #             return {"status": -1}
        #
        #     return {"status": -1}
