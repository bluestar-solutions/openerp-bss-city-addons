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

import base64
import io

from openerp.netsvc import logging
from openerp.osv import osv
from openerp.tools.translate import _


class bss_import_cities(osv.TransientModel):
    _inherit = 'bss.import_cities'
    _logger = logging.getLogger(_inherit)

    def import_openedata_admin_ch(self, cr, uid, wiz, context=None):
        state_obj = self.pool.get('res.country.state')
        city_obj = self.pool.get('bluestar.city')

        if not context:
            context = {}

        file_input = io.BytesIO(base64.b64decode(wiz.file))
        reader = self.decoded_csv_reader(file_input, 'iso-8859-15',
                                         delimiter=';')

        headers = reader.next()
        if len(headers) != 7:
            raise osv.except_osv(
                _("Error!"),
                _("Incorrect file format, 7 columns expected.")
            )
        if headers[0] != 'Ortschaftsname':
            raise osv.except_osv(
                _("Error!"),
                _("First column header must be 'Ortschaftsname'.")
            )
        if headers[1] != 'PLZ':
            raise osv.except_osv(
                _("Error!"),
                _("Second column header must be 'PLZ'.")
            )
        if headers[4] != 'Kantonskürzel':
            raise osv.except_osv(
                _("Error!"),
                _("Fifth column header must be 'Kantonskürzel'.")
            )

        existing_city_ids = city_obj.search(cr, uid, [
            ('country_id', '=', wiz.country_id.id),
        ], context=context)
        city_obj.unlink(cr, uid, existing_city_ids, context)

        rows = list(reader)
        total = len(rows)
        count = 1
        for row in rows:
            self._logger.info("Import '%s %s' [%d/%d]",
                              row[1], row[0], count, total)
            state_ids = state_obj.search(
                cr, uid, [('code', '=', row[4]),
                          ('country_id', '=', wiz.country_id.id)],
                context=context
            )
            city_obj.create(cr, uid, {
                'zip': row[1],
                'short_name': row[0],
                'long_name': row[0],
                'country_id': wiz.country_id.id,
                'state_id': state_ids and state_ids[0],
            }, context)
            count += 1
        return True

bss_import_cities()
