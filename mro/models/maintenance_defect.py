# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, date


class MaintenanceDefectState(models.Model):
    _name = "maintenance.defect.state"
    _description = "Maintenance defect state "
    _rec_name = "name"

    name = fields.Char("Titre")
    label = fields.Char("Description")
    sequence = fields.Integer("Sequence", default=0)


class MaintenanceDefect(models.Model):
    _name = 'maintenance.defect'
    _description = 'Work Order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _rec_name = "title"

    title = fields.Char('Reférence', required=True, tracking=True)
    description = fields.Text('Description')
    user_id = fields.Many2one('res.users', string="Responsible")
    location = fields.Char('Location', tracking=True)
    department_id = fields.Many2one('hr.department', string="Department")
    state_id = fields.Many2one('maintenance.defect.state', 'State')
    priority = fields.Selection([('0', 'Normal'),('1', 'Good'),('2', 'Very Good'),('3', 'Excellent')],"Priority", default="0")
    creation_date = fields.Date("Creation date", tracking=True, required=True, default=datetime.today(), readonly=True)
    validation_date = fields.Date("Validation date", tracking=True, readonly=True)
    request_date = fields.Date("Request date", tracking=True, readonly=True)

    @api.model
    def create(self, vals):
        res = super(MaintenanceDefect, self).create(vals)
        m_state_obj = self.env['maintenance.defect.state']
        state = m_state_obj.sudo().search([('sequence', '=', 0)])
        if state:
            res.state_id = state.id
        return res
    
    def reset_action(self):
        for val in self:
            m_state_obj = self.env['maintenance.defect.state']
            state = m_state_obj.sudo().search([('sequence', '=', 0)])
            if state:
                val.state_id = state[0].id
                val.validation_date = False
    
    def set_confirmed_action(self):
        for val in self:
            m_state_obj = self.env['maintenance.defect.state']
            state = m_state_obj.sudo().search([('sequence', '=', 1)])
            if state:
                val.state_id = state[0].id
                val.validation_date = date.today().strftime('%Y-%m-%d'),
    
    def create_i_req_action(self):
        for val in self:
            m_state_obj = self.env['maintenance.defect.state']
            state = m_state_obj.sudo().search([('sequence', '=', 2)])
            if state:
                val.state_id = state[0].id
        
