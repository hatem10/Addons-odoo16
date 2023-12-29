from odoo import fields,models,api
from datetime import date
class Veterinary(models.Model):
    _name = "veterinary"
    _description = "Información general de los Veterinarios"
    _inherit = "mail.thread"

    name = fields.Char(string="Veterinario",size=30,tracking=True)
    code = fields.Char(string="Codigo",tracking=True)
    last_name = fields.Char(string="Apellido",size=30,tracking=True)
    address = fields.Char(string="Dirección",size=80,tracking=True)
    phone = fields.Char(string="Telefono",size=30,tracking=True)
    dui = fields.Char(string="DUI",size=12,tracking=True)
    nit = fields.Char(string="NIT",size=17,tracking=True)
    sexo_id = fields.Many2one(string="Sexo",comodel_name="veterinary.sexo")
    speciality_id = fields.Many2one(string="Especialidad",comodel_name="veterinary.speciality",tracking=True)

    def default_get(self,fields):
        res = super(Veterinary,self).default_get(fields)
        res["register_date"] = date.today()
        return res
    @api.model
    def create(self,values):
        return super(Veterinary,self).create(values)

    def write(self,values):
        return super(Veterinary,self).write(values)

    def unlink(self):
        return super(Veterinary,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(Veterinary,self).copy(default)