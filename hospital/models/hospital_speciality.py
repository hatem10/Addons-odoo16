from odoo import fields,models,api

class HospitalSpeciality(models.Model):
    _name = "hospital.speciality"
    _description = "Especialidades"
    _inherit = "mail.thread"

    name = fields.Char(string="Especialidad",tracking=True)
    code = fields.Char(string="Codigo",tracking=True)
    active = fields.Boolean(string="Active",default=True)