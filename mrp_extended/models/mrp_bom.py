# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpBomLine(models.Model):
    _inherit = ['mrp.bom.line']
    _description = "MRP Bom line extended"

    product_qty = fields.Float('Quantity', default=1.0, digits=(14, 5),
                               required=True)