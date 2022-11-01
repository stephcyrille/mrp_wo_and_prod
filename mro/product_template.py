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

    isParts = fields.Boolean('Est une pièce')
    kind_of_part = fields.Selection([('generic', 'Générique'), ('specific', 'Spécifique')], 
                                    string='Kind part', default='generic')
    equipment = fields.Many2one("maintenance.equipment", string='Equipement')
    vendor_ref = fields.Char("Reférence du fournisseur")
    manufactor = fields.Char("Fabricant")
    isTools = fields.Boolean('Est un outil')
    maintenance_plan_id = fields.Many2one("maintenance.plan")
    wo_id = fields.Many2one("mro.task")
