from odoo import models,fields,api
from ..services.utils import OPTION_STATE
class Order(models.Model):
    _name = "garden.order"
    _description = "Pedido"
    _inherit = "mail.thread"

    name = fields.Char(string="Codigo",tracking=True)
    date_order = fields.Date(string="Fecha",tracking=True)
    date_expected = fields.Date(string="Fecha Esperada",tracking=True)
    date_delivery = fields.Date(string="Fecha Entregada",tracking=True)
    state = fields.Selection(string="Estado",selection=OPTION_STATE,tracking=True)
    comment = fields.Html(string="Comentario",tracking=True)
    id_customer = fields.Many2one(string="Cliente",comodel_name="garden.customer",tracking=True)

    def btn_pendient(self):
        self.state = "pendient"

    def btn_deliveried(self):
        self.state = "deliveried"

    def btn_rejected(self):
        self.state = "rejected"