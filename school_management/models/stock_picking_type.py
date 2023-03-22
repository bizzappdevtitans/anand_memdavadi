from odoo import models, fields


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    auto_invoice = fields.Boolean(string="Auto Invoice")
