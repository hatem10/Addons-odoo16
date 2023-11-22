from odoo import models,fields,api

class Facultad(models.Model):
    _name = "facultad"
    _description = "Lista de Facultades"
    name = fields.Char(string="Facultad")
    code = fields.Char(string="Codigo")

    @api.model
    def create(self,values):
        return super(Facultad,self).create(values)
    def write(self,values):
        return super(Facultad,self).write(values)
    def unlink(self):
        return super(Facultad,self).unlink()