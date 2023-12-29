from odoo import fields,models,api
from datetime import date
class Speciality(models.Model):
    _name = "veterinary.speciality"
    _description = "Información sobre la especialidad de veterinarios"
    _inherit = "mail.thread"

    name = fields.Char(string="Especialidad",tracking=True)
    code = fields.Char(string="Codigo",tracking=True)

    def default_get(self,fields):
        res = super(Speciality,self).default_get(fields)
        return res
    @api.model
    def create(self,values):
        return super(Speciality,self).create(values)

    def write(self,values):
        return super(Speciality,self).write(values)

    def unlink(self):
        return super(Speciality,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(Speciality,self).copy(default)