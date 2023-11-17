from odoo import models, fields, api


class CustomerWhatsappWizard(models.TransientModel):
    _name = "customer.whatsapp.wizard"
    _description = "Enviar WhatsApp a Cliente"

    customer_id = fields.Many2one(string="Cliente",comodel_name="order.customer")
    cell_mobile = fields.Char(string="Celular",related="customer_id.cell_phone")
    message = fields.Text(string="Mensaje",required=True)

    def send_message_whatsapp(self):
        if self.cell_mobile and self.message:
            message_string = ""
            message = self.message.split(" ")
            for msg in message:
                message_string = message_string + msg + "%20"
            message_string = message_string[0:len(message_string)-3]
            return {
                "type":"ir.actions.act_url",
                "url":"https://api.whatsapp.com/send?phone=%s&text=%s" %(self.cell_mobile,message_string),
                "target":"new",
                "res_id":self.id
            }