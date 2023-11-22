from odoo import models,fields,api
from ..services.utils import TYPE_STATE
class Order(models.Model):
    _name = "order"
    _inherit = "mail.thread"
    _description = "Pedidos por el Cliente"

    name = fields.Char(string="Numero/Pedido")
    date = fields.Date(string="Fecha del pedido",tracking=True)
    customer_id = fields.Many2one(string="Customer",comodel_name="order.customer",tracking=True)
    address_id = fields.Many2one(string="Direccion",comodel_name="order.customer.address",domain="[('customer_id','=',customer_id)]",tracking=True)
    state = fields.Selection(selection=TYPE_STATE,tracking=True)
    order_line_ids = fields.One2many(string="Productos",comodel_name="order.line",inverse_name="order_id",tracking=True)

    @api.model
    def create(self,values):
        values["name"] = self.env["ir.sequence"].next_by_code("order.code")
        return super(Order,self).create(values)

    def name_get(self):
        name = []
        for rec in self:
            data = "[%s]%s" %(rec.name,rec.customer_id.name)
            name.append((rec.id,data))
        return name

    def btn_draft(self):
        self.write({
            "state":"draft"
        })
    def btn_register(self):
        self.write({
            "state":"register"
        })

    def btn_preparation(self):
        self.write({
            "state":"preparation"
        })

    def btn_done(self):
        self.write({
            "state":"done"
        })

    #@api.onchange("customer_id")
    #def _onchange_customer_id(self):
        #self.address_id = False
        #if len(self.customer_id.address_ids) == 1:
            #self.address_id = self.customer_id.address_ids

class OrderLine(models.Model):
    _name = "order.line"
    _description = "Detalle de Pedido"

    product_id = fields.Many2one(string="Producto",comodel_name="order.product")
    quanty = fields.Integer(string="Cantidad",required=True)
    unit_price = fields.Float(string="Precio Unitario",required=True)
    subtotal = fields.Float(string="Subtotal")
    order_id = fields.Many2one(comodel_name="order")

    @api.onchange("quanty","unit_price")
    def _onchange_subtotal(self):
        if self.quanty and self.unit_price:
            amount = self.quanty * self.unit_price
            self.subtotal = amount
        else:
            self.subtotal = 0