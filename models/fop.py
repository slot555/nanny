# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FOP(models.Model):
    _name = 'nanny.fop'
    _description = 'FOP'

    name = fields.Char(string="ФОП")