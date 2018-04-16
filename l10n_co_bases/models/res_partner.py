# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID, api, fields, models, _
from odoo.exceptions import ValidationError, except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char(
        string="First Name",
    )
    middle_name = fields.Char(
        string="Middle Name",
    )
    last_name = fields.Char(
        string="Last Name",
    )
    second_last_name = fields.Char(
        string="Second Last Name",
    )
    vat_ref = fields.Char(
        string="NIT Formateado",
        compute="_compute_vat_ref",
        readonly=True,
    )
    vat_type = fields.Selection(
        string=u'Tipo de Documento',
        selection=[
            ('11', u'11 - Registro civil de nacimiento'),
            ('12', u'12 - Tarjeta de identidad'),
            ('13', u'13 - Cédula de ciudadanía'),
            ('14', u'14 - Certificado de la Registraduría para sucesiones ilíquidas de personas naturales que no tienen ningún documento de identificación.'),
            ('15', u'15 - Tipo de documento que identifica una sucesión ilíquida, expedido por la notaria o por un juzgado. '),
            ('21', u'21 - Tarjeta de extranjería'),
            ('22', u'22 - Cédula de extranjería'),
            ('31', u'31 - NIT/RUT'),
            ('33', u'33 - Identificación de extranjeros diferente al NIT asignado DIAN'),
            ('41', u'41 - Pasaporte'),
            ('42', u'42 - Documento de identificación extranjero'),
            ('43', u'43 - Sin identificación del exterior o para uso definido por la DIAN'),
        ],
        required=False,
        help = u'Identificacion del Cliente, segun los tipos definidos por la DIAN.',
    )
    vat_vd = fields.Integer(
        string=u"Digito Verificación",
    )
    ciiu_id = fields.Many2one(
        string='Actividad CIIU',
        comodel_name='res.ciiu',
        domain=[('type', '!=', 'view')],
        help=u'Código industrial internacional uniforme (CIIU)'
    )

    sale_taxes_id = fields.Many2many(
        string="Customer taxes",
        comodel_name="account.tax",
        relation="partner_tax_sale_rel",
        column1="partner_id",
        column2="tax_id",
        domain="[('type_tax_use','=','sale')]",
        context={"default_type_tax_use": "sale"},
        help="Taxes applied for sale.",
    )
    purchase_taxes_id =  fields.Many2many(
        string="Supplier taxes",
        comodel_name="account.tax",
        relation="partner_tax_purchase_rel",
        column1="partner_id",
        column2="tax_id",
        domain="[('type_tax_use','=','purchase')]",
        context={"default_type_tax_use": "sale"},
        help="Taxes applied for purchase.",
    )

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Busca VAT en las vistas relacionadas con res.partner
            args = [('vat', 'ilike', name)] + args
        return super(ResPartner, self).name_search(name, args=args, operator=operator, limit=limit)

    @api.multi
    def _display_address(self, without_company=False):
        if self.vat_type in ['31','13','22']:
            id_type = {}
            id_type['31'] = 'NIT'
            id_type['13'] = 'CC'
            id_type['22'] = 'CE'
            id_id = id_type[self.vat_type]
        else:
            id_id = 'ID'

        res = super(ResPartner, self)._display_address(without_company=without_company)
        if self.vat_ref:
            res = "%s:%s\n%s" % (id_id, self.vat_ref, res)
        else:
            res = "%s:%s\n%s" % (id_id, self.vat, res)

        return res


    @api.one
    def _compute_vat_ref(self):
        result_vat = None
        if self.vat_type == '31' and self.vat and self.vat.isdigit() and len(self.vat.strip()) > 0:
            result_vat = '{:,}'.format(int(self.vat.strip())).replace(",", ".")
            self.vat_ref = "%s-%i" % (result_vat,self.vat_vd)
        else:
            self.vat_ref = self.vat

    @api.one
    @api.depends('vat', 'vat_type', 'vat_vd')
    @api.constrains("vat_vd")
    def check_vat_dv(self):
        if self.vat_type == '31' and self.vat and not self.check_vat_co(self.vat, self.vat_vd):
            _logger.info(u'Importing VAT Number [%s - %i] for "%s" is not valid !' % (self.vat, self.vat_vd, self.name))
            raise ValidationError(u'NIT/RUT [%s - %i] suministrado para "%s" no supera la prueba del dígito de verificacion!' %
                                  (self.vat, self.vat_vd, self.name))
        return True

    @api.one
    @api.constrains("vat")
    def check_vat(self):
        self.vat.strip()
        if self.vat:
            if len(self.search(
                    [
                        ('company_id','=',self.company_id),
                        ('vat','=',self.vat)
                    ]
                )) != 1:
                raise ValidationError(u'Identificación [%s] suministrado para "%s" ya existe' %
                                     (self.vat, self.name))
        return True
    def check_vat_co(self, vat, vat_vd):
        factor = (71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3)
        vat = vat.rjust(15, '0')
        csum = sum([int(vat[i]) * factor[i] for i in range(15)])
        check = csum % 11
        if check > 1:
            check = 11 - check
        if check == vat_vd:
            return True
        return False

    @api.onchange('first_name', 'middle_name', 'last_name', 'second_last_name')
    def _onchange_person_names(self):
        if self.company_type == 'person':
            names = [name for name in [self.first_name, self.middle_name, self.last_name, self.second_last_name] if name]
            self.name = u' '.join(names)

    @api.depends('company_type', 'name', 'first_name', 'middle_name', 'last_name', 'second_last_name')
    def copy(self, default=None):
        default = default or {}
        if self.company_type == 'person':
            default.update({
                'first_name': self.first_name and self.first_name + '(copy)' or '',
                'middle_name': self.middle_name and self.middle_name + '(copy)' or '',
                'last_name': self.last_name and self.last_name + '(copy)' or '',
                'second_last_name': self.second_last_name and self.second_last_name + '(copy)' or '',
            })
        return super(ResPartner, self).copy(default=default)

    @api.multi
    def person_name(self, vals):
        values = vals or {}
        person_field = ['first_name', 'middle_name', 'last_name', 'second_last_name']
        person_names = set(person_field)
        values_keys = set(values.keys())

        if person_names.intersection(values_keys):
            names = []
            for x in person_field:
                if x in values.keys():
                    names += [values.get(x, False) and values.get(x).strip() or '']
                else:
                    names += [self[x] or '']
            name = ' '.join(names)
            if name.strip():
                values.update({
                    'name': name,
                })

        if values.get('name', False):
            values.update({
                'name': values.get('name').strip(),
            })

        return values

    @api.multi
    def write(self, values):
        values = self.person_name(values)
        return super(ResPartner, self).write(values)

    @api.model
    def create(self, values):
        values = self.person_name(values)
        return super(ResPartner, self).create(values)
