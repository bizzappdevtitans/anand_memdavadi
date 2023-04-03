from odoo import fields, api, models, _
from datetime import date, datetime
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _name = "electronic.employee"
    _description = "Employee in SHOP"
    _rec_name = "emp_name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    emp_name = fields.Char(string="Employee Name", required=True)
    reference_no = fields.Char(
        string="Employee Reference",
        readonly=True,
        required=True,
        default=lambda self: _("New"),
    )
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", help="Student's Age", compute="_compute_age")
    image = fields.Binary("Employee Photo")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
        tracking=True,
    )
    email = fields.Char(string="Email")
    joining_date = fields.Datetime(string="Date of joining")
    contact_no = fields.Char(string="Phone Number")
    adhaar_no = fields.Char(string="Adhaar Number")
    pan_no = fields.Char(string="PAN Number")
    qualification = fields.Selection(
        [
            ("under_graduate", "Under Graduate"),
            ("graduate", "Graduate"),
            ("post_graduate", "Post Graduate"),
        ],
        string="Qualification",
    )
    address = fields.Text(string="Residential Address")
    active = fields.Boolean("Active", default=True)
    sale_count = fields.Integer(compute="compute_sale_emp", tracking=True)
    all_sale_order_count = fields.Integer(compute="_compute_all_sale_order")
    progress = fields.Float(compute="_compute_progress")
    user_id = fields.Many2one("res.users", string="Select User")
    branch = fields.Many2one(
        "electronic.management", string="Branch", ondelete="cascade"
    )

    """While creating employee add prefix based on gender"""

    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "electronic.employee"
            ) or _("New")
            res = super(Employee, self).create(vals)
            if vals.get("gender") == "male":
                res["emp_name"] = "Mr." + res["emp_name"]
            elif vals.get("gender") == "female":
                res["emp_name"] = "Mrs." + res["emp_name"]
            else:
                return res
        return res

    """Added name_get to add employee with ref_no and name """

    def name_get(self):
        emp_list = []
        for rec in self:
            emp_list.append((rec.id, "%s - %s" % (rec.reference_no, rec.emp_name)))
        return emp_list

    """Used to compute employee age"""

    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    """Used for cronjob to send message in general on birthday"""

    def message_in_general_channel(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        employees = self.env["electronic.employee"].search([("active", "=", True)])
        for employee in employees:
            bday_month = employee.dob.strftime("%m")
            bday_date = employee.dob.strftime("%d")
            if bday_date == today_date and bday_month == today_month:
                message = "Happy Birthday %s" % (employee.emp_name)
                channel_id = self.env.ref("mail.channel_all_employees").id
                channel = self.env["mail.channel"].browse(channel_id)
                channel.message_post(
                    body=(message),
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )

    """Used to calculate employee sale order"""

    def compute_sale_emp(self):
        for record in self:
            record.sale_count = self.env["sale.order"].search_count(
                [("sale_emp", "=", self.id)]
            )

    """Added action for smart button to see sale order record"""

    def get_sales(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sale",
            "view_mode": "tree",
            "res_model": "sale.order",
            "domain": [("sale_emp", "=", self.id)],
            "context": "{'create': False}",
        }

    """Calculates all sale order"""

    def _compute_all_sale_order(self):
        for record in self:
            record.all_sale_order_count = self.env["sale.order"].search_count([])

    """Progress of employee will be calculated based on sale order created"""

    def _compute_progress(self):
        for rec in self:
            rec.progress = 0
            rec.progress = (rec.sale_count / rec.all_sale_order_count) * 100

    """Used in cron job to send email on birthday"""

    def check_bday_emp(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        employees = self.env["electronic.employee"].search([])
        for employee in employees:
            if employee.email:
                bday_month = employee.dob.strftime("%m")
                bday_date = employee.dob.strftime("%d")
                if bday_date == today_date and bday_month == today_month:
                    template = self.env.ref(
                        "electronic_management.employee_birthday_mail"
                    )
                    template.send_mail(employee.id)

    """Added name_search to find employee based on ref_no and adhaar_number"""

    @api.model
    def _name_search(
        self, emp_name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if not (emp_name == "" and operator == "ilike"):
            args += [
                "|",
                "|",
                (self._rec_name, operator, emp_name),
                ("reference_no", operator, emp_name),
                ("adhaar_no", operator, emp_name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    """Added ValidationError for phone number to be of 10 digit"""

    @api.constrains("contact_no")
    def check_phone(self):
        for rec in self:
            if len(rec.contact_no) < 10 or len(rec.contact_no) > 10:
                raise ValidationError(("Phone number should be of 10 digit only"))

    """Added validationerror for Adhaar number to be of 12 digit"""

    @api.constrains("adhaar_no")
    def check_adhaar(self):
        for rec in self:
            if len(rec.adhaar_no) < 12 or len(rec.adhaar_no) > 12:
                raise ValidationError(("Adhaar Number should be of 12 digit only"))
