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

from openerp.osv import osv, fields


class res_country_state(osv.osv):
    _inherit = 'res.country.state'

    def _get_unique_code(self, cr, uid, ids, field_name, arg, context):
        result = {}
        for state in self.browse(cr, uid, ids, context=context):
            result[state.id] = '%(cc)s_%(sc)s' % {
                'cc': state.country_id.code,
                'sc': state.code
            }
        return result

    _columns = {
        'name': fields.char('State Name', size=64,
                            required=True, translate=True),
        'active': fields.boolean("Active"),
        'unique_code': fields.function(
            _get_unique_code, type='char', method=True, store={
                'res.country.state': (
                    lambda self, cr, uid, ids, ctx=None: ids,
                    ['code'], 10
                ),
                'res.country': (
                    lambda self, cr, uid, ids, ctx=None:
                    self.pool.get('res.country.state').search(cr, uid, [
                        ('country_id.id', 'in', ids),
                    ], context=ctx),
                    ['code'], 10
                ),
            }, string='Unique Code'),
    }

    _defaults = {
        'active': True,
    }

    _sql_constraints = [
        ('unique_code_unique', 'unique(unique_code)',
         'Unique code has to be unique!')
    ]

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        ids = self.search(cr, user, [('unique_code', 'ilike', name)] + args,
                          limit=limit, context=context)
        if not ids:
            ids = self.search(cr, user, [('name', operator, name)] + args,
                              limit=limit, context=context)
        return self.name_get(cr, user, ids, context)

res_country_state()
