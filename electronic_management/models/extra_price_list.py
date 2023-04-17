from odoo import fields, models


class ExtraPriceList(models.Model):
    _name = "extra.pricelist"
    _description = "Extra Price List of Product"
    _rec_name = "extra_price_name"

    extra_price_name = fields.Char(string="Extra Price Name", required=True)
    extra_price = fields.Float(string="Extra Price Rate", required=True)
