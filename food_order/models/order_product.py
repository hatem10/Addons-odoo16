from odoo import models,fields,api

class OrderProduct(models.Model):
    _name = "order.product"
    _inherit = "mail.thread"
    _description = "Producto"

    name = fields.Char(string="Nombre Producto",tracking=True)
    stock = fields.Integer(string="Stock",tracking=True)
    price = fields.Float(string="Precio",tracking=True)
    discount = fields.Float(string="Descuento %s",tracking=True)
    image = fields.Binary(string="Imagen")