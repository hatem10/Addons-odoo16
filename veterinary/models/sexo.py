from odoo import fields,models,api
from datetime import date
class Sexo(models.Model):
    _name = "veterinary.sexo"
    _description = "Información sobre el Genero"
    _inherit = "mail.thread"

    name = fields.Char(string="Sexo",tracking=True)

    def default_get(self,fields):
        res = super(Sexo,self).default_get(fields)
        return res
    @api.model
    def create(self,values):
        return super(Sexo,self).create(values)

    def write(self,values):
        return super(Sexo,self).write(values)

    def unlink(self):
        return super(Sexo,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(Sexo,self).copy(default)