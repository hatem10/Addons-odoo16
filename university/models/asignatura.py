from odoo import models,fields,api
from ..services.utils import TYPE_ASIGNATURA

class Grado(models.Model):
    _name = "university.grado"
    _description = "Grado"

    name = fields.Char(string="Grado",size=100)
class Asignatura(models.Model):
    _name = "university.asignatura"
    _description = "Asiganturas de Estudiantes"
    _inherit = "mail.thread"

    name = fields.Char(string="Codigo",size=20,tracking=True)
    creditos = fields.Integer(string="Creditos",tracking=True)
    curso = fields.Char(string="Asigantura",size=100,tracking=True)
    type_asignatura = fields.Selection(string="Tipo",selection=TYPE_ASIGNATURA,tracking=True)
    id_teacher = fields.Many2one(string="Docente",comodel_name="university.teacher",tracking=True)
    id_grado = fields.Many2one(string="Grado",comodel_name="university.grado",tracking=True)


    def default_get(self,fields):
        res = super(Asignatura,self).default_get(fields)
        res["creditos"] = 1
        return res

    def name_get(self):
        data = []
        for rec in self:
            name = "[%s]%s" %(rec.name,rec.curso)
            data.append((rec.id,name))
        return data

