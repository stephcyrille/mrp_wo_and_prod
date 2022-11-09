# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MrpDecoupageWizard(models.TransientModel):
    _name = 'mrp.decoupade.wizard'
    _description = 'decoupage wizard'

    lot_id = fields.Many2one('stock.production.lot', string='Lot')
    mrp_id = fields.Many2one('mrp.production', string='MRp')
    location_dest_id = fields.Many2one('stock.location', string='Destination', required=True)
    show_qty = fields.Float(string=u'Quantité')
    # lot_sous_id = fields.Many2one('stock.production.lot', string='Lot enfant')
    product_id = fields.Many2one('product.product', string='Article',readonly=True)
    
    
  
    
    @api.model
    def default_get(self, fields):
        res = super(MrpDecoupageWizard, self).default_get(fields)
        if 'mrp_id' in fields and not res.get('mrp_id') and self._context.get('active_model') == 'mrp.production' and self._context.get('active_id'):
            res['mrp_id'] = self._context['active_id']
        if 'lot_id' in fields :
            res['lot_id'] = self.env['mrp.production'].browse(res['mrp_id']).lot_producing_id
        return res
    
    def process(self):
        for order in self:
            order.mrp_id._create_picking_from_mrp_decoupage(order.show_qty, order.mrp_id,order.location_dest_id)
        return True
