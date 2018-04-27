# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import models, fields, api, _

class ResCountry(models.Model):
    _inherit = 'res.country'

    code_dian = fields.Char(
        string=u'Código Dian',
        required=False,
        readonly=False
    )

    @api.multi
    def name_get(self):
        rec = []
        for recs in self:
            name = '%s [%s]' % (recs.name or '', recs.code or '')
            rec += [ (recs.id, name) ]
        return rec

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        args = args[:]
        ids = []
        if name:
            ids = self.search([('code_dian', '=like', name + "%")] + args, limit=limit)
            if not ids:
                ids = self.search([('code', operator, name)] + args,limit=limit)
                if not ids:
                    ids = self.search([('name', operator, name)] + args,limit=limit)
        else:
            ids = self.search([], limit=100)

        if ids:
            return ids.name_get()
        return self.name_get()

class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    @api.multi
    def name_get(self):
        rec = []
        for recs in self:
            name = '%s [%s]' % (recs.name or '', recs.code or '')
            rec += [ (recs.id, name) ]
        return rec

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        args = args[:]
        ids = []
        if name:
            ids = self.search([('code', '=like', name + "%")] + args, limit=limit)
            if not ids:
                ids = self.search([('name', operator, name)] + args,limit=limit)
        else:
            ids = self.search([], limit=100)

        if ids:
            return ids.name_get()
        return self.name_get()
