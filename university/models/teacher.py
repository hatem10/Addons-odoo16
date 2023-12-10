from odoo import models,fields,api
from ..services.utils import TYPE_SEXO
class Teacher(models.Model):
    _name = "university.teacher"
    _description = "Lista de Maestros"
    _inherit = "mail.thread"

    name = fields.Char(string="NIF",size=9,tracking=True)
    full_name = fields.Char(string="Nombres",size=100,tracking=True)
    father_last_name = fields.Char(string="Apellido Paterno",size=100,tracking=True)
    mother_last_name = fields.Char(string="Apellido Materno", size=100,tracking=True)
    city = fields.Many2one(string="Ciudad",comodel_name="res.country.state",tracking=True)
    address = fields.Char(string="Direccion",size=100,tracking=True)
    phone_mobile = fields.Char(string="Celular",size=9,tracking=True)
    birth_date = fields.Date(string="Fecha Nacimiento",tracking=True)
    sexo = fields.Selection(string="Sexo",selection=TYPE_SEXO,default="M",tracking=True)
    id_department = fields.Many2one(string="Departamento",comodel_name="university.department",tracking=True)

    def name_get(self):
        user = []
        for rec in self:
            name = "[%s]%s %s %s" %(rec.name,rec.full_name,rec.father_last_name,rec.mother_last_name)
            user.append((rec.id,name))
        return user
