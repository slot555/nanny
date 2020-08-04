# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from datetime import datetime
from dateutil.relativedelta import relativedelta

class DefData(models.Model):
    _name = 'nanny.def_data'
    _description = 'Базовые данные'

    def_data_sum = fields.Integer(string='Сумма для выплат', required=True)
    def_data_month = fields.Selection(string='Месяц', required=True,
        selection=[('1', 'Январь'),
                   ('2', 'Февраль'),
                   ('3', 'Март'),
                   ('4', 'Апрель'),
                   ('5', 'Май'),
                   ('6', 'Июнь'),
                   ('7', 'Июль'),
                   ('8', 'Август'),
                   ('9', 'Сентябрь'),
                   ('10', 'Октябрь'),
                   ('11', 'Ноябрь'),
                   ('12', 'Декабрь')])
    def_data_year = fields.Selection(string='Год', required=True,
        selection=[('2019', '2019'),
                   ('2020', '2020'),
                   ('2021', '2021')])

    @api.model
    def create(self, values):
        year = values['def_data_year']
        month = values['def_data_month']
        def_data = self.env['nanny.def_data'].search([('def_data_year', '=', year), ('def_data_month', '=', month)])
        if def_data:
            raise ValidationError(_('Запись с такой датой уже существует'))
        else:
            res = super(DefData, self).create(values)
            self.env['nanny.client_data'].check_if_exist_calc_data(False, self)
            return res

    def write(self, values):
        res = super(DefData, self).write(values)
        self.env['nanny.client_data'].check_if_exist_calc_data(False, self)
        return res

    def unlink(self):
        self.env['nanny.client_data'].search([('def_data_year', '=', self.def_data_year), ('def_data_month', '=', self.def_data_month)]).unlink()
        return super(DefData, self).unlink()
