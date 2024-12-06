# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class GeneralAudit(models.Model):
    _name = "general_audit"
    _description = "General Audit"
    _inherit = [
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_cancel",
        "mixin.transaction_partner",
    ]

    # Attributes related to multiple approval
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,open,confirm,done"

    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    _create_sequence_state = "open"

    title = fields.Char(
        string="Title",
        default="-",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Date(
        string="Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Date(
        string="End Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    need_interim = fields.Boolean(
        string="Need Interim",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    need_previous = fields.Boolean(
        string="Need Previous",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self._default_currency_id(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_type_set_id = fields.Many2one(
        string="Account Type Set",
        comodel_name="client_account_type_set",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    financial_accounting_standard_id = fields.Many2one(
        string="Financial Accounting Standard",
        comodel_name="accountant.financial_accounting_standard",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    opinion_id = fields.Many2one(
        string="Opinion",
        comodel_name="accountant.opinion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    accountant_id = fields.Many2one(
        string="Accountant",
        comodel_name="res.partner",
        domain=[
            ("is_company", "=", False),
            ("parent_id", "=", False),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    num_of_consecutive_audit_firm = fields.Integer(
        string="Num. of Consecutive Audit (Firm)",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    num_of_consecutive_audit_accountant = fields.Integer(
        string="Num. of Consecutive Audit (Accountant)",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    restatement_option = fields.Selection(
        string="Restatement Option",
        selection=[
            ("no", "Not a restatement"),
            ("internal", "Restated audit exist in Odoo"),
            ("external", "Restated audit does not exist in Odoo"),
        ],
        required=True,
        default="no",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_audit_id = fields.Many2one(
        string="Previous # Audit",
        comodel_name="general_audit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    previous_audit = fields.Char(
        string="Previous Audit",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    required_worksheet_type_ids = fields.Many2many(
        string="Required Worksheet Type(s)",
        comodel_name="general_audit_worksheet_type",
        relation="rel_general_audit_2_required_worksheet_type",
        column1="general_audit_id",
        column2="worksheet_type_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    additional_worksheet_type_ids = fields.Many2many(
        string="Additional Worksheet Type(s)",
        comodel_name="general_audit_worksheet_type",
        relation="rel_general_audit_2_additional_worksheet_type",
        column1="general_audit_id",
        column2="worksheet_type_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    worksheet_ids = fields.One2many(
        string="Worksheets",
        comodel_name="general_audit_worksheet",
        inverse_name="general_audit_id",
        readonly=True,
    )
    worksheet_control_ids = fields.One2many(
        string="Controls",
        comodel_name="general_audit.worksheet_control",
        inverse_name="general_audit_id",
        readonly=True,
    )
    trial_balance_ids = fields.One2many(
        string="Trial Balance",
        comodel_name="client_trial_balance",
        inverse_name="general_audit_id",
        readonly=True,
    )
    home_trial_balance_id = fields.Many2one(
        string="# Home Statement Trial Balance",
        comodel_name="client_trial_balance",
        compute="_compute_trial_balance_id",
        store=True,
    )
    interim_trial_balance_id = fields.Many2one(
        string="# Interim Trial Balance",
        comodel_name="client_trial_balance",
        compute="_compute_trial_balance_id",
        store=True,
    )
    previous_trial_balance_id = fields.Many2one(
        string="# Previous Trial Balance",
        comodel_name="client_trial_balance",
        compute="_compute_trial_balance_id",
        store=True,
    )
    account_mapping_ids = fields.One2many(
        string="Account Mappings",
        comodel_name="client_account_mapping",
        inverse_name="general_audit_id",
    )
    account_mapping_id = fields.Many2one(
        string="# Account Mapping",
        comodel_name="client_account_mapping",
        compute="_compute_account_mapping_id",
        store=True,
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="general_audit.detail",
        inverse_name="general_audit_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
        copy=False,
    )
    standard_detail_ids = fields.One2many(
        string="Standard Detail",
        comodel_name="general_audit.standard_detail",
        inverse_name="general_audit_id",
        readonly=True,
        copy=True,
    )
    group_detail_ids = fields.One2many(
        string="Group Detail",
        comodel_name="general_audit.group_detail",
        inverse_name="general_audit_id",
        readonly=True,
        copy=True,
    )
    computation_ids = fields.One2many(
        string="Computations",
        comodel_name="general_audit.computation",
        inverse_name="general_audit_id",
        readonly=True,
        copy=True,
    )
    standard_adjustment_ids = fields.One2many(
        string="Standard Adjustment",
        comodel_name="general_audit.adjustment",
        inverse_name="general_audit_id",
        readonly=True,
    )
    account_adjustment_ids = fields.One2many(
        string="Account Adjustment",
        comodel_name="general_audit.account_adjustment",
        inverse_name="general_audit_id",
        readonly=True,
    )
    group_adjustment_ids = fields.One2many(
        string="Group Adjustment",
        comodel_name="general_audit.group_adjustment",
        inverse_name="general_audit_id",
        readonly=True,
    )
    adjustment_entry_ids = fields.One2many(
        string="Adjustment Entri(es)",
        comodel_name="client_adjustment_entry",
        inverse_name="general_audit_id",
        readonly=True,
    )
    account_type_ids = fields.Many2many(
        string="Account Types",
        comodel_name="client_account_type",
        compute="_compute_account_type_ids",
        store=False,
        compute_sudo=True,
    )

    @api.model
    def _get_policy_field(self):
        res = super(GeneralAudit, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "open_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.depends(
        "account_type_set_id",
    )
    def _compute_policy(self):
        _super = super(GeneralAudit, self)
        _super._compute_policy()

    @api.depends(
        "standard_detail_ids",
        "standard_detail_ids.type_id",
    )
    def _compute_account_type_ids(self):
        for record in self:
            record.account_type_ids = record.standard_detail_ids.mapped("type_id")

    @api.depends(
        "account_mapping_ids",
        "account_mapping_ids.state",
    )
    def _compute_account_mapping_id(self):
        for record in self:
            result = False
            # TODO: Check
            criteria = [("general_audit_id", "=", record.id)]
            mappings = self.env["client_account_mapping"].search(criteria)

            if len(mappings) > 0:
                result = mappings[0]
            record.account_mapping_id = result

    @api.depends(
        "trial_balance_ids",
        "trial_balance_ids.trial_balance_type",
    )
    def _compute_trial_balance_id(self):
        for document in self:
            home = interim = previous = False

            # Home statement
            homes = document.trial_balance_ids.filtered(
                lambda r: r.trial_balance_type == "home"
            )
            if len(homes) > 0:
                home = homes[0]

            # Interim
            interims = document.trial_balance_ids.filtered(
                lambda r: r.trial_balance_type == "interim"
            )
            if len(interims) > 0:
                interim = interims[0]

            # Previous
            previouses = document.trial_balance_ids.filtered(
                lambda r: r.trial_balance_type == "previous"
            )
            if len(previouses) > 0:
                previous = previouses[0]

            document.home_trial_balance_id = home
            document.interim_trial_balance_id = interim
            document.previous_trial_balance_id = previous

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)

    @api.constrains("interim_date_start", "interim_date_end")
    def _check_interim_date_start_end(self):
        for record in self:
            if record.interim_date_start and record.interim_date_end:
                strWarning = _(
                    "Interim Date end must be greater than Interim Date start"
                )
                if record.interim_date_end < record.interim_date_start:
                    raise UserError(strWarning)

    @api.constrains("previous_date_start", "previous_date_end")
    def _check_previous_date_start_end(self):
        for record in self:
            if record.previous_date_start and record.previous_date_end:
                strWarning = _(
                    "Previous Date end must be greater than Previous date start"
                )
                if record.previous_date_end < record.previous_date_start:
                    raise UserError(strWarning)

    @api.constrains("interim_date_start", "previous_date_end")
    def _check_previous_interim_date(self):
        for record in self:
            if record.interim_date_start and record.previous_date_end:
                strWarning = _(
                    "Interim Date start must be greater than previous Interim Date end"
                )
                if record.previous_date_end >= record.interim_date_start:
                    raise UserError(strWarning)

    # @api.onchange("account_type_set_id")
    # def onchange_standard_detail_ids(self):
    #     self.update({"standard_detail_ids": [(5, 0, 0)]})
    #     if self.account_type_set_id:
    #         result = []
    #         for detail in self.account_type_set_id.detail_ids:
    #             result.append(
    #                 (
    #                     0,
    #                     0,
    #                     {
    #                         "sequence": detail.sequence,
    #                         "type_id": detail.id,
    #                     },
    #                 )
    #             )
    #         self.update({"standard_detail_ids": result})

    # @api.onchange("account_type_set_id")
    # def onchange_group_detail_ids(self):
    #     self.update({"group_detail_ids": [(5, 0, 0)]})
    #     AccountGroup = self.env["accountant.client_account_group"]
    #     if self.account_type_set_id:
    #         result = []
    #         criteria = []
    #         for detail in AccountGroup.search(criteria):
    #             result.append(
    #                 (
    #                     0,
    #                     0,
    #                     {
    #                         "sequence": detail.sequence,
    #                         "group_id": detail.id,
    #                     },
    #                 )
    #             )
    #         self.update({"group_detail_ids": result})

    # @api.onchange("account_type_set_id")
    # def onchange_computation_ids(self):
    #     self.update({"computation_ids": [(5, 0, 0)]})
    #     if self.account_type_set_id:
    #         result = []
    #         for detail in self.account_type_set_id.computation_ids:
    #             result.append(
    #                 (
    #                     0,
    #                     0,
    #                     {
    #                         "computation_item_id": detail.computation_id.id,
    #                     },
    #                 )
    #             )
    #         self.update({"computation_ids": result})

    @api.constrains(
        "state",
    )
    def _constrains_state_confirm(self):
        for record in self.sudo():
            record._check_home_tb_exist()
            record._check_home_tb_done()
            record._check_previous_tb_exist()
            record._check_previous_tb_done()
            record._check_interim_tb_done()
            record._check_required_worksheet()
            record._check_additional_worksheet()

    def _check_home_tb_exist(self):
        self.ensure_one()
        if not self.home_trial_balance_id and self.state == "confirm":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: No home statement trial balance
            Solution: Create home statement trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_home_tb_done(self):
        self.ensure_one()
        if self.state == "confirm" and self.home_trial_balance_id.state != "done":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: Home statement trial balance is not finished
            Solution: Finish home statement trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_previous_tb_exist(self):
        self.ensure_one()
        if (
            not self.previous_trial_balance_id
            and self.state == "confirm"
            and self.need_previous
        ):
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: No previous trial balance
            Solution: Create previous trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_previous_tb_done(self):
        self.ensure_one()
        if (
            self.state == "confirm"
            and self.previous_trial_balance_id.state != "done"
            and self.need_previous
        ):
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: Previous trial balance is not finished
            Solution: Finish Previous trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_interim_tb_exists(self):
        self.ensure_one()
        if (
            not self.interim_trial_balance_id
            and self.state == "confirm"
            and self.need_previous
        ):
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: No interim trial balance
            Solution: Create interim trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_interim_tb_done(self):
        self.ensure_one()
        if (
            self.interim_trial_balance_id
            and self.interim_trial_balance_id.state != "done"
            and self.state == "confirm"
            and self.need_interim
        ):
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: Interim trial balance is not finished
            Solution: Finish interim trial balance
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_required_worksheet(self):
        self.ensure_one()
        worksheet_state = True
        for worksheet in self.worksheet_control_ids:
            if worksheet.state != "done" and worksheet.required:
                worksheet_state = False
                break

        if not worksheet_state and self.state == "confirm":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: One of the required worksheet not done
            Solution: Create and finish required worksheet
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _check_additional_worksheet(self):
        self.ensure_one()
        worksheet_state = True
        for worksheet in self.worksheet_control_ids:
            if (
                worksheet.state not in ["done", "cancel"]
                and not worksheet.required
                and worksheet.worksheet_id
            ):
                worksheet_state = False
                break

        if not worksheet_state and self.state == "confirm":
            error_message = """
            Context: Confirming general audit
            Database ID: %s
            Problem: One of the additional worksheet not done
            Solution: Finish or cancel additional worksheet
            """ % (
                self.id
            )
            raise ValidationError(_(error_message))

    def _recompute_extrapolation_computation(self):
        self.ensure_one()
        additional_dict = self._get_extrapolation_account_type_dict()
        for computation in self.computation_ids:
            additionaldict = computation._recompute_extrapolation(additional_dict)
            additional_dict = additionaldict

    def _get_extrapolation_account_type_dict(self):
        self.ensure_one()
        result = {
            "account_type": {},
            "account_group": {},
        }
        for standard in self.standard_detail_ids:
            result["account_type"].update(
                {
                    standard.type_id.code: standard.adjusted_extrapolation_balance,
                }
            )
            account_group_amount = result["account_group"].get(
                standard.type_id.group_id.code, 0.0
            )
            result["account_group"].update(
                {
                    standard.type_id.group_id.code: account_group_amount
                    + standard.adjusted_extrapolation_balance,
                }
            )
        return result

    def action_reload_account(self):
        for record in self.sudo():
            record._reload_account()

    def _reload_account(self):
        self.ensure_one()

        self.detail_ids.unlink()

        if not self.account_mapping_id:
            return True

        Detail = self.env["general_audit.detail"]

        for account in self.account_mapping_id.detail_ids:
            Detail.create(
                {
                    "general_audit_id": self.id,
                    "account_id": account.account_id.id,
                }
            )

    def action_reload_standard_account(self):
        for record in self.sudo():
            record._reload_standard_account()

    def _reload_standard_account(self):
        self.ensure_one()
        standard_details = self.account_type_set_id.detail_ids
        StandardDetail = self.env["general_audit.standard_detail"]
        self.standard_detail_ids.unlink()
        for standard_detail in standard_details:
            StandardDetail.create(
                {
                    "general_audit_id": self.id,
                    "type_id": standard_detail.id,
                }
            )
        self._reload_group_account()

    def action_reload_group_account(self):
        for record in self.sudo():
            record._reload_group_account()

    def _reload_group_account(self):
        self.ensure_one()
        groups = self.detail_ids.mapped("account_id.type_id.group_id")
        Group = self.env["general_audit.group_detail"]
        self.group_detail_ids.unlink()
        for group in groups:
            Group.create(
                {
                    "general_audit_id": self.id,
                    "group_id": group.id,
                }
            )

    def action_reload_computation(self):
        for record in self.sudo():
            record._reload_computation()

    @ssi_decorator.post_open_action()
    def _reload_computation(self):
        self.ensure_one()
        Computation = self.env["general_audit.computation"]
        self.computation_ids.unlink()
        if self.account_type_set_id:
            for detail in self.account_type_set_id.computation_ids:
                data = {
                    "general_audit_id": self.id,
                    "computation_item_id": detail.computation_id.id,
                    "sequence": detail.sequence,
                }
                Computation.create(data)

    def action_recompute_computation(self):
        for record in self.sudo():
            record._recompute_computation()

    def _recompute_computation(self):
        self.ensure_one()
        for computation in self.computation_ids:
            computation._compute_computation()

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
