from odoo import fields, models


class ProductInherited(models.Model):
    _inherit = "product.product"

    weight = fields.Boolean(string="Has weight ?")
