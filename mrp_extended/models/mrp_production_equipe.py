# -*- coding: utf-8 -*-

from tracemalloc import start
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class MrpProductionEquipe(models.Model):
    _name = "mrp.production_equipe"
    _description = "MRP production par equipe"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    description = fields.Text("Description")
    team_id = fields.Many2one('mrp.stop.team', string='Equipe', required = True)
    quarter_id = fields.Many2one('mrp.stop.quarter', string='Quart', required = True)
    start_date = fields.Datetime('Date début', help="Date at which you have started bloc production." , required = True)
    end_date = fields.Datetime('Date fin', help="Date at which you will finish to bloc the production." , required = True)
    production_id = fields.Many2one('mrp.production', string='OF', ondelete='cascade')
    product_qty = fields.Float(u'Quantité produit',default=0.0, digits='Product Unit of Measure', required = True, tracking = True)
    user_id = fields.Many2one('res.users', string = u"Responsable",default=lambda self: self.env.user, readonly=True)
    
    _sql_constraints = [
    
        ('date_check2', "CHECK ((start_date <= end_date))", "La date de début doit être antérieure à la date de fin.."),
    ]
   

    @api.onchange('start_date')
    def _onchange_start_date(self):
        for line in self:
            if line.start_date:
                if not line.production_id.start_date:
                    raise UserError(_("you must fill in the start date of the OF"))
                if line.start_date < line.production_id.start_date:
                        line.start_date = False
                        raise UserError(_("A break start date must be between the production period"))
    
    # @api.onchange('end_date')
    # def _onchange_end_date(self):
        # for line in self:
            # if line.end_date:
                # if line.end_date > line.production_id.end_date:
                    # line.end_date = False
                    # raise UserError(_("A break start date must be between the production period"))


