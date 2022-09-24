# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

class MrpStopType(models.Model):
    _name = "mrp.stop.type"
    _description = "MRP Stop Type"
    _rec_name = "name"

    name = fields.Char("Name")
    label = fields.Char("Label")


class MrpStopReason(models.Model):
    _name = "mrp.stop.reason"
    _description = "MRP Stop reason"
    _rec_name = "name"

    name = fields.Char("Name")
    label = fields.Char("Label")


class MrpStop(models.Model):
    _name = "mrp.stop"
    _description = "MRP Stop"

    stop_type_id = fields.Many2one('mrp.stop.type', string='Type', ondelete='cascade', required=True)
    stop_reason_id = fields.Many2one('mrp.stop.reason', string='Reason', ondelete='cascade', required=True)
    description = fields.Text("Description")
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', ondelete='cascade', required=True)
    start_date = fields.Datetime('Start Date', help="Date at which you have started bloc production.")
    end_date = fields.Datetime('End Date', help="Date at which you will finish to bloc the production.")
    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', ondelete='cascade')
    intervention_id = fields.Many2one('maintenance.request', string="Demande d'intevention" )
    
    _sql_constraints = [
    
        ('date_check2', "CHECK ((start_date <= end_date))", "La date de début doit être antérieure à la date de fin.."),
    ]
    
    # @api.constrains('start_date', 'end_date', 'equipment_id', 'intervention_id')
    # def _check_date(self):
        # for order in self:
            # nholidays =' '
            # domain = [
                # ('end_date', '<=', order.production_id.end_date),
                # ('start_date', '>=', order.production_id.start_date),
            # ]
            # nholidays = order.production_id.search_count(domain)
            # if not nholidays:
                # raise ValidationError(_("La periode raison d'arret doit etre dans la periode de l'ordre de fabrication."))
                
    # @api.onchange('start_date')
    # def onchange_date_start(self):
        # if self.start_date and self.production_id.start_date and self.production_id.end_date:
            # print ('je suit la ')
            # if self.production_id.start_date >= self.start_date and self.start_date <= self.production_id.end_date:
                # raise ValidationError(_("La periode raison d'arret doit etre dans la periode de l'ordre de fabrication."))
                
            # if self.start_date <= self.production_id.end_date:
                # raise ValidationError(_("La periode raison d'arret doit etre dans la periode de l'ordre de fabrication."))
                
    # @api.onchange('end_date')
    # def onchange_date_end(self):
        # if self.end_date and self.production_id.start_date and self.production_id.end_date:
            # if self.production_id.start_date <= self.end_date <=  self.production_id.end_date:
                # raise ValidationError(_("La periode raison d'arret doit etre dans la periode de l'ordre de fabrication."))