# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Decodio applications ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemVerificationLine(models.Model):
    """Class to manage verification's Line."""
    _inherit = "mgmtsystem.verification.line"

    requirement_id = fields.Many2one(
        'mgmtsystem.requirement',
        string='Requirements'
    )