from odoo import models,fields,api
from ..services.utils import TYPE_DOCUMENT,TYPE_STATE
from datetime import datetime

class MoviePresupuesto(models.Model):
    _name = "movie.presupuesto"
    _description = "Presupuesto de Peliculas"
    _inherit = "mail.thread"

    name = fields.Char(string="Presupuesto",tranking=True)
    customer_id = fields.Many2one(string="Cliente",comodel_name="res.partner",required=True,tracking=True)
    document = fields.Selection(string="Documento",selection=TYPE_DOCUMENT,required=True,tracking=True)
    number_document = fields.Char(string="Numero",required=True,tracking=True)
    currency_id = fields.Many2one(string="Moneda",comodel_name="res.currency",required=True,tracking=True)
    date_pre = fields.Datetime(string="Fecha de Presupuesto",required=True,tracking=True)
    state = fields.Selection(selection=TYPE_STATE,tracking=True)
    amount_base = fields.Monetary(string="Base Imponible:",compute="_compute_amounts")
    amount_tax = fields.Monetary(string="IGV:")
    amount_total = fields.Monetary(string="Total:",compute="_compute_amounts")
    note = fields.Text(string="Nota")
    detail_pre_ids = fields.One2many(comodel_name="movie.detail.presupuesto",inverse_name="movie_pre_id")

    def default_get(self,fields):
        res = super(MoviePresupuesto,self).default_get(fields)
        res["document"] = "dni"
        res["date_pre"] = datetime.now()
        return res

    @api.model
    def create(self,values):
        values["name"] = self.env["ir.sequence"].next_by_code("movie.presupuesto.name")
        values["state"] = "draft"
        return super(MoviePresupuesto,self).create(values)

    @api.depends("detail_pre_ids.price_subtotal")
    def _compute_amounts(self):
        for rec in self:
            rec.amount_base = sum([p_subtotal.price_subtotal for p_subtotal in rec.detail_pre_ids])
            rec.amount_tax =  sum([igv.price_subtotal * (1 - (igv.tax_id.amount)/100) for igv in rec.detail_pre_ids])
            rec.amount_total = rec.amount_base + rec.amount_tax


    def btn_draft(self):
        self.write({"state":"draft"})

    def btn_approved(self):
        self.write({"state":"approved"})

    def btn_done(self):
        self.write({"state":"done"})

    _sql_constraints = [
        ("unique_name", "unique(name)","!!!....No puede haber Presupuesto con Numero Iguales.....!!!!"),
        ("unique_number_document","unique(number_document)","!!!....No puede haber Documentos iguales.....!!!!")
    ]
class MovieDetailPresupuesto(models.Model):
    _name = "movie.detail.presupuesto"
    _description = "Detalle Presupuesto"

    movie_id = fields.Many2one(string="Pelicula",comodel_name="movie")
    quanty = fields.Integer(string="Cantidad")
    price_unit = fields.Float(string="Precio Unitario")
    tax_id = fields.Many2one(string="Impuesto",comodel_name="account.tax")
    price_subtotal = fields.Monetary(string="Subtotal")
    movie_pre_id = fields.Many2one(comodel_name="movie.presupuesto")
    currency_id = fields.Many2one(related="movie_pre_id.currency_id")

    @api.onchange("quanty","price_unit")
    def _onchange_price_subtotal(self):
        if self.quanty and self.price_unit:
            self.price_subtotal = self.quanty * self.price_unit
        else:
            self.price_subtotal = 0