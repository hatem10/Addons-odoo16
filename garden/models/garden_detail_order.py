from odoo import models,fields,api

class DetailPedido(models.Model):
    _name = "garden.detail.order"
    _description = "Detalle Pedido"
    _inherit = "mail.thread"

    id_order = fields.Char(string="Pedido",comodel_name="garden.order",tracking=True)
    id_product = fields.Many2many(string="Productos",comodel_name="garden.product",
                                  relation="product_order",column1="id_detail_product",column2="id_product",tracking=True)
    quanty = fields.Integer(string="Cantidad",digits=(11,0))
    price_unit = fields.Float(string="Precio Unitario",digits=(15,2))
    #number_line = fields.


