from odoo import models,fields,api
from logging import getLogger

logger = getLogger(__name__)

class Area(models.Model):
    _name = "area"
    _description = "Tipos de Tramite"

    name = fields.Char(string="Tramite",required=True)
    code = fields.Char(string="Codigo")

    @api.model
    def create(self,values):
        return super(Area,self).create(values)
    def write(self,values):
        return super(Area,self).write(values)
    def unlink(self):
        return super(Area,self).unlink()
