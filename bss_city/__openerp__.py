# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2013 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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
    'name': 'Cities',
    'version': 'master',
    "category" : 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Search for zip codes and cities
=====================================

Add a search field in partner form view. The search field can search data by postal codes or city name.

When a user selects a city, the module fills the following fields automatically  : postal code, city, state and country.    
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': [],
    'init_xml': [],
    'update_xml': ['security/ir.model.access.csv',
                   'city_view.xml'],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images' : ['images/city_search_1.png','images/city_search_2.png','images/city_search_3.png',],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
