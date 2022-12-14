# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2013-2020 CodUP (<http://codup.com>).
#
##############################################################################

{
    'name': 'MRO',
    'version': '1.10',
    'summary': 'Asset Maintenance, Repair and Operation',
    'description': """
Manage Maintenance process in OpenERP
=====================================

Asset Maintenance, Repair and Operation.
Support Breakdown Maintenance and Corrective Maintenance.

Main Features
-------------
    * Request Service/Maintenance Management
    * Maintenance Orders Management
    * Work Orders Management (group MO)
    * Parts Management
    * Tasks Management (standard job)
    * Convert Maintenance Order to Task
    * Print Maintenance Order
    * Print Maintenance Request

Required modules:
    * asset
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'license': 'AGPL-3',
    'category': 'Industries',
    'sequence': 0,
    'depends': ['asset','purchase','maintenance_plan'],
    'demo': ['mro_demo.xml'],
    'data': [
        'security/mro_security.xml',
        'security/ir.model.access.csv',
        'wizard/reject_view.xml',
        'wizard/convert_order.xml',
        'asset_view.xml',
        'product_view.xml',
        'mro_sequence.xml',
        'mro_data.xml',
        'mro_view.xml',
        'mro_report.xml',
        'views/report_mro_order.xml',
        'views/report_mro_request.xml',
        'views/mro_workorder_view.xml',
        'views/mro_product.xml',
        'views/maintenance_defect_views.xml',
    ],
    'application': True,
}
