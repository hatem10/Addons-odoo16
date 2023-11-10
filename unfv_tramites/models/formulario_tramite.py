from odoo import models,fields,api
from logging import getLogger

logger = getLogger(__name__)

class FormularioTramite(models.Model):
    _name = "formulario.tramite"
    _description = "Registro Solicitud de Tramite"

    TYPE_PROCEDURE = [
        ('AC-SG','(AC-SG) ARCHIVO CENTRAL'),
        ('BC-UNFV', '(BC-UNFV) BIBLIOTECA CENTRAL - UNFV')
    ]
    TYPE_DEPENDS = [
        ('')
    ]
    make_procedure = fields.Selection(string="Tramite a Realizar",selection=TYPE_PROCEDURE)
    directed = fields.Selection(string="Dirigido")
    type_solicitant = fields.Selection(string="Tipo Solicitante")
    type_document = fields.Selection(string="Tipo Documento")
    number_document = fields.Char(string="Numero Documento",requerid=True)
    father_last_name = fields.Char(string="Apellido Paterno")
    mother_last_name = fields.Char(string="Apellido Materno")
    name_solicitant = fields.Char(string="Nombres")
    facultad = fields.Selection(string="Facultad")
    school_solicitant = fields.Selection(string="Escuela Solicitante")
    code_solicitant = fields.Char(string="Codigo del Solicitante")
    departament = fields.Many2one(string = "Departamento",comodel_name="res.country.state")
    province = fields.Many2one()
    #district = fields.Many2one()
    address = fields.Char(string="Dirección")
    number_departament = fields.Char(string="N° y/o Departamento")
    phone = fields.Char(string="Telefono Fijo")
    cell_phone = fields.Char(string="Celular")
    email = fields.Char(string="Correo Electronico",required=True)
    fundament_solicitud = fields.Text(string="Fundamento de Solicitud",required=True)
    document_adjunt = fields.Char(string="Documento que se Adjuntan")
    document_digital'''
    '''number_folios = fields.Integer(string = "Numero de Folios")