# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Decodio applications ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class MgmtsystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    requirement_id = fields.Many2one(
        'mgmtsystem.requirement',
        string='Requirement'
    )

    @api.onchange('system_id')
    def onchange_system(self):
        self.requirement_id = None
