from odoo import fields, models


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "All product brands are mentioned here"
    _rec_name = "brand_name"

    brand_name = fields.Char(string="Product Brand")
    brand_image = fields.Binary(string="Brand Photo")
    brand_desc = fields.Html(string="Description")
    product_details = fields.One2many("product.template", "product_brand")
    brand_sale = fields.Integer("Brand Sale Count", compute="compute_brand_sale")

    def compute_brand_sale(self):
        for record in self:
            record.brand_sale = self.env["sale.order.line"].search_count(
                [("product_template_id.product_brand", "=", self.id)]
            )

    def action_brand_sale(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Brand Sale",
            "view_mode": "tree,kanban",
            "res_model": "sale.order.line",
            "domain": [("product_template_id.product_brand", "=", self.id)],
            "context": "{'create': False}",
        }
