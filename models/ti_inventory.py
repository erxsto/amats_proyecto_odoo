import string
from odoo import models, fields

class Dispositivo(models.Model):
    _name = 'module_test.device'
    _description = 'dispositivos electronicos'

    tipo = fields.Selection([('c', 'computadora'), ('t', 'telefono')], default='c')
    marca = fields.Many2one('module_test.app', string = 'marca')
    

class Aplicacion(models.Model):
    _name = 'module_test.app'
    _description = 'software'

    name = fields.Char(string = 'nombre')
    descripcion = fields.Char(string = 'descripcion')
    version = fields.Char(string = 'version')