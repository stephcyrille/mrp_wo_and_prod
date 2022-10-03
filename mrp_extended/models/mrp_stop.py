# -*- coding: utf-8 -*-

from tracemalloc import start
from odoo import api, fields, models, _
from odoo.exceptions import UserError


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
    team_id = fields.Many2one('mrp.stop.team', string='Team')
    quarter_id = fields.Many2one('mrp.stop.quarter', string='Quarter')
    start_date = fields.Datetime('Start Date', help="Date at which you have started bloc production.")
    end_date = fields.Datetime('End Date', help="Date at which you will finish to bloc the production.")
    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', ondelete='cascade')

    @api.onchange('start_date')
    def _onchange_start_date(self):
        for line in self:
            if line.start_date:
                if line.start_date < line.production_id.start_date:
                        line.start_date = False
                        raise UserError(_("A break start date must be between the production period"))
    
    @api.onchange('end_date')
    def _onchange_end_date(self):
        for line in self:
            if line.end_date:
                if line.end_date > line.production_id.end_date:
                    line.end_date = False
                    raise UserError(_("A break start date must be between the production period"))

    # @api.model
    # def create(self, vals):
    #   res = super(MrpStop, self).create(vals)
    #   if res.production_id.start_date and res.production_id.end_date:
    #     if res.start_date:
    #       if res.start_date < res.production_id.start_date or res.start_date > res.production_id.end_date:
    #         raise UserError(_("Your break start date must be between the production period."))
    #       else:
    #         return res
    #     elif res.end_date:
    #       if res.end_date < res.production_id.start_date or res.end_date > res.production_id.end_date:
    #         raise UserError(_("Your break end date must be between the production period."))
    #       else:
    #         return res
    #     else:
    #       return res
    #   else:
    #     raise UserError(_("Your must first set the production period"))
    
    # @api.model
    # def write(self, vals):
    #   res = super(MrpStop, self).write(vals)
    #   if self.production_id.start_date and self.production_id.end_date:
    #     if self.start_date:
    #       if self.start_date > self.production_id.start_date and self.start_date < self.production_id.end_date:
    #         return res
    #       else:
    #         raise UserError(_("Your break end date must be betwenn the production period."))
    #     if self.end_date:
    #       if self.end_date > self.production_id.start_date and self.end_date < self.production_id.end_date:
    #         return res
    #       else:
    #         raise UserError(_("Your break end date must be betwenn the production period."))
    #   else:
    #     raise UserError(_("Your must first set the production period"))
