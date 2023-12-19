from odoo import models,fields,api
from ..services.utils import TYPE_DOCUMENT
class Doctor(models.Model):
    _name = "hospital.doctor"
    _description = "Doctores"
    _inherit = "mail.thread"

    name = fields.Char(string="Doctor",tracking=True)
    last_name = fields.Char(string="Apellidos",tracking=True)
    address = fields.Char(string="Dirección",size=100,tracking=True)
    type_doc = fields.Selection(string="Tipo Documento",selection=TYPE_DOCUMENT)
    document = fields.Char(string="Documento",size=8,tracking=True)
    codigo = fields.Char(string="Colegiaura",size=6,tracking=True)
    active = fields.Boolean(string="Active",default=True)

    @api.model
    def create(self,values):
        return super(Doctor,self).create(values)

    def write(self,values):
        return super(Doctor,self).write(values)

    def unlink(self):
        return super(Doctor,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(Doctor,self).copy(default)
