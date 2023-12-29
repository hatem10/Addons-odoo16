from odoo import fields,models,api
from datetime import date
class ClaseMascota(models.Model):
    _name = "veterinary.clase.mascota"
    _description = "Información sobre clase Mascota"
    _inherit = "mail.thread"

    name = fields.Char(string="Clase Mascota",tracking=True)

    def default_get(self,fields):
        res = super(ClaseMascota,self).default_get(fields)
        return res
    @api.model
    def create(self,values):
        return super(ClaseMascota,self).create(values)

    def write(self,values):
        return super(ClaseMascota,self).write(values)

    def unlink(self):
        return super(ClaseMascota,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(ClaseMascota,self).copy(default)