# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools


class MroModeOperatoir(models.Model):
    _name = "maintenance.team.state"
    _description = "Maintenance team state "
    _rec_name = "name"

    name = fields.Char("Titre")
    label = fields.Char("Description")
    isFinal = fields.Boolean("Etat final", default=False)


class MaintenanceTeam(models.Model):
    _inherit = 'maintenance.team'

    state_id = fields.Many2one('maintenance.team.state', 'State')

    # @api.model
    # def create(self, vals):
    #     res = super(MaintenanceTeam, self).create(vals)
    #     res.code = self.env['ir.sequence'].next_by_code("maintenance.equipment") or 'New'
    #     return res