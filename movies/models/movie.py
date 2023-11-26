from odoo import models,fields,api
from ..services.utils import OPTIONS_SEDE,TYPE_STATE,OPTIONS_CLASIFICATION
from datetime import date
class Movie(models.Model):
    _name = "movie"
    _description = "Registro de Peliculas"
    _inherit = "mail.thread"

    name = fields.Char(string="Pelicula",required=True,tracking=True)
    description = fields.Text(string="Descripción",required=True,tracking=True)
    duration = fields.Char(string="Duracion",tracking=True)
    date = fields.Date(string="Fecha Estreno",tracking=True)
    clasification = fields.Selection(string="Clasificacion",selection=OPTIONS_CLASIFICATION,tracking=True)
    sede = fields.Selection(string="Sede",selection=OPTIONS_SEDE,tracking=True)
    state = fields.Selection(string="Estado",selection=TYPE_STATE,tracking=True)
    image = fields.Binary(tracking=True)
    author_id = fields.Many2one(string="Author",comodel_name="movie.author",tracking=True)
    genero_id = fields.Many2many(string="Genero",comodel_name="movie.genero",relation="movie_movie_genero",colum1="movie_id",colum2="movie_genero_id")
    country_id = fields.Many2one(string="Pais",comodel_name="res.country")

    @api.model
    def create(self,values):
        return super(Movie,self).create(values)

    def write(self,values):
        return super(Movie,self).write(values)

    def unlink(self):
        return super(Movie,self).unlink()
