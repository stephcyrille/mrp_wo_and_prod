# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2017-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    isParts = fields.Boolean('Can be Part')
    kind_of_part = fields.Selection([('generic', 'Generic'), ('specific', 'Specific')], 
                                    string='Kind part', default='generic')
    equipment = fields.Many2one("maintenance.equipment", string='Equipment')
    vendor_ref = fields.Char("Vendor reference")
    manufactor = fields.Char("Manufactor")
    isTools = fields.Boolean('Can be a tool')
