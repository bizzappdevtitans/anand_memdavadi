from odoo import models, fields


class Picking(models.Model):
    _inherit = "stock.picking"

    sp_des = fields.Char(string="Delivery Description")
    product_weight = fields.Integer(string="weight in DOL")
