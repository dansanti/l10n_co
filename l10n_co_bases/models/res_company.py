# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'


    default_taxes_ids = fields.Many2many(
        string="Customer taxes",
        comodel_name="account.tax",
        relation="company_default_taxes_rel",
        column1="product_id",
        column2="tax_id",
        domain="[('type_tax_use','=','sale')]",
        help="Taxes applied for sale.",
    )
    default_supplier_taxes_ids = fields.Many2many(
        string="Supplier taxes",
        comodel_name="account.tax",
        relation="company_default_supplier_taxes_rel",
        column1="product_id",
        column2="tax_id",
        domain="[('type_tax_use','=','purchase')]",
        help="Taxes applied for purchase.",
    )
