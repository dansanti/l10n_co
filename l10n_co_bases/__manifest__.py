# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Colombian - Base Locatization',
    'summary': 'Colombian - Base Locatization',
    'author': 'Genaro Zorrilla',
    'maintainer': 'Odoo Colombia',
    'website': 'http://www.myodoo.co',
    'version': '11.0.1.0.0',
    'category': 'Localization',
    'depends': [
        'base',
        'account',
        'account_tax_python',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/res.ciiu.csv',
        'data/res_country_data.xml',
        'data/res.country.state.csv',
        'data/res.bank.csv',
        'views/res_ciiu_view.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/res_country_view.xml',
        'views/account_tax_view.xml',
        'views/account_journal_view.xml',
        'views/account_invoice_view.xml',
        'views/product_category_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application' : True,
}
