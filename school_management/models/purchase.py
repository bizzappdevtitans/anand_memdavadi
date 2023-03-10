from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_des = fields.Char(string="Description from SO")
