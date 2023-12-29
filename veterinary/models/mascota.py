from odoo import fields,models,api
from datetime import date
class Mascotas(models.Model):
    _name = "veterinary.mascota"
    _description = "Información general de las mascotas"
    _inherit = "mail.thread"

    name = fields.Char(string="Mascota",size=40,tracking=True)
    code = fields.Char(string="Codigo",tracking=True)
    customer_id = fields.Many2one(string="Cliente",comodel_name="res.partner",tracking=True)
    type_mascota_id = fields.Many2one(string="Tipo Mascota",comodel_name="veterinary.type.mascota",tracking=True)
    sexo_id = fields.Many2one(string="Sexo",comodel_name="veterinary.sexo",tracking=True)
    color = fields.Char(string="Color",size=30)
    clase_mascota_id = fields.Many2one(string="Clase Mascota",comodel_name="veterinary.clase.mascota",tracking=True)
    birth_date = fields.Date(string="Fecha Nacimiento",tracking=True)
    observation = fields.Text(string="Observacion",tracking=True)
    tratamiento = fields.Text(string="Tratamiento",tracking=True)
    register_date = fields.Date(string="Fecha Registro",tracking=True)

    def default_get(self,fields):
        res = super(Mascotas,self).default_get(fields)
        res["register_date"] = date.today()
        return res
    @api.model
    def create(self,values):
        return super(Mascotas,self).create(values)

    def write(self,values):
        return super(Mascotas,self).write(values)

    def unlink(self):
        return super(Mascotas,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(Mascotas,self).copy(default)