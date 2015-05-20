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

from openerp.osv import osv, fields

ZIP_TYPES = [('10', 'Home addresses and PO Box'),
             ('20', 'Home addresses only'),
             ('30', 'PO Box only'),
             ('40', 'Business'),
             ('80', 'Internal for the Post')]


class bluestar_city(osv.osv):
    _name = "bluestar.city"
    _description = "City"

    def _get_name(self, cr, uid, ids, field_name, arg, context):
        result = {}
        for city in self.browse(cr, uid, ids, context=context):
            result[city.id] = '%(zip)s %(city)s' % {
                'zip': city.zip,
                'city': city.long_name
            }
        return result

    def _get_is_country_of_company(self, cr, uid, ids, field_name,
                                   arg, context):
        result = {}

        country_id = self.pool.get('res.users').browse(
            cr, uid, uid, context
        ).company_id.country_id

        if not country_id:
            return dict.fromkeys(ids, False)

        for city in self.browse(cr, uid, ids, context=context):
            result[city.id] = city.country_id == country_id
        return result

    _columns = {
        'zip_type': fields.selection(ZIP_TYPES, 'Zip Types'),
        'zip': fields.char('Zip', size=10),
        'zip_complement': fields.char('Zip Complement', size=2),
        'short_name': fields.char('Short Name', size=18),
        'long_name': fields.char('Long Name', size=27),
        'state_id': fields.many2one('res.country.state', 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
        'name': fields.function(
            _get_name, type='char', method=True, store={
                'bluestar.city': (
                    lambda self, cr, uid, ids, ctx=None: ids,
                    ['zip', 'city'], 10
                ),
            }, string='Name'
        ),
        'is_country_of_company': fields.function(
            _get_is_country_of_company, type='boolean', method=True,
            store={
                'res.company': (
                    lambda self, cr, uid, ids, ctx=None:
                        self.pool.get('bluestar.city').search(
                            cr, uid, [], context=ctx
                        ), ['country_id'], 10
                ),
                'bluestar.city': (
                    lambda self, cr, uid, ids, ctx=None: ids,
                    ['country_id'], 10
                )
            }, string="Is Country of Company"
        )
    }

    _order = 'is_country_of_company DESC, country_id, name asc'

bluestar_city()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
