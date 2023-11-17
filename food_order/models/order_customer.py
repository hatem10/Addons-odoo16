from odoo import models,fields,api
from ..services.utils import TYPE_DOCUMENT,DNI
class OrderCustomer(models.Model):
    _name = "order.customer"
    _inherit = "mail.thread"
    _description = "Clientes"

    name = fields.Char(string="Nombre",size=100,required=True,tracking=True)
    document = fields.Selection(string="Tipo Documento",selection=TYPE_DOCUMENT,default=DNI,required=True,trackicng=True)
    number_document = fields.Char(string="Documento",sise=10,required=True,tracking=True)
    cell_phone = fields.Char(string="Celular",size=9,required=True,tracking=True)
    address_ids = fields.One2many(string="Direcciones",comodel_name="order.customer.address",inverse_name="customer_id",tracking=True)

    def btn_whatsapp(self):
        return {
            "type":"ir.actions.act_window",
            "name":"WhatsApp",
            "res_model":"customer.whatsapp.wizard",
            "view_mode":"form",
            "target":"new",
            "context":{
                "default_customer_id":self.id
            }
        }
    @api.model
    def create(self,values):
        return super(OrderCustomer,self).create(values)

    def write(self,values):
        return super(OrderCustomer,self).write(values)

    def unlink(self,values):
        return super(OrderCustomer,self).unlink()
