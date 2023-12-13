from odoo import models,fields,api

class GamaProducto(models.Model):
    _name = "garden.gama.product"
    _description = "Lista de Productos"
    _inherit = "mail.thread"

    name = fields.Char(string="Gama",size=100,tracking=True)
    description_text = fields.Text(string="Descripción Corta",size=100,tracking=True)
    description_html = fields.Html(string="Descripcion Larga",size=100,tracking=True)
    image = fields.Binary(string="Imagen")

