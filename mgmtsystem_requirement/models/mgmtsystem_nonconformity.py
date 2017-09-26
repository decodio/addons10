# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Decodio applications ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class MgmtsystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    requirement_id = fields.Many2one(
        'mgmtsystem.requirement',
        string='Requirements'
    )
