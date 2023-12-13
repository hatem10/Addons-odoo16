from odoo import models,fields,api
class Customer(models.Model):
    _name = "garden.office"
    _description = "Oficina"
    _inherit = "mail.thread"

    name = fields.Char(string="Codigo",tracking=True)
    id_city = fields.Many2one(string="Ciudad", comodel_name="res.country.state", tracking=True)
    id_country = fields.Many2one(string="Pais", comodel_name="res.country", tracking=True)
    code_postal = fields.Char(string="Codigo Postal", size=10, tracking=True)
    phone = fields.Char(string="Telefono", size=15, tracking=True)
    address_1 = fields.Char(string="Dirección 1",tracking=True)
    address_2 = fields.Char(string="Dirección 2",tracking=True)



