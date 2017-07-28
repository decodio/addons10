# -*- coding: utf-8 -*-

###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

{
    "name": "MuK Preview Attachment",
    "summary": """Attachment Preview Dialog""",
    "description": """ 
        Adds a button to the Attachment Sidebar to
        preview the content directly in the browser..
    """,
    "version": "10.0.1.0.1",
    "category": "Extra Tools",
    "license": "AGPL-3",
    "website": "http://www.mukit.at",
    "author": "MuK IT",
    "contributors": [
        "Mathias Markl <mathias.markl@mukit.at>",
    ],
    "depends": [
        "muk_web_preview",
        "muk_web_preview_audio",
        "muk_web_preview_csv",
        "muk_web_preview_image",
        "muk_web_preview_mail",
        "muk_web_preview_msoffice",
        "muk_web_preview_text",
        "muk_web_preview_vector",
        "muk_web_preview_video",
    ],
    "data": [
        "template/assets.xml",
    ],
    "demo": [
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    "images": [
        'static/description/banner.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
    
}