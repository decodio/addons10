# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AddPrinterWizard(models.TransientModel):
    _name = 'add.printer.wizard'
    _description = 'Add Printer Wizard'

    name = fields.Char(required=True, help='Zebra_wh_3_28, Printer Queue Name'
                                           'in CUPS')
    
    def _default_server(self):
        return self.env['printing.server'].search([], limit=1)

    server_id = fields.Many2one(
        comodel_name='printing.server', string='Server', required=True,
        help='Server used to access this printer.', default=_default_server)
    system_name = fields.Char("System name", required=True)
    location = fields.Char("Location", help='Warehouse 3, Location',
                           required=True)
    info = fields.Char(string='Description',
                       help='Zebra Warehouse 3 zone 28, Description in CUPS',
                       required=True)
    uri = fields.Char(string='URI', required=True,
                      help='socket://10.134.32.81:9100')

    @api.multi
    def add_printer(self):
        self.ensure_one()
        try:
            self.server_id.add_printer(
                name=self.name,
                device_uri=self.uri,
                info=self.info,
                location=self.location
            )
        except Exception as a:
            _logger.error("Error: " + str(a))
            raise UserError(_("Invalid URI."))


