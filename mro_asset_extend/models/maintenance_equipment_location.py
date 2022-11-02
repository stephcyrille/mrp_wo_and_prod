# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools

class MaintenanceEquipmentLocation(models.Model):
    _name = "maintenance.equipment.location"
    _description = "Maintenance equipment location "
    _rec_name = "name"

    code = fields.Char("Code")
    name = fields.Char("Nom du lieu")
    equipment_id = fields.Many2one("maintenance.equipment", string="Equipment")