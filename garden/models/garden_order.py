from odoo import models,fields,api
from ..services.utils import OPTION_STATE
class Order(models.Model):
    _name = "garden.order"
    _description = "Pedido"
    _inherit = "mail.thread"

    name = fields.Char(string="Codigo",tracking=True)
    date_order = fields.Date(string="Fecha")
    date_expected = fields.Date(string="Fecha Esperada")
    date_delivery = fields.Date(string="Fecha Entregada")
    state = fields.Selection(string="Estado",selection=OPTION_STATE)
    comment = fields.Html(string="Comentario")
    id_customer = fields.Many2one(string="Cliente",comodel_name="garden.customer")