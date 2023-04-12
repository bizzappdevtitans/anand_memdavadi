from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    Category = fields.Selection(
        [
            ("tv", "TV"),
            ("mobile", "Mobile"),
            ("fridge", "Refridgerator"),
            ("washing_machine", "Washing Machine"),
        ],
        string="Device Category",
    )
    product_brand = fields.Many2one(
        "product.brand", string="PRODUCT BRAND", ondelete="cascade"
    )
    website = fields.Char(string="Website for Product Details")
    _sql_constraints = [("unique_tag_name", "unique (name)", "Product already exists")]

    """Name get function to append product brand name and product name"""

    def name_get(self):
        product_list = []
        for rec in self:
            product_list.append(
                (rec.id, "%s-%s" % (rec.product_brand.brand_name, rec.name))
            )
        return product_list

    """Action given to WhatsApp Integration"""

    def action_url(self):
        return {"type": "ir.actions.act_url", "target": "new", "url": self.website}
