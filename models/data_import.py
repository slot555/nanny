# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DataImport(models.TransientModel):
    _name = 'nanny.data_import'
    _description = 'Import'

    name = fields.Char(string="import")

    def make_data_impoort(self):
        from_data = self.env['test.mod'].search([])
        for client in from_data:
            if not self.env['nanny.client'].search([('name', '=', client.name)]):
                if client.parent_id:
                    parent_id = self.env['nanny.client'].search([('name', '=', client.parent_id.name)])
                else:
                    parent_id = False
                client_values = {
                    'name': client.name,
                    'add_date': client.add_date,
                    'parent_id': parent_id,
                    'fop': client.fop  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                }
                new_client = self.env['nanny.client_data'].create(client_values)
                for baby in client.babies:
                    baby_values = {
                        'name': baby.name,
                        'birthday': baby.birthday,
                        'mother': client,
                    }
                    new_baby = self.env['nanny.baby'].create(baby_values)


