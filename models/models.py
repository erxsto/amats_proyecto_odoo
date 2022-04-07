from odoo import models, fields, api


class Asesorcomponents(models.Model):
    _name = 'module_test.asesor'
    _description = 'Componentes de Asesor'

    asesor = fields.Many2one('hr.employee', 'Asesor', attribute='id')
    currency_id = fields.Many2one('res.currency', 'Moneda', required=True, writeonly=False)
    puesto = fields.Char(related='asesor.job_title', string='Puesto', store=True)


class Rules_total_asesor_ventas(models.Model):
    _name = 'amats.rules_total_asesor'

    rule_total_id = fields.Integer()
    year = fields.Integer(string='Año')
    currency_id = fields.Many2one(comodel='res.currency', string='Moneda')
    meta_anual = fields.Monetary(string='🎯Meta Anual', computed='_get_meta_anual', store=True)
    meta_mes = fields.One2many('amats.rules_mes_asesor', 'rule_mes_id', string='🎯 Meta de meses')

    @api.depends('meta_mes')
    def _get_meta_anual(self):
        for record in self:
            record.meta_anual = sum(line.meta for line in record.meta_mes)


class Rules_mes_asesor_ventas(models.Model):
    _name = 'module_test.rules_mes_asesor'

    sequence = fields.Integer()

    rule_mes_id = fields.Integer()
    fecha_inicio = fields.Date(string='Fecha Inicio')
    fecha_fin = fields.Date(string='Fecha Fin')
    currency_id = fields.Many2one('res.currency', string='Moneda')
    nombre_mes = fields.Char(string='Nombre del Mes')
    meta = fields.Monetary(string='Meta')



