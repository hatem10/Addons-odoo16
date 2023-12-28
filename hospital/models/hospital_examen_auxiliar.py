from odoo import models,fields,api
from datetime import date
from ..services.utils import TYPE_EXAMEN,TYPE_SEGURO,TYPE_ACIVITES
class ExamenAuxiliar(models.Model):
    _name = "hospital.examen.auxiliar"
    _description = "Solicitud Examen Auxiliar"
    _inherit = "mail.thread"

    name = fields.Char(string="Nro.de Solicitud",tracking=True)
    type_examen = fields.Selection(string="Tipo Examen",selection=TYPE_EXAMEN)
    type_seguro = fields.Selection(string="Tipo de Seguro",selection=TYPE_SEGURO)
    plan_salud = fields.Char(string="Plan de Salud",tracking=True)
    date = fields.Date(string="Fecha",default=lambda self:date.today(),tracking=True)
    patient_id = fields.Many2one(string="Paciente",comodel_name="hospital.patient",tracking=True)
    document = fields.Char(string="Documento Identidad",related="patient_id.number_document",tracking=True)
    age = fields.Integer(string="Edad",related="patient_id.age",tracking=True)
    sexo = fields.Selection(string="Sexo",related="patient_id.sexo",tracking=True)
    #Datos del Paciente
    department = fields.Char(string="Departamento",tracking=True)
    province = fields.Char(string="Provincia",tracking=True)
    district = fields.Char(string="Distrito",tracking=True)
    address = fields.Char(string="Dirección")
    reference = fields.Char(string="Referencia",tracking=True)
    mobile = fields.Char(string="Celular",tracking=True)
    phone = fields.Char(string="Telefono Fijo",tracking=True)
    email = fields.Char(string="Email",tracking=True)
    #Datos Doctor
    doctor_id = fields.Many2one(string="Medico",comodel_name="hospital.doctor",tracking=True)
    acto_medico = fields.Char(string="Acto Medico",tracking=True)
    date_atention = fields.Date(string="Fecha Atención",tracking=True)
    speciality_id = fields.Many2one(string="Especialidad",comodel_name="hospital.speciality",tracking=True)
    activity_specific = fields.Selection(string="Actividad Especifica",selection=TYPE_ACIVITES,tracking=True)
    history_clinic_id = fields.Many2one(string="Nro.Historia Clinica",comodel_name="hospital.history.clinic",tracking=True)
    type_examen_ids = fields.Many2many(string="Tipo Examen",comodel_name="hospital.type.examen",tracking=True)
    observation = fields.Html(string="Observaciones",tracking=True)
    @api.model
    def create(self,values):
        return super(ExamenAuxiliar,self).create(values)

    def write(self,values):
        return super(ExamenAuxiliar,self).write(values)

    def unlink(self):
        return super(ExamenAuxiliar,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(ExamenAuxiliar,self).copy(default)

    def default_get(self,fields):
        res = super(ExamenAuxiliar,self).default_get(fields)
        res["date"] = date.today()
        res["date_atention"] = date.today()
        return res

    @api.onchange("patient_id")
    def _onchange_history_clinic_id(self):
        if self.patient_id:
            history_clinic = self.env["hospital.history.clinic"].search([("patient_id","in",[self.patient_id.id])])
            self.history_clinic_id = history_clinic
        else:
            self.history_clinic_id = False


