# -*- coding: utf-8 -*-

{
    "name": "Odoo Rebranding",
    "version": "0.1.0.",
    'summary': """ This module helps to rebrand odoo.""",
    "author": "Arpit Goel",
    "license": "Other proprietary",
    "category": "Customization",
    "depends": [
        'base', 'base_setup', 'web', 'mail', 'mail_bot', 'portal',
    ],
    "data": [
        'views/templates.xml',
        'views/login_template.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'data/ir_config_parameter_data.xml',
        'data/mail_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ag_odoo_debrand/static/src/js/webclient.js',
            'ag_odoo_debrand/static/src/js/user_menu.js',
            'ag_odoo_debrand/static/src/js/dialog.js',
            'ag_odoo_debrand/static/src/js/error_dialogs.js',
        ],
        'web.assets_qweb': [
            ('replace', 'base_setup/static/src/xml/res_config_edition.xml', 'ag_odoo_debrand/static/src/xml/res_config_edition.xml'),
            ('replace', 'web/static/src/core/errors/error_dialogs.xml', 'ag_odoo_debrand/static/src/xml/error_dialogs.xml'),
            ('replace', 'mail/static/src/components/notification_alert/notification_alert.xml', 'ag_odoo_debrand/static/src/xml/notification_alert.xml'),
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': True,
}
