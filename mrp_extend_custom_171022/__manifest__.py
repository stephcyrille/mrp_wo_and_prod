# -*- coding: utf-8 -*-
{
    'name': "MRP DECOUPAGE EXTEND",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "open engineering",
    'website': "http://www.openengineering.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Industries',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/mrp_decoupage_views.xml',
        'views/mrp_decoupage_extend.xml',
        
    ],
}