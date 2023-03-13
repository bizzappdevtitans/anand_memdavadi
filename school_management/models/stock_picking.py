from odoo import models, fields


class Picking(models.Model):
    _inherit = "stock.picking"

    sp_des = fields.Char(string="Delivery Description")
