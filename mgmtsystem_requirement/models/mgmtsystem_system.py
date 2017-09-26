# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Decodio applications ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


class MgmtSystemSystem(models.Model):
    _inherit = 'mgmtsystem.system'

    requirement_ids = fields.One2many(
        'mgmtsystem.requirement',
        inverse_name='system_id',
        string="Requirements"
    )