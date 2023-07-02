from odoo import models,fields,api

class DetailInvoice(models.Model):
    _name="bodega.detail_invoice"
    _description="Detalle de Factura"
    
    name=fields.Char(string="Codigo")
    customer=fields.Char(string="Cliente")
    ruc=fields.Char(string="RUC")
    address=fields.Char(string="Direccion")
    sale_product_id=fields.One2many(string="Producto",comodel_name="bodega.sale_product",
                                    inverse_name="detail_invoice_id")
    

    