# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api, fields, models, _

class AccountTax(models.Model):
    _inherit = 'account.tax'

    notprintable = fields.Boolean(
        string="Not Printable",
        default=False,
    )

class AccountTaxTemplate(models.Model):
    _inherit = 'account.tax.template'

    notprintable = fields.Boolean(
        string="Not Printable",
        default=False,
    )
