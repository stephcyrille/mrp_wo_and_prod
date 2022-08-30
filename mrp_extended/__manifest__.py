# -*- coding: utf-8 -*-
{
    'name': "MRP Extension",

    'summary': """
        This is a MRP module addon for extending base MRP module with some 
        specifics element dedicated for daily usage purpose
        """,

    'description': """
        This is a MRP module addon for extending base MRP module with some 
        specifics element dedicated for daily usage purpose
    """,

    'author': "Open Engineering",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'All',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'queue_job'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_production.xml',
        'views/mrp_stop_type.xml',
        'views/mrp_stop_reason.xml',
        'views/mrp_equipment.xml',
        'views/mrp_stop.xml',
        'views/mrp_production_pivot_views.xml',
        #'views/mrp_workorder.xml',

        'report/mrp_report_view_extended.xml',
        'report/mrp_production_template_before.xml',
        'report/mrp_production_template_after.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
