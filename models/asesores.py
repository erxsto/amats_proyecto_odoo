from odoo import models, fields, api


class Asesorcomponents(models.Model):
    _name = 'module_test.asesor'
    _description = 'Componentes de Asesor'

    asesor = fields.Many2one('hr.employee', 'Asesor', attribute='id')
    currency_id = fields.Many2one('res.currency', 'Moneda', required=True, writeonly=False)
    puesto = fields.Char(related='asesor.job_title', string='Puesto', store=True)


class Rules_total_asesor_ventas(models.Model):
    _name = 'module_test.rules_total_asesor'

    rule_total_id = fields.Integer()
    year = fields.Integer(string='Año')
    currency_id = fields.Many2one('res.currency', string='Moneda')
    meta_anual = fields.Monetary(string='🎯Meta Anual', computed='_get_meta_anual', store=True)
    meta_mes = fields.One2many('module_test.rules_mes_asesor', 'rule_mes_id', string='🎯 Meta de meses', store=True)

    @api.depends('meta_mes')
    def _get_meta_anual(self):
        for record in self:
            record.meta_anual = sum(line.meta for line in record.meta_mes)


class Rules_mes_asesor_ventas(models.Model):
    _name = 'module_test.rules_mes_asesor'

    sequence = fields.Integer()

    rule_mes_id = fields.Integer()
    rule_anual_id = fields.Many2one(inverse_name='meta_mes', store=True)
    fecha_inicio = fields.Date(string='Fecha Inicio')
    fecha_fin = fields.Date(string='Fecha Fin')
    currency_id = fields.Many2one('res.currency', string='Moneda')
    nombre_mes = fields.Char(string='Nombre del Mes')
    meta = fields.Monetary(string='Meta')


class Asesor_ventas(models.Model):
    _name = 'amats.asesor'

    currency_id = fields.Many2one(comodel='res.currency', string='Moneda')

    asesor_venta_id = fields.Integer()
    empleado = fields.Many2one(comodel='hr.employee', string='Empleado')
    puesto = fields.Many2one(comodel='hr.job', string='Puesto')

    rules_total_asesor = fields.Many2one(comodel='amats.rules_total_asesor')
    meta_anual = fields.Monetary(related='rules_total_asesor.meta_anual', readonly='True')

    acumulado = fields.Monetary(string='Acumulado', computed='_get_total_anual')
    cumplimiento_total = fields.Float(string='Cumplimiento', computed='_get_cumplimiento')

    lineas_mes_asesor = fields.One2many('amats.lineas_mes_asesor', 'linea_id', string='Linea Mes')

    @api.depends('lineas_mes_asesor.cumplimiento')
    def _get_cumplimiento_total(self):
        for record in self:
            record.cumplimiento_total = sum(line.cumplimiento for line in record.lineas_mes_asesor)

    @api.depends('lineas_mes_asesor.cumplimiento')
    def _get_total_anual(self):
        for record in self:
            record.total_anual = sum(line.total for line in record.lineas_mes_asesor)

    @api.depends('total_anual', 'meta_anual')
    def _get_cumplimiento(self):
        for record in self:
            if record.total_anual > 0 and record.meta_anual > 0:
                cumplimiento_total = (record.total_anual * 100 / record.meta_anual)
            else:
                cumplimiento_total = 0
            return cumplimiento_total


class Lineas_Mes_Asesor(models.Model):
    _name = 'amats.lineas_mes_asesor'
    _description = 'Desgloce de ventas'

    asesor_venta_id = fields.Many2one(comodel='amats.asesor')
    linea_id = fields.Integer()
    sequence = fields.Integer()

    rules_mes_asesor = fields.Many2one(comodel='amats.rules_mes_asesor')
    meta_mes = fields.Monetary(related='rules_mes_asesor')
    fecha_inicio = fields.Date(related='rules_mes_asesor.fecha_inicio', string='Fecha Inicio')
    fecha_fin = fields.Date(related='rules_mes_asesor.fecha_fin', string='Fecha Fin')

    total_mes = fields.Monetary(string='📈Total', computed='_get_total_mes')
    total_pagado_mes = fields.Monetary(string='💵Total pagado', computed='_get_total_pagado_mes')
    deficit_mes = fields.Monetary(string='☹Deficit', computed='_get_deficit_mes')

    # Cumplimiento
    cumplimiento = fields.Float(string='Cumplimiento', computed='_get_cumplimiento')
    porcentaje_pagado = fields.Float(string='% Pagado', computed='_get_porcentaje_pagado')

    # Facturas
    facturas_mes = fields.One2many('account.move', 'id_user',
                                   domain='[["type","=","out_invoice"],["invoice_date",">=",fecha_inicio],'
                                          '["invoice_date","<=",fecha_fin],["state","=","posted"]]')
    facturas_generadas = fields.Integer(string='Facturas generadas', computed='_get_facturas_generadas')
    facturas_pagadas = fields.Integer(string='Facturas pagadas', computed='_get_facturas_pagadas')
    porcentaje_generadas_pagadas = fields.Float(string='Porcentaje', computed='_get_porcentaje_generadas_pagadas')

    n_credito_mes = fields.One2many('account.move', 'id_user',
                                    domain='[["type","=","out_refund"],["invoice_date",">=", fecha_inicio],'
                                           '["invoice_date","<=", fecha_fin],["state","=","posted"]]')
    studio_desc_ncc_mes = fields.Float(string='Desc. NCC', computed='_get_desc_ncc')

    # Comisiones
    comision_pronto_pago = fields.Monetary(string='Comision Pronto Pago', computed='_get_comision_pronto_pago')
    comision_venta = fields.Monetary(string='Comision por Venta', computed='_get_comision_venta')
    comision_cobrar = fields.Monetary(string='Comision a Cobrar', computed='_get_comision_cobrar')

    x_pedidos_usd_mes = fields.One2many('sale.order', 'id_user', string='Pedidos USD', domain='[["date_order", ">=", '
                                                                                              'fecha_inicio] ,'
                                                                                              '["date_order", "<=", '
                                                                                              'fecha_fin], '
                                                                                              '["state", "not in", '
                                                                                              '("draft", "sent", '
                                                                                              '"cancel")], '
                                                                                              '["currency_id.id", '
                                                                                              '"=", "2"]]')
    x_pedidos_mxn_mes = fields.One2many('sale.order', 'id_user', string='Pedidos MXN', domain='[["date_order",">=",'
                                                                                              'fecha_inicio],'
                                                                                              '["date_order","<=",'
                                                                                              'fecha_fin], '
                                                                                              '["state", "not in", '
                                                                                              '("draft", "sent", '
                                                                                              '"cancel")], '
                                                                                              '["currency_id.id", '
                                                                                              '"=", "33"]]')

    # Cumpimiento
    @api.depends('meta_mes', 'total_pagado_mes')
    def _get_cumplimiento(self):
        for record in self:
            if record.total_mes > 0 and record.meta_mes > 0:
                record['cumplimiento_mes'] = (record.total_mes * 100 / record.meta_mes)
            else:
                record['cumplimiento_mes'] = 0

    @api.depends('total_pagado_mes')
    def _get_porcentaje_pagado(self):
        for record in self:
            total = 0.0
            porc = 0.0
            for line in record.facturas_mes:
                total += line.amount_total_signed
                if total > 0 and record.total_pagado_mes > 0:
                    porc = (record.total_pagado_mes * 100 / record.meta_mes)
                else:
                    porc = 0
            record['porcentaje_pagado'] = porc

    # Facturas
    @api.depends('n_credito_mes')
    def _get_desc_ncc(self):
        for record in self:
            total = 0.0
            for line in record.n_credito_mes:
                fecha = line.invoice_date
                rate_usd = self.env['res.currency'].search([('name', '=', 'MXN')], limit=1).with_context(
                    date=fecha).rate
                total += line.amount_untaxed_signed * rate_usd
            record['studio_desc_ncc_mes'] = total

    @api.depends('fecha_inicio', 'fecha_fin')
    def _get_facturas_generadas(self):
        results = self.env['account.move'].read_group(
            [('id_user', 'in', self.ids), ('type', '=', 'out_invoice'), "&", ("invoice_date", ">=", self.fecha_inicio),
             ("invoice_date", "<=", self.fecha_fin), ("state", "=", "posted")],
            ['id_user'], ['id_user'])
        dic = {}
        for x in results:
            dic[x['id_user'][0]] = x['id_usr_count']
        for record in self:
            record['fact_pag'] = dic.get(record.id, 0)

    @api.depends('facturas_mes')
    def _get_facturas_pagadas(self):
        for record in self:
            total = 0.0
            adeudo = 0.0
            for line in record.facturas_mes:
                total += line.amount_total_signed
                adeudo += line.amount_residual_signed
            record['facturas_pagadas'] = total - adeudo

    @api.depends('facturas_pagadas', 'facturas_generadas')
    def _get_porcentaje_generadas_pagadas(self):
        for record in self:
            if record.facturas_pagadas > 0:
                record['porcentaje_generadas_pagadas'] = (record.facturas_pagadas * 100 / record.facturas_mes)
            else:
                record['porcentaje_generadas_pagadas'] = 0

    # Comisiones
    @api.depends('facturas_mes')
    def _get_comision_pronto_pago(self):
        for record in self:
            total = 0.0
            for line in record.facturas_ene:
                total += line.comision1
            record['comision_pronto_pago'] = total

    @api.depends('facturas_mes')
    def _get_comision_venta(self):
        for record in self:
            total = 0.0
            for line in record.facturas_mes:
                total += line.comision_2
            record['comision_venta'] = total

    @api.depends('comision_venta', 'comision_pronto_pago')
    def _get_comision_cobrar(self):
        for record in self:
            record['comision_cobrar'] = record.comision_venta + record.comision_pronto_pago

    @api.depends('facturas_mes')
    def _get_total_mes(self):
        for record in self:
            total = 0.0
            for line in record.facturas_mes:
                total += line.amount_untaxed_signed
            record['total_mes'] = total

    @api.depends('facturas_mes')
    def _get_total_pagado_mes(self):
        for record in self:
            total = 0.0
            adeudo = 0.0
            for line in record.facturas_mes:
                total += line.amount_total_signed
                adeudo += line.amount_residual_signed
            record['total_pagado_mes'] = total - adeudo

    @api.depends('meta_mes', 'total_mes')
    def _get_deficit_mes(self):
        for record in self:
            if record.total_mes > 0 and record.meta_mes > 0:
                record['deficit_mes'] = (record.meta_mes - record.total_mes)
            else:
                record['deficit_mes'] = 0