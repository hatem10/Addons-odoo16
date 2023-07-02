from odoo import models,fields,api

class DetailInvoice(models.Model):
    _name="bodega.detail_invoice"
    _description="Detalle de Factura"
    
    name=fields.Char(string="Factura",readonly=True)
    customer=fields.Char(string="Cliente")
    ruc=fields.Char(string="RUC")
    address=fields.Char(string="Direccion")
    sale_product_id=fields.One2many(string="Producto",comodel_name="bodega.sale_product",
                                    inverse_name="detail_invoice_id")
    sub_total=fields.Float(string="Sub Total",digits=(12,2),compute="compute_amount_totales")
    igv=fields.Float(string="IGV 18%",digits=(12,2),compute="compute_amount_totales")
    total=fields.Float(string="Total",digits=(12,2),compute="compute_amount_totales")
    comment=fields.Text(string="Comentario")
    

    def compute_amount_totales(self):
        if self.sale_product_id.price_total:
            print("***Se ingreso Pric total***")
            amount_sub_total=0
            for rec in self:
                for a in rec.sale_product_id:
                    amount_sub_total+=a.price_total
                rec.sub_total=amount_sub_total
                rec.igv=rec.sub_total*0.18
                rec.total=rec.sub_total+rec.igv
        else:
            print("No ingreso Price Total")
            self.sub_total=0.00
            self.igv=0.00
            self.total=0.00
        


    @api.model
    def create(self,values):
        invoice=self.env['ir.sequence'].next_by_code('invoice.detail_invoice')
        values['name']=invoice
        return super(DetailInvoice,self).create(values)