# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MonthReport(models.TransientModel):
    _name = 'nanny.month_report'
    _description = 'Month report'

    def_data_month = fields.Selection(string='Месяц', required=True,
                                      selection=[('1', 'Январь'), ('2', 'Февраль'), ('3', 'Март'),
                                                 ('4', 'Апрель'), ('5', 'Май'), ('6', 'Июнь'),
                                                 ('7', 'Июль'), ('8', 'Август'), ('9', 'Сентябрь'),
                                                 ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь')])
    def_data_year = fields.Selection(string='Год', required=True,
                                     selection=[('2019', '2019'), ('2020', '2020'), ('2021', '2021')])
    client_datas = fields.One2many(comodel_name='nanny.client_data', string="", compute='_compute_client_datas')

    @api.depends('def_data_year', 'def_data_month')
    def _compute_client_datas(self):
        records = self.env['nanny.client_data'].search([('def_data_year', '=', self.def_data_year),
                                                        ('def_data_month', '=', self.def_data_month),
                                                        ('client.is_active', '=', True)])
        self.client_datas = records

    def print_report(self):
        return self.env.ref('nanny.nanny_clients_month_statistic').report_action(self)