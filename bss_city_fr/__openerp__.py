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
    'name': 'French Cities',
    'version': 'master',
    "category" : 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Search for french zip codes and cities
=====================================

This module imports a list of all french postal codes and cities and add a search field in partner form view. The search field can search data by postal codes or city name.

When a user selects a city, the module Cities fills the following fields automatically  : postal code, city, and country.    
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': ['bss_city'],
    'init_xml': [],
    'update_xml': [
                   'datas/country_state_data.xml',
                   'datas/bluestar.city.csv',],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images' : [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
