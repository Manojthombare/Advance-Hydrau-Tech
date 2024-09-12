# -*- coding: utf-8 -*-
{
    'name': "Fetch Deal Data",
    'summary': "fetch data from another erp server",
    'description': "fetch data from another server",
    'author': "Vikash Tiwari",
    'category': 'Fetch Data',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'product'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/deal_data.xml',
        'views/product_views.xml',
        'views/all_account.xml',
        'wizard/deal_wizard.xml',
        'views/deal_data_cron.xml',
        'views/deal_all_data.xml',

    ],
    'installable': True,
    'application': True,
}
