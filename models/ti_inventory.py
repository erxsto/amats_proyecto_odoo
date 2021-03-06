import string
from odoo import models, fields

class Dispositivo(models.Model):
    _name = 'module_test.device'
    _description = 'dispositivos electronicos'

    empleado = fields.Many2one('hr.employee', 'Asesor', attribute='id')
    tipo = fields.Selection([('c', 'computadora'), ('t', 'telefono')], default='c')
    marca = fields.Many2one('module_test.brand', string = 'marca')
    app = fields.Many2many('module_test.app',string = 'aplicacion')

class Aplicacion(models.Model):
    _name = 'module_test.app'
    _description = 'software'

    id_app = fields.Integer()
    sequence = fields.Integer()
    name = fields.Char(string = 'nombre')
    descripcion = fields.Char(string = 'descripcion')
    version = fields.Char(string = 'version')

    
class Marca(models.Model):
    _name = 'module_test.brand'
    _description = 'Marca de dispositivos'

    name = fields.Char(string = 'nombre')