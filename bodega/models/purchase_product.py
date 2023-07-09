from odoo import models,fields,api,exceptions
from datetime import date

class Product(models.Model):
    _name='bodega.purchase_product'
    _description='Compra de Productos'

    name=fields.Char(string="Producto",required=True)
    description=fields.Char(string="Descripcion")
    quanty=fields.Integer(string="Cantidad")
    price_unit=fields.Float(string="Precio/Unit")
    price_total=fields.Float(string="Total",required=True)
    date_purchase=fields.Date(string="Fecha/Compra",default=lambda self:date.today())
    sale_product_id=fields.Many2one(comodel_name="bodega.sale_product",compute="compute_sale_product_id")
    quanty_sale_product=fields.Integer(string="Cantidad/Venta",related="sale_product_id.quanty")
    stock_product=fields.Integer(string="Stock")


    def compute_sale_product_id(self):
        for rec in self:
            sale_product=rec.env['bodega.sale_product'].search([('name','=',rec.id)])
            if sale_product:
                rec.sale_product_id=sale_product.id
            else:
                rec.sale_product_id=None



    @api.onchange('quanty','price_unit')
    def onchange_price_total(self):

        if self.quanty and self.price_unit:
            self.price_total=self.price_unit*self.quanty
        else:
            self.price_total=0
        
        if self.quanty:
            print("****Onchange stock***")
            print(self.quanty_sale_product)
            self.stock_product=self.quanty - self.quanty_sale_product
        else:
            self.stock_product=0

    @api.model
    def create(self,values):
        return super(Product,self).create(values)
    
    def btn_delete(self):
        pass

    def btn_update(self):
        pass
    