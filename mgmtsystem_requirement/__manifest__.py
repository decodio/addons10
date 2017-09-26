# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Decodio applications ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Management System - Requirement",
    "version": "10.0.1.0.0",
    "author": "Decodio Applications Ltd.",
    "website": "http://www.decod.io",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        'mgmtsystem_audit',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/mgmtsystem_requirement_view.xml',
        'views/mgmtsystem_nonconformity_view.xml',
        'views/mgmtsystem_audit_view.xml',
        'views/mgmtsystem_system_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
