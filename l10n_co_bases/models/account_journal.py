# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    invoice_comment = fields.Text(
        string="Invoice Comment"
    )
