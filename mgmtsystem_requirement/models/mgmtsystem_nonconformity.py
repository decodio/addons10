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

    @api.model
    def create(self, vals):
        """Override of create with direct call to models.Model.create()
           so we can inherit and update vals without triggering sequence before
           or after calling super
        """
        if vals.get('ref', 'NEW') == 'NEW':
            vals.update({
                'ref': self.env['ir.sequence'].next_by_code(
                    'mgmtsystem.nonconformity')
            })
        return super(models.Model, self).create(vals)