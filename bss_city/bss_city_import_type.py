# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

from openerp.osv import osv, fields


class bss_city_import_type(osv.osv):
    _name = "bss.city.import_type"
    _description = "City Import Type"

    _columns = {
        'name': fields.char("Name", translated=True),
        'country_id': fields.many2one('res.country', "Country"),
        'method': fields.char('Method'),
        'given_file': fields.boolean('Given File'),
        'comment': fields.text('Comment'),
    }

bss_city_import_type()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
