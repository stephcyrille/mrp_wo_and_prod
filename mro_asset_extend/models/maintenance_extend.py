# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools

class MroModeOperatoir(models.Model):
    _name = "maintenance.mode_operatoi"
    _description = "Mode operatoire de la maintenance "
    _rec_name = "name"

    name = fields.Char("Nom du mode")
    label = fields.Char("Description")


class MroOutils(models.Model):
    _name = "maintenance.outil"
    _description = "Les outils de maintenance"
    _rec_name = "name"

    name = fields.Char("Nom outil")
    label = fields.Char("Description")


class MaintenanceEquipmentExtent(models.Model):
    _name = 'maintenance.equipment'
    _inherit = 'maintenance.equipment'

    code = fields.Char('Code', tracking=True, readonly=True, index=True, copy=False, default="New")

    @api.model
    def create(self, vals):
        res = super(MaintenanceEquipmentExtent, self).create(vals)
        res.code = self.env['ir.sequence'].next_by_code("maintenance.equipment") or 'New'
        return res

    def _read_group_state_ids(self, domain, read_group_order=None, access_rights_uid=None, team='3'):
        access_rights_uid = access_rights_uid or self.uid
        stage_obj = self.env['asset.state']
        order = stage_obj._order
        # lame hack to allow reverting search, should just work in the trivial case
        if read_group_order == 'stage_id desc':
            order = "%s desc" % order
        # write the domain
        # - ('id', 'in', 'ids'): add columns that should be present
        # - OR ('team','=',team): add default columns that belongs team
        search_domain = []
        search_domain += ['|', ('team','=',team)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(search_domain, order=order, access_rights_uid=access_rights_uid)
        result = stage_obj.name_get(access_rights_uid, stage_ids)
        # restore order of the search
        result.sort(lambda x,y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))
        return result, {} 
    
    def _read_group_maintenance_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '3')
    
    image = fields.Binary("Image")
    image_small = fields.Binary("Small-sized image")
    image_medium = fields.Binary("Medium-sized image")
    maintenance_state_id = fields.Many2one('asset.state', 'State', domain=[('team','=','3')])
    # maintenance_state_color = fields.Selection(related='maintenance_state_id.state_color', selection=STATE_COLOR_SELECTION, string="Color", readonly=True)
    
    _group_by_full = {

        'maintenance_state_id': _read_group_maintenance_state_ids,

    }
