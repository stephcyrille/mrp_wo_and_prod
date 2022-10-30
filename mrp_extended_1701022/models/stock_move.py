# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = ['stock.move']
    _description = "Stock move extended"

    product_uom_qty = fields.Float(
        'Demand',
        digits=(14, 5),
        default=1.0, required=True, states={'done': [('readonly', True)]},
        help="This is the quantity of products from an inventory "
             "point of view. For moves in the state 'done', this is the "
             "quantity of products that were actually moved. For other "
             "moves, this is the quantity of product that is planned to "
             "be moved. Lowering this quantity does not generate a "
             "backorder. Changing this quantity on assigned moves affects "
             "the product reservation, and should be done with care.")
    quantity_done = fields.Float('Quantity Done', compute='_quantity_done_compute', digits=(14, 5),
                                 inverse='_quantity_done_set')
    forecast_availability = fields.Float('Forecast Availability', compute='_compute_forecast_information',
                                         digits=(14, 5), compute_sudo=True)
