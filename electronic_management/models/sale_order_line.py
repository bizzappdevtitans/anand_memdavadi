from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    categ_id = fields.Many2one("product.category", string="Product Category")

    @api.onchange("categ_id")
    def onchange_category(self):
        return {
            "domain": {"product_template_id": [("categ_id", "=", self.categ_id.id)]}
        }
