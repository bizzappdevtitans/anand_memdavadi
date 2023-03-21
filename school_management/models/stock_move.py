from odoo import models, fields


class StockMove(models.Model):
    _inherit = "stock.move"
    product_weight = fields.Integer(string="weight in DOL")

    def _prepare_procurement_values(self):
        vals = super(StockMove, self)._prepare_procurement_values()
        vals["mrp_des"] = self.sale_line_id.order_id.manu_order_des
        vals["purchase_des"] = self.sale_line_id.order_id.purchase_order_des
        return vals

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        vals["sp_des"] = self.group_id.sale_id.delivery_des
        return vals
