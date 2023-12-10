from odoo import models,fields,api

class YearSchool(models.Model):
    _name = "university.year.school"
    _description = "Año Escolar"
    _inherit = "mail.thread"

    name = fields.Char(string="Año Escolar",tracking=True)
    year_start = fields.Date(string="Inicio",tracking=True)
    year_end = fields.Date(string="Termina",tracking=True)

    @api.onchange("year_start","year_end")
    def _onchange_name(self):
        if self.year_start and self.year_end:
            self.name = "Periodo [%s - %s]" %(self.year_start.strftime("%Y"),self.year_end.strftime("%Y"))
        else:
            self.name = ""

