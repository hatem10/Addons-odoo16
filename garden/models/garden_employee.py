from odoo import models,fields,api

class Employee(models.Model):
    _inherit = "hr.employee"

    id_office = fields.Many2one(string="Oficina",comodel_name="garden.office")