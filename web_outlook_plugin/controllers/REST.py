# import werkzeug
import simplejson
from openerp import http
from openerp.http import request
from openerp.exceptions import AccessError, Warning
import requests
from lxml import etree

import logging
_logger = logging.getLogger(__name__)


class outlook_REST_API(http.Controller):
    @http.route('/web_outlook_plugin/REST/attachtolead/', type='http', auth="public")
    def attachtolead(self, **kw):
        _logger.info('Enter attachtolead: ')
        if not request.session.uid:
            ret = {"status": "expired", "desc": "Session expired!"}
            return simplejson.dumps(ret)
        message_body = kw.get('message_body')
        lead_id = kw.get('lead_id')
        subject = kw.get('subject')
        _from = kw.get('from')
        _to = kw.get('to')
        # _logger.info('body: %s, id:%s, %s', message_body, lead_id, subject)
        _logger.info('_from: %s, _to:%s', _from, _to)

        msg_obj = request.env['mail.message']
        msg_id = msg_obj.create({
            'model': 'crm.lead',
            'res_id': lead_id,
            'record_name': subject,
            'type': 'email',
            'body': message_body,
            'email_from': _from,
        })
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        url = base_url + ("/web#id=%s&view_type=form&model=crm.lead") % (lead_id)
        ret = {"status": "success", "messageId": msg_id.id, "url": url}
        return simplejson.dumps(ret)

    @http.route('/web_outlook_plugin/REST/attach_message_to_model/', type='http', auth="public")
    def attach_message_to_model(self, **kw):
        _logger.info('Enter attach_message_to_model: ')
        if not request.session.uid:
            ret = {"status": "expired", "desc": "Session expired!"}
            return simplejson.dumps(ret)

        message_body = kw.get('message_body')
        res_id = kw.get('res_id', False)
        subject = kw.get('subject')
        _from = kw.get('from')
        _to = kw.get('to')
        res_model = kw.get('model', False)

        if not res_model:
            ret = {"status": "error", "desc": "model not supplied!"}
            return simplejson.dumps(ret)

        if not res_id:
            ret = {"status": "error", "desc": "res_id not supplied!"}
            return simplejson.dumps(ret)

            # _logger.info('body: %s, id:%s, %s', message_body,         res_id, subject)
        _logger.info('_from: %s, _to:%s', _from, _to)
        _logger.info('model: %s, res_id:%s', res_model, res_id)

        msg_obj = request.env['mail.message']
        try:
            msg_id = msg_obj.create({
                'model': res_model,
                'res_id': res_id,
                'record_name': subject,
                'type': 'email',
                'body': message_body,
                'email_from': _from,
            })
        except AccessError:  # no create access rights
            ret = {"status": "error",
                   "desc": "Sorry, you are not allowed to create this kind of document. Please contact your Odoo administrator!"}
            _logger.info('not allowed; model: %s, res_id:%s', res_model, res_id)
            return simplejson.dumps(ret)


        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        url = base_url + ("/web#id=%s&view_type=form&model=%s") % (res_id, res_model)
        ret = {"status": "success", "messageId": msg_id.id, "url": url}
        return simplejson.dumps(ret)

    @http.route('/web_outlook_plugin/REST/createobject/', type='http', auth="public")
    def createobject(self, **kw):
        if not request.session.uid:
            ret = {"status": "expired", "desc": "Session expired!"}
            return simplejson.dumps(ret)
        _logger.info('sendtolead kw: %s ', kw)
        partner_obj = request.env['res.partner']

        model = kw.get('model', False)
        sender_name = kw.get('senderName')
        senderAddress = kw.get('senderAddress')
        name = kw.get('name', False)
        _logger.info('Sender name: %s, address: %s ', sender_name, senderAddress)

        if not model:
            ret = {"status": "error", "desc": "Resource model missing!"}
            return simplejson.dumps(ret)
        res_obj = request.env[model]

        if not name:
            users_obj = request.env['res.users']
            user = users_obj.browse(request.session.uid)
            name = user.name + " added new lead!"
        try:
            res_id = res_obj.create({
                'name': name,
            })
        except AccessError:  # no create access rights
            ret = {"status": "error",
                   "desc": "Sorry, you are not allowed to create this kind of document. Please contact your Odoo administrator!"}
            return simplejson.dumps(ret)

        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        url = base_url + ("/web#id=%s&view_type=form&model=%s") % (res_id.id, model)

        ret = {"status": "success", "res_id": res_id.id, "url": url}
        return simplejson.dumps(ret)

    # obsolete, delete
    @http.route('/web_outlook_plugin/REST/sendtolead/', type='http', auth="public")
    def sendtolead(self, **kw):
        if not request.session.uid:
            ret = {"status": "expired", "desc": "Session expired!"}
            return simplejson.dumps(ret)
        _logger.info('sendtolead kw: %s ', kw)
        lead_obj = request.env['crm.lead']
        partner_obj = request.env['res.partner']

        sender_name = kw.get('senderName')
        senderAddress = kw.get('senderAddress')
        subject = kw.get('subject')
        _logger.info('Sender name: %s, address: %s ', sender_name, senderAddress)

        if not subject:
            users_obj = request.env['res.users']
            user = users_obj.browse(request.session.uid)
            subject = user.name + " added new lead!"
        try:
            cid = lead_obj.create({
                'name': subject,
                # 'type': 'lead',
            })
        except AccessError:  # no create access rights
            ret = {"status": "error", "desc": "Sorry, you are not allowed to create this kind of document."}
            return simplejson.dumps(ret)

        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        url = base_url + ("/web#id=%s&view_type=form&model=crm.lead") % (cid.id)
        print "url"
        print url
        ret = {"status": "success", "leadId": cid.id, "url": url}
        return simplejson.dumps(ret)

    @http.route('/web_outlook_plugin/REST/getleads/', type='http', auth="public")
    def getleads(self, **kw):
        if not request.session.uid:
            ret = {"status": "expired", "desc": "Session expired!"}
            return simplejson.dumps(ret)
        lead_obj = request.env['crm.lead']
        domain = []
        fields = ['name', 'id']
        data = lead_obj.search_read(domain, fields)
        ret = {"status": "success", "data": data}
        return simplejson.dumps(ret)

    # https: // graph.microsoft.com / beta / me / messages / [message % 20id] / attachments / [attachment % 20id]




    @http.route('/web_outlook_plugin/REST/AttachAttachmentToObject/', type='http', auth="public")
    def AttachAttachmentToObject(self, **kw):
        if not request.session.uid:
            ret = {"status": "expired", "desc": "Session expired!"}
            return simplejson.dumps(ret)
        _logger.info('AttachAttachmentToObject kw: %s ', kw)

        attachment_obj = request.env['ir.attachment']

        res_id = kw.get('res_id')
        res_model = kw.get('res_model')
        ewsUrl = kw.get('ewsUrl')
        attachments = kw.get('attachments')
        attachments_len = kw.get('attachments_len')
        attachmentToken = kw.get('attachmentToken')

        # generate soap request for exchange server
        att_ids = ""
        for x in range(0, int(attachments_len)):
            att_id = kw.get('attachments[' + str(x) + '][id]')
            att_ids += '<t:AttachmentId Id="' + str(att_id) + '"/>'

        soap_req = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
            <soap:Header>
                <t:RequestServerVersion Version="Exchange2013" />
            </soap:Header>
          <soap:Body>
            <GetAttachment xmlns="http://schemas.microsoft.com/exchange/services/2006/messages"
            xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
              <AttachmentShape/>
              <AttachmentIds>
                %s
              </AttachmentIds>
            </GetAttachment>
          </soap:Body>
        </soap:Envelope>""" % (att_ids)

        # send authorization code in header
        headers = {'content-type': 'text/xml', 'Authorization': 'Bearer ' + str(attachmentToken)}

        response = requests.post(ewsUrl, data=soap_req, headers=headers)

        _fName = ""
        _fContentType = ""
        _fContent = ""

        tree = etree.fromstring(response.content)
        for node in tree.iter(tag=etree.Element):

            nm = node.tag.replace('{http://schemas.microsoft.com/exchange/services/2006/types}', '')
            if nm == 'Name':
                _fName = node.text
            if nm == 'ContentType':
                _fContentType = node.text
            if nm == 'Content':
                _fContent = node.text
                attachment_id = attachment_obj.create({
                    'name': _fName,
                    'datas': _fContent,
                    'datas_fname': _fName,
                    'res_model': res_model,
                    'res_id': int(res_id)
                })
                print attachment_id
                # ContentType
                # Content
                # Name
        # print tree.find('GetAttachmentResponseMessage').text

        ret = {"status": "success"}
        return simplejson.dumps(ret)

        # att_obj = request.env['ir.attachment']
        # att_id = att_obj.create({
        #     'res_model': res_model,
        #     'res_id': res_id,
        #     'record_name': subject,
        #     'name': name,
        #     # 'body': message_body,
        #     # 'email_from': _from,
        # })
        #
        # base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        # url = base_url + ("/web#id=%s&view_type=form&model=crm.lead") % (att_id.id)
        # print "url"
        # print url
        # ret = {"status": "success", "att_id": att_id.id, "url": url}
        # return simplejson.dumps(ret)



    """
    @http.route('/web_outlook_plugin/REST/getleads/', type='http', auth="public")
    def getleads(self, **kw):
        if not request.session.uid:
            ret = {"status": "expired", "desc": "Session expired!"}
            return simplejson.dumps(ret)

        lead_obj = request.env['crm.lead']
        partner_obj = request.env['res.partner']
        data = []
        cids = lead_obj.search([('type', '=', 'lead'), ('partner_id', '!=', False)])
        for cid in cids:
            lead = lead_obj.browse(cid.id)
            print "lead"
            print lead
            print lead.partner_name
            print lead.partner_id
            print lead.partner_id.id
            data.append({'name': lead.partner_name, 'id': lead.partner_id.id})

        ret = {"status": "success", "data": data}
        return simplejson.dumps(ret)
    """