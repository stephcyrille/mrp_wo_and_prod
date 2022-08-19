# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = ['mrp.workorder']
    _description = "MRP Work Order extended"

    def button_start(self):
      self.ensure_one()
      if any(not time.date_end for time in self.time_ids.filtered(lambda t: t.user_id.id == self.env.user.id)):
          return True
      # As button_start is automatically called in the new view
      if self.state in ('done', 'cancel'):
          return True

      all_workorders = self.production_id.workorder_ids
      delay = 0
      for wo in all_workorders:
        if wo.id != self.id:
          record = wo.id
          # print("\n\n RECORD ID IS : %s -> DELAY:  %s\n\n" % (wo.id, delay))
          self.with_delay(priority=0, eta=int(delay*60), 
                            description='Start %s at %s' % (wo.name, 
                              datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                          ).start_work_order(record)
        else:
          record = self.id
          # print("\n\n MY BASE IS ISSS : %s -> DELAY:  %s\n\n" % (self.id, delay))
          self.start_work_order(record)
        # Add delta time after each iteration
        delay += delay + wo.duration_expected

      return True
      
    
    def start_work_order(self, rs_id):
      rs = self.env['mrp.workorder'].browse(rs_id)
      if rs.exists():
        # print("\n\nGOOOOOOOOOOOOOOOOOOOOODDDDDDD\n\n")
        if rs.product_tracking == 'serial':
          rs.qty_producing = 1.0
        else:
          rs.qty_producing = rs.qty_remaining
        
        self.env['mrp.workcenter.productivity'].create(
          rs._prepare_timeline_vals(rs.duration, datetime.now())
        )
        if rs.production_id.state != 'progress':
            rs.production_id.write({
                'date_start': datetime.now(),
            })
        if rs.state == 'progress':
            return True
        start_date = datetime.now()
        vals = {
            'state': 'progress',
            'date_start': start_date,
        }

        if not rs.leave_id:
            leave = self.env['resource.calendar.leaves'].create({
                'name': rs.display_name,
                'calendar_id': rs.workcenter_id.resource_calendar_id.id,
                'date_from': start_date,
                'date_to': start_date + relativedelta(minutes=rs.duration_expected),
                'resource_id': rs.workcenter_id.resource_id.id,
                'time_type': 'other'
            })
            vals['leave_id'] = leave.id
            return rs.write(vals)
        else:
            if rs.date_planned_start > start_date:
                vals['date_planned_start'] = start_date
            if rs.date_planned_finished and rs.date_planned_finished < start_date:
                vals['date_planned_finished'] = start_date
            return rs.write(vals)

      return True
