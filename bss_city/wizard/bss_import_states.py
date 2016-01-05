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
import copy
import csv
import io

from openerp.netsvc import logging
from openerp.osv import osv, fields
from openerp.tools.translate import _


class bss_import_states(osv.TransientModel):
    _name = 'bss.import_states'
    _description = 'Import States'
    _logger = logging.getLogger(_name)

    _columns = {
        'country_id': fields.many2one('res.country', "Country",
                                      required=True, readonly=True),
        'type_id': fields.many2one(
            'bss.state.import_type', "Type", required=True,
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
        selected_type = self.pool.get('bss.state.import_type').browse(
            cr, uid, type_id, context
        )
        return {
            'value': {
                'comment': selected_type.comment,
                'given_file': selected_type.given_file,
            }
        }

    def execute(self, cr, uid, ids, context=None):
        wiz = self.browse(cr, uid, ids[0], context)
        getattr(self, wiz.type_id.method)(cr, uid, wiz, context=None)
        return True

    def import_default(self, cr, uid, wiz, context=None):
        lang_obj = self.pool.get('res.lang')
        state_obj = self.pool.get('res.country.state')

        if not context:
            context = {}

        file_input = io.BytesIO(base64.b64decode(wiz.file))
        reader = csv.reader(file_input)

        headers = reader.next()
        if len(headers) < 2:
            raise osv.except_osv(
                _("Error!"),
                _("Incorrect file format, at least 2 columns expected.")
            )
        if headers[0] != 'code':
            raise osv.except_osv(
                _("Error!"),
                _("First column header must be 'code'.")
            )
        if headers[1] != 'name':
            raise osv.except_osv(
                _("Error!"),
                _("Second column header must be 'name'.")
            )
        lang_columns = {}
        for i in range(len(headers[2:])):
            header = headers[i + 2]
            terms = header.split(':')
            if len(terms) != 2 or terms[0] != 'name':
                raise osv.except_osv(
                    _("Error!"),
                    _("Incorrect column format. Column '%s' must be in format "
                      "'name:[LOCALE_CODE]'") % header
                )
            iso_code = terms[1]
            lang_ids = lang_obj.search(cr, uid, [('iso_code', '=', iso_code)],
                                       context=context)
            if not lang_ids:
                self._logger.warn("'%s' is not an installed language code, "
                                  "column will be ignored" % iso_code)
                continue
            lang_columns[i + 2] = iso_code

        tmp_context = copy.deepcopy(context)
        state_ids = []
        rows = list(reader)
        total = len(rows)
        count = 1
        for row in rows:
            self._logger.info("Import '%s' [%d/%d]", row[1], count, total)
            existing_state_ids = state_obj.search(cr, uid, [
                ('country_id', '=', wiz.country_id.id),
                ('code', '=', row[0]),
            ], context=context)
            state_id = None
            if existing_state_ids:
                state_id = existing_state_ids[0]

            existing_inactive_state_ids = state_obj.search(cr, uid, [
                ('country_id', '=', wiz.country_id.id),
                ('code', '=', row[0]),
                ('active', '=', False),
            ], context=context)
            if existing_inactive_state_ids:
                state_id = existing_inactive_state_ids[0]
                state_obj.write(cr, uid, [state_id], {
                    'active': True,
                }, context)

            tmp_context['lang'] = 'en_US'
            if state_id:
                state_obj.write(cr, uid, [state_id], {
                    'name': row[1],
                }, context)
            else:
                state_id = state_obj.create(cr, uid, {
                    'code': row[0],
                    'name': row[1],
                    'country_id': wiz.country_id.id,
                }, context)
            for column, iso_code in lang_columns.items():
                tmp_context['lang'] = iso_code
                state_obj.write(cr, uid, [state_id],
                                {'name': row[column]}, tmp_context)
            state_ids.append(state_id)
            count += 1

        inactive_state_ids = state_obj.search(cr, uid, [
            ('country_id', '=', wiz.country_id.id),
            ('id', 'not in', state_ids),
        ], context=context)
        state_obj.write(cr, uid, inactive_state_ids, {'active': False},
                        context)
        return True

bss_import_states()
