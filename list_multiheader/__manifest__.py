# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) Anybox
# Copyright (C) 2017 Decodio applications ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'List/tree multi header',
    'version': '10.0.1.0.0',
    'sequence': 150,
    'category': 'Anybox',
    'author': 'Anybox, Decodio applications ltd.',
    'website': 'http://anybox.fr',
    'depends': [
        'base',
        'web',
    ],
    'qweb': [
        'static/src/xml/list_multiheader.xml',
    ],
    'data': [
        'views/list_multiheader.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
