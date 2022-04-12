from odoo import models, fields


class ProductExtended(models.Model):
    _inherit = 'product.template'
    # Cosas a modificar
    currency_id = fields.Many2one('res.currency', string='Moneda X', required=True, writeonly=True, readonly=False)
# Cosas que le falten al modelo
