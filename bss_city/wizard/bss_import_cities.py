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
import csv
import io

from openerp.netsvc import logging
from openerp.osv import osv, fields
from openerp.tools.translate import _


class bss_import_cities(osv.TransientModel):
    _name = 'bss.import_cities'
    _description = 'Import Cities'
    _logger = logging.getLogger(_name)

    _columns = {
        'country_id': fields.many2one('res.country', "Country",
                                      required=True, readonly=True),
        'type_id': fields.many2one(
            'bss.city.import_type', "Type", required=True,
            domain="['|', ('country_id', '=', country_id), "
            "('country_id', '=', False)]",
        ),
        'file': fields.binary("File"),
        'given_file': fields.boolean('Given File', readonly=True),
        'comment': fields.text('Comment', readonly=True),
    }

    def type_id_change(self, cr, uid, ids, type_id, context=None):
        if not type_id:
            return {
                'value': {
                    'comment': "",
                    'given_file': False,
                }
            }
        selected_type = self.pool.get('bss.city.import_type').browse(
            cr, uid, type_id, context
        )
        return {
            'value': {
                'comment': selected_type.comment,
                'given_file': selected_type.given_file,
            }
        }

    def win1250_csv_reader(self, data, **kwargs):
        csv_reader = csv.reader(data, **kwargs)
        for row in csv_reader:
            yield [cell.decode('windows-1250').encode('utf-8') for cell in row]

    def execute(self, cr, uid, ids, context=None):
        wiz = self.browse(cr, uid, ids[0], context)
        getattr(self, wiz.type_id.method)(cr, uid, wiz, context=None)
        return True

    def import_default(self, cr, uid, wiz, context=None):
        state_obj = self.pool.get('res.country.state')
        city_obj = self.pool.get('bluestar.city')

        if not context:
            context = {}

        file_input = io.BytesIO(base64.b64decode(wiz.file))
        reader = csv.reader(file_input)

        headers = reader.next()
        if len(headers) != 4:
            raise osv.except_osv(
                _("Error!"),
                _("Incorrect file format, 5 columns expected.")
            )
        if headers[0] != 'zip':
            raise osv.except_osv(
                _("Error!"),
                _("First column header must be 'zip'.")
            )
        if headers[1] != 'short_name':
            raise osv.except_osv(
                _("Error!"),
                _("Second column header must be 'short_name'.")
            )
        if headers[2] != 'long_name':
            raise osv.except_osv(
                _("Error!"),
                _("Third column header must be 'long_name'.")
            )
        if headers[3] != 'state_code':
            raise osv.except_osv(
                _("Error!"),
                _("Fifth column header must be 'state_code'.")
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
                              row[0], row[2], count, total)
            state_ids = state_obj.search(
                cr, uid, [('code', '=', row[3]),
                          ('country_id', '=', wiz.country_id.id)],
                context=context
            )
            city_obj.create(cr, uid, {
                'zip': row[0],
                'short_name': row[1],
                'long_name': row[2],
                'country_id': wiz.country_id.id,
                'state_id': state_ids and state_ids[0],
            }, context)
            count += 1
        return True

bss_import_cities()
