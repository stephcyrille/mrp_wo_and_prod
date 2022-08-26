# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpWorkcenterProductivity(models.Model):
    _inherit = ['mrp.workcenter.productivity.loss']
    _description = "MRP workcenter productivity loss extended"

    description = fields.Text("Description")
    start_date = fields.Datetime('Start Date', help="Date at which you have started bloc production.")
    end_date = fields.Datetime('End Date', help="Date at which you will finish to bloc the production.")
    production_id = fields.Many2one('mrp.production', string='Manufacturing Order', ondelete='cascade',
                                    readonly=True)
