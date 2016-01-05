# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2015 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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
##############################################################################


{
    'name': 'Postal Codes',
    'version': '7.0.2.0-20160104',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Common structure for localized postal codes addons
==================================================

This is a technical addon to define common structure to store cities
(used by localized cities addons).
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',

        'data/bss_state_import_type.xml',
        'data/bss_city_import_type.xml',

        'wizard/bss_import_states_view.xml',
        'wizard/bss_import_cities_view.xml',

        'res_country_view.xml',
        'res_country_state_view.xml',
        'bss_city_view.xml',
    ],
    'demo': [
        'demo/res.country.state.yml',
        'demo/bluestar.city.yml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
