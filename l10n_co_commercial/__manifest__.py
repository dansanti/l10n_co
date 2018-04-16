# -*- coding: utf-8 -*-
# Copyright 2013 Genaro Zorrilla, Odoo Colombia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Colombian - Accounting Commercial',
    'summary': 'Colombian - Accounting Commercial',
    'author': 'Genaro Zorrilla',
    'maintainer': 'Odoo Colombia',
    'website': 'http://www.myodoo.co',
    'version': '11.0.1.0.0',
    'category': 'Localization',
    'depends': [
        'account',
        'l10n_co_bases',
    ],
    'data':[
        'data/l10n_co_chart_template_commercial.xml',
        'data/account.account.template.csv',
        'data/account_chart_template.xml',
        'data/account_tax_group.xml',
        'data/account_tax_template.xml',
        'data/account_chart_template.yml',

    ],
    'installable': True,
    'auto_install': False,
    'application' : True,
}
