import werkzeug
from openerp import http
from openerp.http import request
from openerp.modules.registry import RegistryManager
from openerp import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


class office_365_auth(http.Controller):
    @http.route('/web_outlook_plugin/<db>/TaskPane.html', type='http', auth="none")
    def TaskPane(self, db, **kw):
        print "TaskPane"
        print "db"
        print db
        print request.uid
        #
        # registry = RegistryManager.get(db)
        # with registry.cursor() as cr:
        #     irc_obj = registry.get('ir.config_parameter')

        if not request.uid:
            request.uid = request.session.uid

        if not request.uid:
            return werkzeug.utils.redirect('/web_outlook_plugin/%s/login' % db)

        if db and db not in http.db_filter([db]):
            db = None
            print "db = NONE!!!"
            # TODO HANDLE THIS!!
        request.session.db = db

        lead_obj = request.env['crm.lead']
        domain = []
        fields = ['name', 'id']
        data = lead_obj.search_read(domain, fields, order='name')

        return request.render('web_outlook_plugin.outlook_taskpane_view', {'partners': data})
