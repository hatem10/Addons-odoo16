from odoo import models,fields,api

class Product(models.Model):
    _name = "garden.product"
    _description = "Producto"
    _inherit = "mail.thread"

    name = fields.Char(string="Codigo",size=100,tracking=True)
    name_product = fields.Char(string="Nombre",size=100,tracking=True)
    gama_product_id = fields.Many2one(string="Gama",comodel_name="garden.gama.product",tracking=True)
    dimensiones = fields.Char(string="Dimensión",size=25,tracking=True)
    proveedor = fields.Char(string="Proveedor",size=50,tracking=True)
    description = fields.Text(string="Descripción",tracking=True)
    quanty_stock = fields.Integer(string="Cantidad")
    price_sale = fields.Float(string="Precio",digits=(15,2),tracking=True)
    price_proveedor = fields.Float(string="Precio Proveedor",digits=(15,2),tracking=True)

