# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Baby(models.Model):
    _name = 'nanny.baby'
    _description = 'Baby'

    name = fields.Char(string="Имя ребенка:", required=True, index=True)
    birthday = fields.Date(string="Дата рождения:")
    mother = fields.Many2one(comodel_name='nanny.client', string="Родитель:", ondelete='cascade', auto_join=True)
    end_date = fields.Date(compute='_compute_end_date', string="Дата окончания услуг:")
    month_till_end_date = fields.Integer(compute='_compute_month_till_end_date', string="Месяцев до окончания:")

    def _compute_end_date(self):
        for rec in self:
            date_start_dt = fields.Datetime.from_string(rec.birthday)
            dt = date_start_dt + relativedelta(years=3)
            rec.end_date = fields.Datetime.to_string(dt)

    def _compute_month_till_end_date(self):
        for rec in self:
            cur_date = datetime.now()
            rec.month_till_end_date = (rec.end_date.year - cur_date.year) * 12 + rec.end_date.month - cur_date.month




