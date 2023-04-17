from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    _description = "Purchase Order Line"

    total_amount_with_cost = fields.Float(string="Extra Price List", related="product_id.total_amount_with_cost")
