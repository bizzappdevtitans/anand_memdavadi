from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_emp = fields.Many2one(
        "electronic.employee", string="Sale Employee", required=True, ondelete="cascade"
    )
    branch = fields.Many2one(
        "electronic.management", string="Branch", ondelete="cascade"
    )

    """WhatsApp Integration in SO"""

    def whatsapp_invoice(self):
        message = (
            "Hi %s, we received your order %s for product %s. Your payment amount is %s. Thank you!"
            % (
                self.partner_id.name,
                self.name,
                self.order_line.product_id.name,
                self.amount_total,
            )
        )
        whatsapp_api_url = "https://api.whatsapp.com/send?phone=%s&text=%s" % (
            self.partner_id.phone,
            message,
        )
        return {"type": "ir.actions.act_url", "target": "new", "url": whatsapp_api_url}

    """When branch changes than employee list will be shown of that particular branch"""

    @api.onchange("branch")
    def onchange_branch(self):
        return {"domain": {"sale_emp": [("branch", "=", self.branch.id)]}}

    # @api.onchange("partner_id")
    # def onchange_partner(self):
    #     print("\nOnchange Triggered\n")
    #     print(self.partner_shipping_id.name)
    #     p_id = self.partner_shipping_id.filtered(lambda la: la.check_true == True)
    #     print(p_id.id)
    #     return p_id

        # for rec in self:
        #     partner = self.env["res.partner"].search(
        #         [("type", "=", "delivery"), ("check_true", "=", True)]
        #     )
        #     partner_shipping_id = partner.filtered(lambda l: l.check_true == True)
        #     print(partner_shipping_id)
        #     return partner_shipping_id

    # for rec in self:
    #     partner_shipping_id = rec.partner_shipping_id.filtered(
    #         lambda la: la.check_true == 'True' and la.type == 'delivery'
    #     )

    @api.onchange("partner_id")
    def onchange_partners(self):
        print("Onchange Triggered")
        for rec in self:
            return {
                "domain": {
                    "partner_shipping_id": [
                        ("type", "=", "delivery"),
                        ("check_true", "=", True),
                        ("id", "in", rec.partner_id.child_ids.ids),
                    ],
                }
            }

    # @api.model
    # def create(self, vals):
    #     partner = self.env["res.partner"].search(
    #         [
    #             ("type", "=", "delivery"),
    #             ("check_true", "=", True),
    #             ("id", "in", self.partner_id.child_ids.ids),
    #         ]
    #     )
    #     vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', partner)
    #     result = super(SaleOrder, self).create(vals)
    #     return result
