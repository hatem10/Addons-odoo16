from odoo import models,fields,api,exceptions

class Product(models.Model):
    _name='bodega.purchase_product'
    _description='Compra de Productos'

    name=fields.Char(string="Producto",required=True)
    description=fields.Char(string="Descripcion")
    quanty=fields.Integer(string="Cantidad")
    price_unit=fields.Float(string="Precio/Unit")
    price_total=fields.Float(string="Total",required=True)

    @api.onchange('quanty','price_unit')
    def onchange_price_total(self):
        print("***Testeando****")
        if self.quanty and self.price_unit:
            self.price_total=self.price_unit*self.quanty
        else:
            self.price_total=0

    @api.model
    def create(self,values):
        return super(Product,self).create(values)
    
    def btn_delete(self):
        pass

    def btn_update(self):
        pass
    