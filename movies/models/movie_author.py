from odoo import models,fields,api

class MovieAuthor(models.Model):
    _name = "movie.author"
    _description = "Lista de Autores"
    _inherit = "mail.thread"

    name = fields.Char(string="Pelicula",required=True,tracking=True)
    last_name = fields.Char(string="Apellidos",required=True,tracking=True)


    @api.model
    def create(self,values):
        return super(MovieAuthor,self).create(values)

    def write(self,values):
        return super(MovieAuthor,self).write(values)

    def unlink(self):
        return super(MovieAuthor,self).unlink()
