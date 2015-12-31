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
import os

from openerp.netsvc import logging
from openerp.osv import osv


class bss_import_states(osv.TransientModel):
    _inherit = 'bss.import_states'
    _logger = logging.getLogger(_inherit)

    def import_default_given_ch(self, cr, uid, wiz, context=None):
        filename = os.path.join(os.path.dirname(__file__),
                                '../data/states_ch_201512.csv')
        wiz.file = base64.b64encode(open(filename).read())
        self.import_default(cr, uid, wiz, context)

bss_import_states()
