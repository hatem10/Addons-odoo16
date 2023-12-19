from odoo import fields,models,api
from datetime import date
class HistoryClinic(models.Model):
    _name = "hospital.history.clinic"
    _description = "Historia Clinica"
    _inherit = "mail.thread"

    name = fields.Char(string="Historia Clinica",tracking=True)
    date = fields.Date(string="Fecha",tracking=True)
    patient_id = fields.Many2one(string="Paciente",comodel_name="hospital.patient",tracking=True)
    active = fields.Boolean(string="Active",tracking=True)

    @api.model
    def create(self,values):
        values["name"] = self.env["ir.sequence"].next_by_code("code.historty.clinic")
        return super(HistoryClinic,self).create(values)

    def write(self,values):
        return super(HistoryClinic,self).write(values)

    def unlink(self):
        return super(HistoryClinic,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(HistoryClinic,self).copy(default)

    def default_get(self,fields):
        res = super(HistoryClinic,self).default_get(fields)
        res["date"] = date.today()
        res["active"] = True
        return res
