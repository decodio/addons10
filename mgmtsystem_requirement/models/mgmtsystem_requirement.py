# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Decodio applications ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class MgmtsystemRequirement(models.Model):
    _name = "mgmtsystem.requirement"

    name = fields.Char(
        string="Name",
        required=True
    )
    description = fields.Text(
        string="Description"
    )
    system_id = fields.Many2one(
        'mgmtsystem.system',
        string='System',
        required=True
    )
    nonconformity_ids = fields.One2many(
        'mgmtsystem.nonconformity',
        inverse_name='requirement_id',
        string="Nonconformitys"
    )
    audit_ids = fields.One2many(
        'mgmtsystem.verification.line',
        inverse_name='requirement_id',
        string="Audits"
    )