from odoo import models,fields,api

class OrderAddressCustomer(models.Model):
    _name = "order.customer.address"
    _inherit = "mail.thread"
    _description = "Direccion Cliente"

    name = fields.Char(string="Lugar",required=True,tracking=True)
    address = fields.Char(string="Dirección",required=True,tracking=True)
    customer_id = fields.Many2one(string="Cliente",comodel_name="order.customer",tracking=True)

    @api.model
    def create(self,values):
        return super(OrderAddressCustomer,self).create(values)

    def write(self,values):
        return super(OrderAddressCustomer,self).write(values)

    def unlink(self,values):
        return super(OrderAddressCustomer,self).unlink()
