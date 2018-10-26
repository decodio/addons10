# -*- coding: utf-8 -*-

import logging
import subprocess

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PrintingPrinterAddWizard(models.TransientModel):
    _name = 'printing.printer.add.wizard'
    _description = 'Add Printer to CUPS Wizard'

    def _default_server(self):
        return self.env['printing.server'].search([], limit=1)

    server_id = fields.Many2one(
        comodel_name='printing.server', string='Server', required=True,
        help='Print Server.', default=_default_server)
    system_name = fields.Char(
        "Printer name", required=True,
        help='Printer and queue name to add/change on CUPS server'
                              )
    name = fields.Char(required=True, help='CUPS Printer Description/Info')
    location = fields.Char("Location", help='e.g. Warehouse 3',
                           required=True)
    uri = fields.Char(string='URI', required=True,
                      help='e.g. socket://10.134.32.81:9100')
    printer_driver = fields.Char(
        string="Printer driver",
        required=True,
        help="e.g. drv:///sample.drv/zebra.ppd")

    @api.onchange('system_name')
    def _onchange_system_name(self):
        self.name = self.system_name
        self.location = self.system_name

    @api.multi
    def add_printer(self):
        self.server_id.add_printer(
            name=self.system_name,
            device_uri=self.uri,
            info=self.name,
            location=self.location,
            ppdname=self.printer_driver
        )
