# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    mobile = fields.Char(related='partner_id.mobile', store=True)
