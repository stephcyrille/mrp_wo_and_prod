# -*- coding: utf-8 -*-

from odoo import  _, api, fields, models
from odoo import tools

from odoo.exceptions import UserError, ValidationError

class MrpProduction(models.Model):
    _inherit = ['mrp.production']
    # _description = "MRP production extended"


    decoupage_ids = fields.One2many('mrp.decoupege_execut', 'production_id', 'Stop reasons')
    qty_decoupage = fields.Float("Qte executer")
    
    
    def _prepare_picking_vals(self,mrp, picking_type, location_id, location_dest_id):
        return {
            'partner_id':  False,
            'user_id': False,
            'origin': mrp.name,
            'picking_type_id': picking_type.id,
            'move_type': 'direct',
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
        }
    
    
    
    def _prepare_stock_move_vals(self, qty,mrp,picking, location_dest_id,location_id):
        return {
            'name': mrp.name,
            'product_uom': mrp.product_id.uom_id.id,
            'picking_id': picking.id,
            'picking_type_id': mrp.picking_type_id.id,
            'product_id': mrp.product_id.id,
            'product_uom_qty': abs(qty),
            'state': 'draft',
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
            'company_id': self.company_id.id,
            # 'lot_id': mrp.lot_producing_id.id,
        }
    
    def action_generate_serial(self):
        # self.ensure_one()
        nbr = 1
        lot_sous_id = self.env['stock.production.lot'].create({
            'product_id': self.product_id.id,
            'company_id': self.company_id.id,
            'ref': self.lot_producing_id.name,
            'name': self.lot_producing_id.name +'/S00/'+ str(nbr + len(self.decoupage_ids))
        })
        return lot_sous_id
    
    @api.model
    def _create_picking_from_mrp_decoupage(self, qty, mrp,location_dest):
        """We'll create some picking based on order_lines"""
        qte = 0
        product_qty = self.product_qty
        for order in self.decoupage_ids:
            qte += order.qty_decoupage
            if qte + qty > product_qty:
                raise UserError(_(u"La quantité déjà produite est supérieure a la quantité de OF planifié"))
        pickings = self.env['stock.picking']
        # virtual_location = self.env['stock.location'].search([('usage','=',production)],limit=1)
        # if virtual_location:
            # virtual_location_source = virtual_location
            # virtual_location_dest = mrp.location_dest_id
        lot= self.action_generate_serial()
        print ('le lot la est',lot.name)
        # lot= 37
        if qty > 0:
            virtual_location = self.env['stock.location'].search([('usage','=','production')],limit=1)
            # if virtual_location:
            virtual_location_source = virtual_location
            virtual_location_dest = mrp.location_dest_id
        
            location_id = mrp.location_dest_id
            if location_dest:
                location_dest_id = location_dest
            else:
                location_dest_id = mrp.location_dest_id
            picking_type = mrp.picking_type_id
            
            
            
            virtual_positive_picking = self.env['stock.picking'].create(self._prepare_picking_vals( mrp,picking_type, virtual_location_source, virtual_location_dest))
            virtual_current_move = self.env['stock.move'].create(self._prepare_stock_move_vals(qty,mrp,virtual_positive_picking, virtual_location_dest,virtual_location_source))
            virtual_confirmed_moves = virtual_current_move._action_confirm()
            
            for move in virtual_confirmed_moves:
                ml_vals = move._prepare_move_line_vals()
                ml_vals.update({'qty_done':qty})
                # existing_lot = mrp.lot_producing_id
                existing_lot = lot
                quant = existing_lot.quant_ids.filtered(lambda q: q.quantity > 0.0 and q.location_id.parent_path.startswith(move.location_id.parent_path))[-1:]
                ml_vals.update({
                    'lot_id': existing_lot.id,
                    'location_id': quant.location_id.id or move.location_id.id
                })   
                self.env['stock.move.line'].create(ml_vals)
            virtual_positive_picking._action_done()
            
            # decoupage = self.env['mrp.decoupege_execut'].create(self._prepare_line_execute( mrp,virtual_positive_picking,qty,virtual_location_dest))
            pickings |= virtual_positive_picking
            
            
            positive_picking = self.env['stock.picking'].create(self._prepare_picking_vals( mrp,picking_type, location_id, location_dest_id))
            current_move = self.env['stock.move'].create(self._prepare_stock_move_vals(qty,mrp,positive_picking, location_dest_id,location_id))
            confirmed_moves = current_move._action_confirm()
            
            for move in confirmed_moves:
                ml_vals = move._prepare_move_line_vals()
                ml_vals.update({'qty_done':qty})
                # existing_lot = mrp.lot_producing_id
                existing_lot = lot
                quant = existing_lot.quant_ids.filtered(lambda q: q.quantity > 0.0 and q.location_id.parent_path.startswith(move.location_id.parent_path))[-1:]
                ml_vals.update({
                    'lot_id': existing_lot.id,
                    'location_id': quant.location_id.id or move.location_id.id
                })   
                self.env['stock.move.line'].create(ml_vals)
            positive_picking._action_done()
            
            decoupage = self.env['mrp.decoupege_execut'].create(self._prepare_line_execute( mrp,positive_picking,qty,location_dest_id,existing_lot))
            pickings |= positive_picking
        return pickings
    
    # @api.model
    # def _create_picking_from_mrp_decoupage(self, qty, mrp,location_dest):
        # """We'll create some picking based on order_lines"""
        # qte = 0
        # product_qty = self.product_qty
        # for order in self.decoupage_ids:
            # qte += order.qty_decoupage
            # if qte + qty > product_qty:
                # raise UserError(_(u"La quantité déjà produite est supérieure a la quantité de OF planifié"))
        # pickings = self.env['stock.picking']
        # if qty > 0:
            # location_id = mrp.location_dest_id
            # if location_dest:
                # location_dest_id = location_dest
            # else:
                # location_dest_id = mrp.location_dest_id
            # picking_type = mrp.picking_type_id
            
            # positive_picking = self.env['stock.picking'].create(self._prepare_picking_vals( mrp,picking_type, location_id, location_dest_id))
            # current_move = self.env['stock.move'].create(self._prepare_stock_move_vals(qty,mrp,positive_picking, location_dest_id,location_id))
            # confirmed_moves = current_move._action_confirm()
            
            # for move in confirmed_moves:
                # ml_vals = move._prepare_move_line_vals()
                # ml_vals.update({'qty_done':qty})
                # existing_lot = mrp.lot_producing_id
                # quant = existing_lot.quant_ids.filtered(lambda q: q.quantity > 0.0 and q.location_id.parent_path.startswith(move.location_id.parent_path))[-1:]
                # ml_vals.update({
                    # 'lot_id': existing_lot.id,
                    # 'location_id': quant.location_id.id or move.location_id.id
                # })   
                # self.env['stock.move.line'].create(ml_vals)
            # positive_picking._action_done()
            
            # decoupage = self.env['mrp.decoupege_execut'].create(self._prepare_line_execute( mrp,positive_picking,qty,location_dest_id))
            # pickings |= positive_picking
        # return pickings
    
    # @api.onchange('start_date')
    def action_execu_tionpartiel(self):
        for line in self:
            # if line.start_date:
                # if line.start_date < line.production_id.start_date:
                        # line.start_date = False
                        # raise UserError(_("A break start date must be between the production period"))
            return True

    def action_send_to_draft(self):
        for production in self:
            production.write({'state': 'draft',})
    
    def _prepare_line_execute(self,mrp, picking, qty,location_dest_id,existing_lot):
        return {
            'production_id':  mrp.id,
            'picking_id': picking.id,
            'qty_decoupage': qty,
            'lot_id': existing_lot.id,
            'location_dest_id': location_dest_id.id,
        }
    
class MrpEquipmentExtent(models.Model):
    _name = 'mrp.decoupege_execut'
    # _inherit = 'maintenance.equipment'
    
    
    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', ondelete='cascade')
    picking_id = fields.Many2one('stock.picking', string="Mouvenment" )
    user_id = fields.Many2one('res.users', string = u"Responsable",default=lambda self: self.env.user)
    qty_decoupage = fields.Float("Qte executer")
    lot_id = fields.Many2one('stock.production.lot', string="Lot" )
    location_dest_id = fields.Many2one('stock.location', string='Destination', required=False)