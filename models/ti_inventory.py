import string
from odoo import models, fields

class Dispositivo(models.Model):
    _name = 'module_test.device'
    _description = 'dispositivos electronicos'

    tipo = fields.Selection([('computadora', 'c'), ('telefono', 't')], default='c')
    marca = fields.Char(string = 'marca')