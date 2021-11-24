# -*- coding: utf-8 -*-
{
    'version': '14.0.0.1.5',    
    'name': "Mobile Connect",

    'summary': """
        App for sending sms from odoo via playsms.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mybizna",
    'website': "http://www.mybizna.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounts',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'component_event'],

    # always loaded
    'data': [
        'demo/cron.xml',
        'demo/demo.xml',
        'security/ir.model.access.csv',
        'views/main_menu.xml',
        'views/ignore_view.xml',
        'views/format_view.xml',
        'views/gateways_view.xml',
        'views/message_view.xml',
        'views/message_moreinfo_view.xml',
        'views/message_template_view.xml',
        'views/payment_view.xml',
        'views/payment_source_view.xml',
        'views/res_config_setting_view.xml',
        #'views/general_assets.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
