from odoo import models,fields,api
class Customer(models.Model):
    _name = "garden.customer"
    _description = "Clientes"
    _inherit = "mail.thread"

    name = fields.Char(string="Codigo",tracking=True)
    full_name  = fields.Char(string="Nombres",tracking=True)
    last_name = fields.Char(string="Apellido",tracking=True)
    contact = fields.Char(string="Contacto",tracking=True)
    phone = fields.Char(string="Telefono",size=15,tracking=True)
    tax = fields.Many2one(string="Impuestos",comodel_name="account.tax",tracking=True)
    address_1 = fields.Char(string="Dirección 1",tracking=True)
    address_2 = fields.Char(string="Dirección 2",tracking=True)
    id_country = fields.Many2one(string="Pais",comodel_name="res.country",tracking=True)
    id_city = fields.Many2one(string="Ciudad",comodel_name="res.country.state",tracking=True)
    code_postal = fields.Char(string="Codigo Postal",size=10,tracking=True)
    id_employee = fields.Many2one(string="Empleado",comodel_name="hr.employee",tracking=True)
    limit_credit = fields.Float(string="Credito",digits=(15,2),tracking=True)

    def name_get(self):
        data = []
        for rec in self:
            name = "[%s]%s %s" %(rec.name,rec.full_name,rec.last_name)
            data.append((rec.id,name))
        return data