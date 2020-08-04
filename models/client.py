# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Сlient(models.Model):
    _name = 'nanny.client'
    _description = 'Client'

    name = fields.Char(string="Имя клиента", required=True, index=True)
    add_date = fields.Date(required=True, string="Начало предоставления услуг")
    parent_id = fields.Many2one(comodel_name='nanny.client', string="Кто привел", ondelete='restrict',
                                auto_join=False, required=False, index=True)
    child_ids = fields.One2many(comodel_name='nanny.client', inverse_name='parent_id', string="Кого привел",
                                auto_join=False, required=False, copy=False)
    count_child_ids = fields.Integer(compute='_compute_count_childs', string="Кол-во приведенных")

    @api.depends('child_ids')
    def _compute_count_childs(self):
        for record in self:
            count = 0
            for child in record.child_ids:
                if child.is_active:
                    count += 1
            record.count_child_ids = count

    babies = fields.One2many(comodel_name='nanny.baby', inverse_name='mother', string="Имя ребенка", index=True)
    babies_count = fields.Integer(compute='_compute_babies_count', string="Кол-во детей")

    @api.depends('babies')
    def _compute_babies_count(self):
        for record in self:
            record.babies_count = len(record.babies)

    babies_count_child_ids = fields.Integer(compute='_compute_babies_count_child_ids', string="Кол-во детей у приведенных")

    @api.depends('child_ids')
    def _compute_babies_count_child_ids(self):
        for record in self:
            record.babies_count_child_ids = len(record.child_ids.babies)

    babies_end_month_count = fields.Integer(compute='_compute_babies_end_month_count', string="Месяцев осталось")

    @api.depends('babies')
    def _compute_babies_end_month_count(self):
        for record in self:
            for rec in record.babies:
                if not record.babies_end_month_count or rec.month_till_end_date < record.babies_end_month_count:
                    record.babies_end_month_count = rec.month_till_end_date
            if not record.babies_end_month_count:
                record.babies_end_month_count = 0
            if record.babies_end_month_count < 3 and record.kanban_state != 'normal':
                record.kanban_state = 'blocked'

    fop = fields.Many2one(comodel_name='nanny.fop', string='ФОП')
    is_active = fields.Boolean(string="Участвеут в рассчетах", default=True)
    client_data = fields.One2many(comodel_name='nanny.client_data', inverse_name='client', string="",)
    phone_num = fields.Char(string="Телефон")
    notes = fields.Text(string="Заметки", required=False)

    color = fields.Integer('Color Index')
    kanban_state = fields.Selection(
        [('normal', 'Не активен'), ('done', 'Активен'), ('blocked', 'Мало времени')],
        string='Kanban State', copy=False, default='done', required=True)


    @api.model
    def create(self, values):
        res = super(Сlient, self).create(values)
        self.env['nanny.client_data'].check_if_exist_calc_data(self, False)
        return res

    def write(self, values):
        res = super(Сlient, self).write(values)
        if 'add_date' in values:
            self.env['nanny.client_data'].check_if_exist_calc_data(self, False)
        return res

    def unlink(self):
        self.sudo().mapped('client_data').unlink()
        return super(Сlient, self).unlink()
