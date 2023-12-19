from odoo import fields,models,api

class TypeExamen(models.Model):
    _name = "hospital.type.examen"
    _description = "Tipo de Examen"
    _inherit = "mail.thread"

    name = fields.Char(string="Nombre",tracking=True)
    code = fields.Char(string="Codigo",tracking=True)
    indication = fields.Text(string="Indicaciones",tracking=True)
    #examen_auxiliar_id = fields.Many2one(comodel_name="hospital.examen.auxiliar")
    @api.model
    def create(self,values):
        return super(TypeExamen,self).create(values)

    def write(self,values):
        return super(TypeExamen,self).write(values)

    def unlink(self):
        return super(TypeExamen,self).unlink()

    def copy(self,default=None):
        default = dict(default or {})
        return super(TypeExamen,self).copy(default)