# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = ['mrp.production']
    _description = "MRP production extended"

    start_date = fields.Datetime('Start Date', help="Date at which you really start the production.")
    end_date = fields.Datetime('End Date', help="Date at which you will finish the production.")
    duration = fields.Char(
        'Duration', compute='_compute_duration', readonly=True, store=True, copy=False)
    block_reasons_ids = fields.One2many('mrp.stop', 'production_id', 'Stop reasons')

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.duration = rec.end_date - rec.start_date
            else:
                rec.duration = False

    def action_confirm(self):
        self._check_company()
        for production in self:
            # if not production.start_date:
            #     raise UserError(_("You cannot proceed! Production start date is mandatory."))
            # if not production.end_date:
            #     raise UserError(_("You cannot proceed! Production end date is mandatory."))
            # if production.end_date < production.start_date:
            #     raise UserError(_("The production start date must not be greater than the production end date."))
            if len(production.block_reasons_ids) > 0:
                for bR in production.block_reasons_ids:
                    if production.start_date and production.end_date:
                        if bR.start_date is False or bR.end_date is False: 
                            raise UserError(_("Stop Reason Error: Your must define the break line period"))
                        if bR.start_date:
                            if bR.start_date > production.start_date and bR.start_date < production.end_date:
                                return True
                            else:
                                raise UserError(_("Stop Reason Error: Your break end date must be betwenn the production period."))
                        if bR.end_date:
                            if bR.end_date > production.start_date and bR.end_date < production.end_date:
                                return True
                            else:
                                raise UserError(_("Stop Reason Error: Your break end date must be betwenn the production period."))
                    else:
                        raise UserError(_("Stop Reason Error: Your must first set the production period"))

            if production.bom_id:
                production.consumption = production.bom_id.consumption
            # In case of Serial number tracking, force the UoM to the UoM of product
            if production.product_tracking == 'serial' and production.product_uom_id != production.product_id.uom_id:
                production.write({
                    'product_qty': production.product_uom_id._compute_quantity(production.product_qty, production.product_id.uom_id),
                    'product_uom_id': production.product_id.uom_id
                })
                for move_finish in production.move_finished_ids.filtered(lambda m: m.product_id == production.product_id):
                    move_finish.write({
                        'product_uom_qty': move_finish.product_uom._compute_quantity(move_finish.product_uom_qty, move_finish.product_id.uom_id),
                        'product_uom': move_finish.product_id.uom_id
                    })
            production.move_raw_ids._adjust_procure_method()
            (production.move_raw_ids | production.move_finished_ids)._action_confirm(merge=False)
            production.workorder_ids._action_confirm()
        # run scheduler for moves forecasted to not have enough in stock
        self.move_raw_ids._trigger_scheduler()
        self.picking_ids.filtered(
            lambda p: p.state not in ['cancel', 'done']).action_confirm()
        # Force confirm state only for draft production not for more advanced state like
        # 'progress' (in case of backorders with some qty_producing)
        self.filtered(lambda mo: mo.state == 'draft').state = 'confirmed'
        return True

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
