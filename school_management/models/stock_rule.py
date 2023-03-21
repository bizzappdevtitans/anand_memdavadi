from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_mo_vals(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
        bom,
    ):
        mo_val = super(StockRule, self)._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
        )
        mo_val["mrp_des"] = values.get("mrp_des")
        return mo_val

    def _prepare_purchase_order(self, company_id, origins, values):
        po_vals = super(StockRule, self)._prepare_purchase_order(
            company_id, origins, values
        )
        po_vals["purchase_des"] = values.get("purchase_des")
        return po_vals

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
    ):
        vals = super(StockRule, self)._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
        )
        vals["product_weight"] = values.get("product_weight")
        return vals
