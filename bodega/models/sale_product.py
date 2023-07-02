from odoo import models,fields,api,exceptions

class SaleProduct(models.Model):
    _name='bodega.sale_product'
    _description='Compra de Productos'

    name=fields.Char(string="Producto",required=True)
    description=fields.Char(string="Descripcion")
    quanty=fields.Integer(string="Cantidad")
    price_unit=fields.Float(string="Precio/Unit")
    price_total=fields.Float(string="Total")

    @api.model
    def create(self,values):
        return super(SaleProduct,self).create(values)
    
    def btn_delete(self):
        pass

    def btn_update(self):
        pass
    