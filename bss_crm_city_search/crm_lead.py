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


class bluestar_partner(osv.osv):
    _inherit = 'crm.lead'

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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
