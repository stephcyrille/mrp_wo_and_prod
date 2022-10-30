# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpTeam(models.Model):
  _name = "mrp.stop.team"
  _description = "MRP Team"

  code = fields.Char("Code")
  name = fields.Char("Name")
  employee_id = fields.Many2one('hr.employee', string='Manager', ondelete='cascade', required=True)
  start_date = fields.Datetime('Start Date', help="Date at which you will start assign team to the production stop.")
  end_date = fields.Datetime('End Date', help="Date at which you will finish assign team to the production stop.")
  member_ids = fields.Many2many('hr.employee', string='Members')


class MrpQuarter(models.Model):
  _name = "mrp.stop.quarter"
  _description = "MRP Quarter"

  code = fields.Char("Code")
  name = fields.Char("Name")