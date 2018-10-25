# -*- coding: utf-8 -*-

import logging
import subprocess

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
    location = fields.Char("Location", help='e.g. Warehouse 3, Location',
                           required=True)
    info = fields.Char(string='Description',
                       help='e.g. Zebra Warehouse 3 zone 28, Description in CUPS',
                       required=True)
    uri = fields.Char(string='URI', required=True,
                      help='e.g. socket://10.134.32.81:9100')
    printer_driver = fields.Char(
        string="Printer driver",
        required=True,
        help="e.g. drv:///sample.drv/zebra.ppd")

    @api.multi
    def add_printer(self):
        self.ensure_one()
        try:
            self.server_id.add_printer(
                name=self.system_name,
                device_uri=self.uri,
                info=self.name,
                location=self.location,
                ppdname=self.printer_driver
            )
            printer_model = self.env['printing.printer']
            printer_id = printer_model.search(
                [('server_id', '=', self.server_id.id), ('uri', '=', self.uri)],
                limit=1)
            if printer_id:
                printer_id.enable()
        except Exception as a:
            _logger.error("Error: " + str(a))
            raise UserError(_("Invalid URI."))


