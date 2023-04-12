from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_brand = fields.Many2one(
        "product.brand", string="PRODUCT BRAND", ondelete="cascade"
    )

    recent_so = fields.One2many(
        "sale.order.line",
        "product_id",
        string="5 Sale Order",
        compute="_last_five_sale_order",
    )
    recent_po = fields.One2many(
        "purchase.order.line",
        "product_id",
        string="5 Purchase Order",
        limit=5,
        compute="_last_five_purchase_order",
    )

    def _last_five_sale_order(self):
        for rec in self:
            orders = self.env["sale.order.line"].search(
                [("product_id", "=", rec.id)], limit=5
            )
            rec.recent_so = orders

    def _last_five_purchase_order(self):
        for rec in self:
            orders = self.env["purchase.order.line"].search(
                [("product_id", "=", rec.id)], limit=5
            )
            rec.recent_po = orders
