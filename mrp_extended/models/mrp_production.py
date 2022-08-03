# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = ['mrp.production']
    _description = "MRP production extended"

    def action_launch_wo(self):
        self.ensure_one()
        if any(wo.state == 'done' for wo in self.workorder_ids):
            raise UserError(_("Some work orders are already done, you cannot launch all the WO of "
                              "this manufacturing order."))
        elif any(wo.state == 'progress' for wo in self.workorder_ids):
            raise UserError(_("Some work orders have already started, you cannot launch all the WO of "
                              "this manufacturing order."))

        # Launch multiples work orders here
        for wo in self.workorder_ids:
            if any(not time.date_end for time in wo.time_ids.filtered(lambda t: t.user_id.id == self.env.user.id)):
                return True
            # As button_start is automatically called in the new view
            if wo.state in ('done', 'cancel'):
                return True

            if wo.product_tracking == 'serial':
                wo.qty_producing = 1.0
            else:
                wo.qty_producing = wo.qty_remaining

            self.env['mrp.workcenter.productivity'].create(
                wo._prepare_timeline_vals(wo.duration, datetime.now())
            )

            if self.state != 'progress':
                self.write({
                    'date_start': datetime.now(),
                })
                # print("\n\tDANS PROGRESS \n\n")

            if wo.state == 'progress':
                return True

            start_date = datetime.now()
            vals = {
                'state': 'progress',
                'date_start': start_date,
                "working_state": "done",
                "is_user_working": True
            }

            if not wo.leave_id:
                leave = self.env['resource.calendar.leaves'].create({
                    'name': wo.display_name,
                    'calendar_id': wo.workcenter_id.resource_calendar_id.id,
                    'date_from': start_date,
                    'date_to': start_date + relativedelta(minutes=wo.duration_expected),
                    'resource_id': wo.workcenter_id.resource_id.id,
                    'time_type': 'other'
                })
                vals['leave_id'] = leave.id
                wo.write(vals)
            else:
                if wo.date_planned_start > start_date:
                    vals['date_planned_start'] = start_date
                if wo.date_planned_finished and wo.date_planned_finished < start_date:
                    vals['date_planned_finished'] = start_date
                wo.write(vals)

        return True
