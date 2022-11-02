# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
import time
import logging

_logger = logging.getLogger(__name__)


class MaintenanceDefectState(models.Model):
    _name = "maintenance.defect.state"
    _description = "Maintenance defect state "
    _rec_name = "name"

    name = fields.Char("Titre")
    label = fields.Char("Description")
    sequence = fields.Integer("Sequence", default=0)
    maintenance_defect_ids = fields.Many2many("maintenance.defect", 'maintenance_defect_state_rel', "state_id", default=0)
    is_last = fields.Boolean(default=False)


class MaintenanceDefect(models.Model):
    _name = 'maintenance.defect'
    _description = 'Work Order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _rec_name = "title"

    title = fields.Char('Nom anomalie', required=True, tracking=True)
    description = fields.Text('Description')
    from_user_id = fields.Many2one('res.users', string="Responsable emetteur")
    to_user_id = fields.Many2one('res.users', string="Responsable destination")
    location_id = fields.Many2one('maintenance.equipment.location', string="Lieu de l'anomalie")
    is_lock = fields.Boolean(default=False)
    from_department_id = fields.Many2one('hr.department', string="Unité demandeur")
    to_department_id = fields.Many2one('hr.department', string="unité de destination")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipement", required=True)
    state_id = fields.Many2one('maintenance.defect.state', 'State')
    priority = fields.Selection([('0', 'Normal'),('1', 'Good'),('2', 'Very Good'),('3', 'Excellent')],"Priority", default="0")
    creation_date = fields.Datetime("Creation date", tracking=True, required=True, default=datetime.today(), readonly=True)
    validation_date = fields.Datetime("Validation date", tracking=True, readonly=True)
    request_date = fields.Datetime("Request date", tracking=True, readonly=True)

    @api.model
    def create(self, vals):
        res = super(MaintenanceDefect, self).create(vals)
        m_state_obj = self.env['maintenance.defect.state']
        state = m_state_obj.sudo().search([('sequence', '=', 0)])
        if state:
            res.state_id = state.id
        return res

    # @api.model
    def write(self, vals):
        res = super(MaintenanceDefect, self).write(vals)
        m_state_obj = self.env['maintenance.defect.state']
        try:
            if vals['state_id']:
                state = m_state_obj.sudo().search([('id', '=', vals['state_id'])])
                if state:
                    if 0 == state.sequence: 
                        values = {
                            'state_id': vals['state_id'],
                            'validation_date': False,
                            'request_date': False,
                            'is_lock': False
                        }
                        res = super(MaintenanceDefect, self).write(values)
                        return res 
                    elif 1 == state.sequence: 
                        values = {
                            'state_id': vals['state_id'],
                            'validation_date': time.strftime('%Y-%m-%d %H:%M:%S'),  
                        }
                        res = super(MaintenanceDefect, self).write(values)
                        return res 
                    if state.is_last: 
                        source = '%s - %s' % (self.id, self.title)
                        name = '%s - %s' % (self.equipment_id.name, self.title)
                        self.env['maintenance.request'].create({'source_document': source, 'name': name})
                        values = {
                            'state_id': vals['state_id'],
                            'request_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'is_lock': True
                        }
                        res = super(MaintenanceDefect, self).write(values)
                        return res 
        except Exception as e:
            pass    
        return res
