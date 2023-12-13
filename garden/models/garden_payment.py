from odoo import models,fields,api

class Payment(models.Model):
    _name = "garden.payment"
    _description = "Pagos"
    _inherit = "mail.thread"

    name = fields.Char(string="Transacción",size=100,tracking=True)
    formant_payment = fields.Char(string="Forma Pago", size=100,tracking=True)
    date_payment = fields.Date(string="Fecha Pago")
    total = fields.Float(string="Total",digits=(15,2),tracking=True)
    id_customer = fields.Many2one(string="Cliente",comodel_name="garden.customer",tracking=True)
