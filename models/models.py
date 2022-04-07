from odoo import models, fields, api


class Asesorcomponents(models.Model):
    _name = 'module_test.asesor'
    _description = 'Componentes de Asesor'

    asesor = fields.Many2one('hr.employee', 'Asesor', attribute='id')
    currency_id = fields.Many2one('res.currency', 'Moneda', required=True, readonly=False)
    puesto = fields.Many2one('hr.job', 'Puesto')




