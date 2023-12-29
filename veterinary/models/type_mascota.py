from odoo import fields,models,api
from datetime import date
class TypeMascotas(models.Model):
    _name = "veterinary.type.mascota"
    _description = "Información sobre tipos de Mascota"
    _inherit = "mail.thread"

    name = fields.Char(string="Tipo Mascota",tracking=True)

    def default_get(self,fields):
        res = super(TypeMascotas,self).default_get(fields)
        res["register_date"] = date.today()
        return res
    @api.model
    def create(self,values):
        return super(TypeMascotas,self).create(values)

    def write(self,values):
        return super(TypeMascotas,self).write(values)

    def unlink(self):
        return super(TypeMascotas,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(TypeMascotas,self).copy(default)