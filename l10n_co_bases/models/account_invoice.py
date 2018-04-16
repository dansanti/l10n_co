
# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for invoice in self:
            invoice.amount_total_words = invoice.currency_id.amount_to_text(invoice.amount_total).upper()

    amount_total_words = fields.Char(
        string="Total (In Words)",
        compute="_compute_amount_total_words"
    )
    show_comment = fields.Boolean(
        string="Show Comment",
        default=False,
    )
