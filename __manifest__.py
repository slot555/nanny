# -*- coding: utf-8 -*-
{
    'name': "nanny",

    'summary': """nanny""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'application': True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'sequence': 3,

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_setup', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/client.xml',
        'views/baby.xml',
        'views/def_data.xml',
        'views/client_data.xml',
        'views/fop.xml',
        'views/month_report.xml',
        'views/data_import.xml',
    ],
}
