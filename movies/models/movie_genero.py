from odoo import models,fields,api

class MovieGenero(models.Model):
    _name = "movie.genero"
    _description = "Lista de Generos"
    _inherit = "mail.thread"

    name = fields.Char(string="Genero",required=True,tracking=True)
