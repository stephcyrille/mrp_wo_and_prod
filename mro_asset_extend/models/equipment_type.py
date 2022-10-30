# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceEquipmentType(models.Model):
  _name = "maintenance.equipment.type"
  _description = "Maintenance equipment type "
  _rec_name = "name"

  name = fields.Char("Name", required=True)
  label = fields.Char("Description")