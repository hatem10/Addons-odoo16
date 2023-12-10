from odoo import models,fields,api
from datetime import date
from ..services.utils import OPTIONS_MATRICULA
class StudentMatricula(models.Model):
    _name = "university.student.matricula"
    _description = "Matricula de Estudiante"
    _inherit = "mail.thread"

    name = fields.Char(string="Codigo Matricula",readonly=True,tracking=True)
    id_asignatura = fields.Many2one(string="Asignatura",comodel_name="university.asignatura",tracking=True)
    id_student = fields.Many2one(string="Estudiante",comodel_name="university.student",tracking=True)
    id_year_school = fields.Many2one(string="Año Escolar",comodel_name="university.year.school",tracking=True)
    date_matricula = fields.Date(string="Matricula",required=True,tracking=True)
    state_matricula = fields.Selection(selection=OPTIONS_MATRICULA,tracking=True)

    @api.model
    def create(self,values):
        values["name"] = self.env["ir.sequence"].next_by_code("code.matricula")
        values["state_matricula"] = "draft"
        return super(StudentMatricula,self).create(values)

    def default_get(self,fields):
        res = super(StudentMatricula,self).default_get(fields)
        res["date_matricula"] = date.today()
        return res

    def btn_draft(self):
        self.state_matricula = "draft"

    def btn_approved(self):
        self.state_matricula = "approved"

    def btn_done(self):
        self.state_matricula = "done"
