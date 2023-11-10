from odoo import models,fields,api
from logging import getLogger

logger = getLogger(__name__)
class Procedure(models.Model):
    _name = "procedure"
    _description = "Registro de Tramites"

    name = fields.Char(string="Nombre Tramite")

    @api.model
    def create(self,values):
        return super(Procedure,self).create(values)
    def write(self,values):
        return super(Procedure,self).write(values)
    def unlink(self):
        return super(Procedure,self).unlink()
