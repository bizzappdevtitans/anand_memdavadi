from odoo import fields, models, api, _


class ElectronicManagement(models.Model):
    _name = "electronic.management"
    _description = "electronic.management"
    _rec_name = "branch_name"

    branch_name = fields.Char(string="Branch Name")
    branch_no = fields.Char(
        string="Branch Number",
        readonly=True,
        required=True,
        default=lambda self: _("New"),
    )
    branch_address = fields.Text(string="Address")
    emp = fields.One2many("electronic.employee", "branch", string="Employees")
    sale_count = fields.Integer(compute="compute_sale")

    """Used for Sequence Number"""

    @api.model
    def create(self, vals):
        if vals.get("branch_no", _("New")) == _("New"):
            vals["branch_no"] = self.env["ir.sequence"].next_by_code(
                "electronic.management"
            ) or _("New")
            res = super(ElectronicManagement, self).create(vals)
            return res

    """Used to Branch name along with branch number"""

    def name_get(self):
        branch_list = []
        for rec in self:
            branch_list.append((rec.id, "%s - %s" % (rec.branch_no, rec.branch_name)))
        return branch_list

    """To calculate sale of particular branch"""

    def compute_sale(self):
        for record in self:
            record.sale_count = self.env["sale.order"].search_count(
                [("branch", "=", self.id)]
            )

    """Action for smart button to view Sale Order"""

    def get_sales(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sale",
            "view_mode": "tree",
            "res_model": "sale.order",
            "domain": [("branch", "=", self.id)],
            "context": "{'create': False}",
        }
