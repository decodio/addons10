import werkzeug
from odoo import api
from odoo import http
from odoo.http import request
from odoo.modules.module import get_module_path
from odoo.modules.registry import RegistryManager
from odoo import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


class office_365_auth(http.Controller):

    @http.route('/web_outlook_plugin/<db>/Manifest.xml', type='http', auth="none")
    def Manifest(self, req, db, **kw):
        mimetype = 'application/xml;charset=utf-8'
        registry = RegistryManager.get(db)


        cr = registry.cursor()
        with api.Environment.manage():
            env = api.Environment(cr, SUPERUSER_ID, {})

            mod_path = get_module_path('web_outlook_plugin')
            path = mod_path + '/static/src/xml/outlook_plugin-manifest.xml'
            contents = open(path).read()

            contents = contents.decode('utf-8')

            # replace URL in XML template with current base url
            base_url = env['ir.config_parameter'].get_param('web.base.url')
            _logger.info("base_url: db:%s, url:%s",  db, base_url)
            base_url = base_url.replace("http://", "")
            base_url = base_url.replace("https://", "")
            print "contents"
            print contents
            content = contents.replace("localhost:8443", base_url)
            content = content.replace("<db>", db)
        return request.make_response(content, [('Content-Type', mimetype)])

