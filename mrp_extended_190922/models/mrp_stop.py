# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


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
