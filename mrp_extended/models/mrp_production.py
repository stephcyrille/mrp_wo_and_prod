# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = ['mrp.production']
    _description = "MRP production extended"

    def action_launch_wo(self):
        if any(wo.state == 'done' for wo in self.workorder_ids):
            raise UserError(_("Some work orders are already done, you cannot launch all the WO of "
                              "this manufacturing order."))
        elif any(wo.state == 'progress' for wo in self.workorder_ids):
            raise UserError(_("Some work orders have already started, you cannot launch all the WO of "
                              "this manufacturing order."))
