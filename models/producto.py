import base64
import io
from odoo import models, fields


class ProductExtended(models.Model):
    _inherit = 'product.template'
    # Cosas a modificar
    currency_id = fields.Many2one('res.currency', string='Moneda X',require='true', writeonly='false')
    # Cosas que le falten al modelo
    product_type = fields.Many2one('product.product_type')
    product_category = fields.Many2one('product.product_category')
    brand = fields.Many2one('product.brand')
    sales_description = fields.Many2one('product.sales_description')


class ProductImportButton(models.TransientModel):
    _name = 'amats.products'

    upload_file = fields.Binary(string='Subir archivo', required=True)
    file_name = fields.Char(string='Nombre del fichero')

    def import_file(self):
        if self.file_name:
            if '.csv' not in self.file_name:
                raise exceptions.ValidationError('El archivo debe ser un .csv')
            file = self.read_file_from_binary(self.upload_file)
            lines = file.split('\n')
            for line in lines:
                elements = line.split(';')
                if len(elements) > 1:
                    self.env['product.template'].create({
                        'name': elements[1],
                        'product_type': elements[2],
                        'product_category': elements[3],
                        'default_code': elements[4],
                        'brand': elements[5],
                        'sales_price': float(elements[6]),
                        'cost': float(elements[7]),
                        'currency_id': float(elements[8]),
                        'sales_description': elements[9],
                        'buy_description': elements[10]
                    })

    def read_file_from_binary(self, file):
        try:
            with io.BytesIO(base64.b64decode(file)) as f:
                f.seek(0)
                return f.read().decode('UTF=8')
        except Exception as e:
            print(str(e))
            raise e


