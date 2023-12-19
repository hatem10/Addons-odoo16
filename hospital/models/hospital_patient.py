from odoo import models,fields,api
from datetime import date
from  ..services.utils import TYPE_DOCUMENT,TYPE_SEXO
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Lista de Pacientes de Hospital"
    _inherit = "mail.thread"

    name = fields.Char(string="Nombres",size=100,tracking=True)
    type_document = fields.Selection(string="Documento",selection=TYPE_DOCUMENT,required=True,tracking=True)
    number_document = fields.Char(string="Numero",sise=100,required=True,tracking=True)
    father_last_name = fields.Char(string="Apellido Paterno",size=200,required=True,tracking=True)
    mother_last_name = fields.Char(string="Apellido materno",size=200,required=True,tracking=True)
    full_name = fields.Char(string="Nombres",size=100,tracking=True)
    date_birth = fields.Date(string="Fecha Nacimiento",tracking=True)
    age = fields.Integer(string="Edad",required=True,tracking=True)
    sexo = fields.Selection(string="Sexo",selection=TYPE_SEXO,tracking=True)
    active = fields.Boolean(string="Activo")
    def default_get(self,fields):
        res = super(HospitalPatient,self).default_get(fields)
        res["type_document"] = "01"
        return res
    @api.onchange("father_last_name","mother_last_name","full_name")
    def _onchange_full_name(self):
        if self.full_name or self.father_last_name or self.mother_last_name:
            self.name = "%s %s %s" %(self.full_name,self.father_last_name,self.mother_last_name)
        else :
            self.full_name = ""

    @api.model
    def create(self,values):
        return super(HospitalPatient,self).create(values)

    def write(self,values):
        return super(HospitalPatient,self).write(values)

    def unlink(self):
        return super(HospitalPatient,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(HospitalPatient,self).copy(default)

