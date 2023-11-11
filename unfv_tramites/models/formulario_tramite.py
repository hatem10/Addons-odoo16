from odoo import models,fields,api
from logging import getLogger

logger = getLogger(__name__)

class FormularioTramite(models.Model):
    _name = "formulario.procedure"
    _description = "Registro Solicitud de Tramite"

    TYPE_SOLICITANT = [
        ("estudiante","ESTUDIANTE"),
        ("docente","DOCENTE"),
        ("administrativo","ADMINISTRATIVO"),
        ("empresa_entidad","EMPRESA O ENTIDAD PUBLICA"),
        ("personal_juridica","PERSONAL JURIDICA")
    ]
    TYPE_DOCUMENT = [
        ('dni','DNI'),
        ('pasaporte', 'PASAPORTE'),
        ('carne', 'CARNET DE EXTRANJERIA'),
        ('ruc','RUC')
    ]
    TYPE_STATE = [
        ("draft","Borrador"),
        ("approved","Aprobado"),
        ("done","Realizado")
    ]

    name = fields.Many2one(string="Tramite a Realizar",comodel_name="procedure")
    code_procedure = fields.Char(string="Codigo")
    state = fields.Selection(selection=TYPE_STATE)
    directed = fields.Many2one(string="Dirigido",comodel_name="area")
    type_solicitant = fields.Selection(string="Tipo Solicitante",selection=TYPE_SOLICITANT)
    type_document = fields.Selection(string="Tipo Documento",selection=TYPE_DOCUMENT)
    number_document = fields.Char(string="Numero Documento",requerid=True)
    father_last_name = fields.Char(string="Apellido Paterno")
    mother_last_name = fields.Char(string="Apellido Materno")
    name_solicitant = fields.Char(string="Nombres")
    facultad = fields.Many2one(string="Facultad",comodel_name="facultad")
    school_solicitant = fields.Char(string="Escuela Solicitante")
    code_solicitant = fields.Char(string="Codigo del Solicitante")
    country_id = fields.Many2one(string="Pais",comodel_name="res.country")
    departament = fields.Many2one(string = "Departamento",comodel_name="res.country.state",domain="[('country_id','=',country_id)]")
    #province = fields.Many2one(string="Provincia")
    #district = fields.Many2one()
    address = fields.Char(string="Dirección")
    number_departament = fields.Char(string="N° y/o Departamento")
    phone = fields.Char(string="Telefono Fijo")
    cell_phone = fields.Char(string="Celular")
    email = fields.Char(string="Correo Electronico",required=True)
    fundament_solicitud = fields.Text(string="Fundamento de Solicitud",required=True)
    document_adjunt = fields.Char(string="Documento que se Adjuntan")
    document_digital = fields.Binary(string="Documentos Adjuntos Digital")
    number_folios = fields.Integer(string="Numero de Folios")

    @api.model
    def create(self,values):
        values["state"] = "draft"
        values["code_procedure"] = self.env["ir.sequence"].next_by_code("code.procedure")
        return super(FormularioTramite,self).create(values)
    def write(self,values):
        return super(FormularioTramite,self).write(values)

    def unlink(self):
        return super(FormularioTramite,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(FormularioTramite,self).copy(default)

    @api.model
    def default_get(self,fields):
        res = super(FormularioTramite,self).default_get(fields)
        return res

    def btn_draft(self):
        self.state = "draft"

    def btn_approved(self):
        self.state = "approved"

    def btn_done(self):
        self.state = "done"

    def name_get(self):
        result = []
        for rec in self:
            name = "[%s]%s" %(self.code_procedure,self.name.name)
            result.append((rec.id,name))
        return result