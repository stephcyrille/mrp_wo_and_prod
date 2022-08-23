# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


class MrpWorkcenterProductivity(models.Model):
    _inherit = ['mrp.workcenter.productivity']
    _description = "MRP workcenter productivity extended"

    start_date = fields.Datetime('Start Date', help="Date at which you have started bloc production.")
    end_date = fields.Datetime('End Date', help="Date at which you will finish to bloc the production.")