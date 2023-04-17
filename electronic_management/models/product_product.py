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
    extra_price_of_product = fields.Many2many('extra.pricelist', string='Extra Price List of Product')
    total_amount = fields.Float(string='Total extra amount', compute='_amount_total')
    total_amount_with_cost = fields.Float(string='Final Total Amount with cost', compute="_total_amount_with_cost")

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

    def _amount_total(self):
        for rec in self:
            total = sum(rec.extra_price_of_product.mapped('extra_price')) if rec.extra_price_of_product else 0
            rec.total_amount = total

    def _total_amount_with_cost(self):
        for rec in self:
            if rec.standard_price:
                rec.total_amount_with_cost = rec.standard_price*rec.total_amount
            else:
                rec.total_amount_with_cost = 0
