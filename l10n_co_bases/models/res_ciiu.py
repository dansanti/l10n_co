# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api, fields, models, _

class ResCIIU(models.Model):
    _name = 'res.ciiu'
    _description = "CIIU Codes"
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'code, name'
    _order = 'parent_left'

    name = fields.Char(
        string='Name',
        help='CIIU Nmae',
        required=True,
        index=1,
    )
    display_name = fields.Char(
        string="Display Name",
        compute="_compute_display_name",
    )
    code = fields.Char(
        string='Code',
        help='CIIU code.',
        required=True,
        index=1,
    )
    note = fields.Text(
        string='Note'
    )
    type = fields.Selection(
        string='Type',
        selection=[
            ('view','view'),
            ('other','other')
        ],
        help="Registry type",
        required=True
    )
    parent_id = fields.Many2one(
        string='Parent',
        comodel_name='res.ciiu',
        ondelete="set null"
    )
    child_ids = fields.One2many(
        string="Childs Codes",
        comodel_name="res.ciiu",
        inverse_name='parent_id',
    )
    parent_left = fields.Integer(
        'Parent Left',
        index=1)
    parent_right = fields.Integer(
        'Parent Right',
        index=1)


    _sql_constraints = [
        ('name_uniq', 'unique (code)', 'The code of CIIU must be unique !')
    ]

    @api.depends('code','name')
    def _compute_display_name(self):
        for ciiu in self:
            ciiu.display_name = "[%s] %s" % (ciiu.code, ciiu.name)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            ciiu = self.search(['|', ('name', operator, name),('code', operator, name)] + args, limit=limit)
        else:
            ciiu = self.search(args, limit=limit)

        return ciiu.name_get()

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.code:
                name = u"[%s] %s" % (record.code, name)
            res.append((record.id, name))
        return res

    @api.multi
    def action_parent_store_compute(self):
        self._parent_store_compute()
