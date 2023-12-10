from odoo import models,fields,api
class Department(models.Model):
    _name = "university.department"
    _description = "Departamentos"
    _inherit = "mail.thread"

    name = fields.Char(string="Departamento",size=100)