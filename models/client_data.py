# -*- coding: utf-8 -*-
from odoo import models, fields, api

class СlientData(models.Model):
    _name = 'nanny.client_data'
    _description = 'Client_data'

    client = fields.Many2one(comodel_name='nanny.client', string="client", ondelete='cascade')
    def_data_year = fields.Char(string="Год")
    def_data_month = fields.Char(string="Месяц")
    def_sum = fields.Integer(string='Базовая сумма')
    calc_data_babies_count_by_date = fields.Integer(compute='_compute_calc_data_babies_count_by_date',
                                                    string="Кол-во детей по дате", store=False)

    @api.depends('client')
    def _compute_calc_data_babies_count_by_date(self):
        for rec in self:
            babies_count = 0
            for baby in rec.client.babies:
                start_date_float = baby.birthday.year + baby.birthday.month / 100  # 2020,04
                cur_data_date_float = float(rec.def_data_year) + float(rec.def_data_month) / 100  # 2020,03
                end_date_float = baby.end_date.year + baby.end_date.month / 100  # 2021,04
                if start_date_float <= cur_data_date_float <= end_date_float:
                    babies_count += 1
            rec.calc_data_babies_count_by_date = babies_count

    calc_data_count_childs_by_date = fields.Integer(compute='_compute_calc_data_count_childs_by_date',
                                                    string="Кол-во приведенных по дате", store=False)

    @api.depends('client', 'calc_data_babies_count_by_date')
    def _compute_calc_data_count_childs_by_date(self):
        for rec in self:
            count_childs = 0
            for child in rec.client.child_ids:
                start_date_float = child.add_date.year + child.add_date.month / 100
                cur_data_date_float = float(rec.def_data_year) + float(rec.def_data_month) / 100
                if start_date_float <= cur_data_date_float and child.is_active:
                    count_childs += 1
            rec.calc_data_count_childs_by_date = count_childs

    calc_data_babies_count_childs_by_date = fields.Integer(compute='_compute_calc_data_babies_count_childs_by_date',
                                                           string="Кол-во детей у приведенных по дате", store=False)

    @api.depends('client', 'calc_data_count_childs_by_date')
    def _compute_calc_data_babies_count_childs_by_date(self):
        for rec in self:
            count_babies_childs = 0
            for child in rec.client.child_ids:
                start_date_float = child.add_date.year + child.add_date.month / 100
                cur_data_date_float = float(rec.def_data_year) + float(rec.def_data_month) / 100
                if start_date_float <= cur_data_date_float and child.is_active:
                    for baby in child.babies:
                        baby_start_date_float = baby.birthday.year + baby.birthday.month / 100
                        end_date_float = baby.end_date.year + baby.end_date.month / 100
                        if baby_start_date_float <= cur_data_date_float <= end_date_float:
                            count_babies_childs += 1
            rec.calc_data_babies_count_childs_by_date = count_babies_childs

    payments_sum = fields.Integer(compute='_compute_payments_sum', string='Сумма выплат')
    return_sum = fields.Integer(compute='_compute_return_sum', string='Сумма возврата')

    @api.depends('client')
    def _compute_payments_sum(self):
        for rec in self:
            rec.payments_sum = rec.calc_data_babies_count_by_date * rec.def_sum

    @api.depends('payments_sum', 'client')
    def _compute_return_sum(self):
        for rec in self:
            rec.return_sum = rec.calc_data_babies_count_by_date * (rec.def_sum / 2 + 100) - rec.calc_data_babies_count_childs_by_date * 100

    def check_if_exist_calc_data(self, client=False, def_data=False):
        if not client:
            client = self.env['nanny.client'].search([])
        if not def_data:
            def_data = self.env['nanny.def_data'].search([])
        for cli in client:
            for data in def_data:
                client_data = self.env['nanny.client_data'].search([('client', '=', cli.id),
                                                                    ('def_data_year', '=', data.def_data_year),
                                                                    ('def_data_month', '=', data.def_data_month)])
                if not client_data:
                    self.create_new_calc_data(cli, data)
                else:
                    if client_data.def_sum != data.def_data_sum:
                        client_data.write({'def_sum': data.def_data_sum})
                    self.check_if_delete_calc_data(cli, data, client_data)

    def create_new_calc_data(self, client, def_data):
        start_date_float = client.add_date.year + client.add_date.month / 100
        cur_data_date_float = float(def_data.def_data_year) + float(def_data.def_data_month) / 100
        if start_date_float <= cur_data_date_float:
            values = {
                'client': client.id,
                'def_data_year': def_data.def_data_year,
                'def_data_month': def_data.def_data_month,
                'def_sum': def_data.def_data_sum,
            }
            self.env['nanny.client_data'].create(values)

    def check_if_delete_calc_data(self, client, def_data, client_data):
        start_date_float = client.add_date.year + client.add_date.month / 100
        cur_data_date_float = float(def_data.def_data_year) + float(def_data.def_data_month) / 100
        if start_date_float > cur_data_date_float:
            client_data.unlink()


