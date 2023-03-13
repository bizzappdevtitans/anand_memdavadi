from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    mrp_des = fields.Char(string="Description from SO")
