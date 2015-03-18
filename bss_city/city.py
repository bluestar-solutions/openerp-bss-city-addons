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
            result[city.id] = '%(zip)s %(city)s' % {'zip': city.zip , 'city': city.long_name}
        return result

    def _get_is_swiss(self, cr, uid, ids, field_name, arg, context):
        result = {}
        res_country_obj = self.pool.get('res.country')
        swiss_country_id = res_country_obj.search(cr, uid, [('code', '=', 'CH')], context=context)
        for city in self.browse(cr, uid, ids, context=context):
            result[city.id] = city.country_id.id in swiss_country_id
        return result

    _columns = {
        'zip_type': fields.selection(ZIP_TYPES, 'Zip types'),
        'zip': fields.char('Zip', size=10),
        'zip_complement': fields.char('Zip complement', size=2),
        'short_name': fields.char('Short name', size=18),
        'long_name': fields.char('Long name', size=27),
        'state_id': fields.many2one('res.country.state', 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
        'name': fields.function(_get_name, type='char', method=True, store=True, string='Name'),
        'is_swiss': fields.function(_get_is_swiss, type='boolean', method=True, store=True)
    }

    _order = 'is_swiss DESC, country_id, name asc'

bluestar_city()

class bluestar_partner(osv.osv):

    _inherit = 'res.partner'
    _description = "Bluestar City Partner"

    _columns = {
        'city_id': fields.many2one('bluestar.city',
                                   'City Search',
                                   domain="[('zip_type', 'not in', ['80'])]",
                                   required=False, store=False),
    }

    def onchange_city_id(self, cr, uid, ids, city_id):
        v = {}

        if city_id:
            city = self.pool.get('bluestar.city').browse(cr, uid, city_id)
            v['zip'] = city.zip
            v['city'] = city.long_name
            v['country_id'] = city.country_id.id
            if city.state_id:
                v['state_id'] = city.state_id.id
            v['city_id'] = None

        return {'value': v}

bluestar_partner()
