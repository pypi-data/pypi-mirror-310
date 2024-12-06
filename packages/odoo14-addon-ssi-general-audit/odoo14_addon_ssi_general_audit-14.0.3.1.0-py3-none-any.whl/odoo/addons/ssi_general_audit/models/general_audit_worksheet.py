# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class GeneralAuditWorksheet(models.Model):
    _name = "general_audit_worksheet"
    _description = "General Audit Worksheet"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
    ]
    _order = "general_audit_id, parent_type_id, id"

    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = "open"

    @api.model
    def _get_policy_field(self):
        res = super(GeneralAuditWorksheet, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _compute_policy(self):
        _super = super(GeneralAuditWorksheet, self)
        _super._compute_policy()

    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        readonly=True,
        required=True,
        ondelete="cascade",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    # Fields related from general audit
    date_start = fields.Date(
        string="Start Date",
        related="general_audit_id.date_start",
        readonly=True,
        store=True,
    )
    date_end = fields.Date(
        string="End Date",
        related="general_audit_id.date_end",
        readonly=True,
        store=True,
    )
    interim_date_start = fields.Date(
        string="Interim Start Date",
        related="general_audit_id.interim_date_start",
        readonly=True,
        store=True,
    )
    interim_date_end = fields.Date(
        string="Interim End Date",
        related="general_audit_id.interim_date_end",
        readonly=True,
        store=True,
    )
    previous_date_start = fields.Date(
        string="Previous Start Date",
        related="general_audit_id.previous_date_start",
        readonly=True,
        store=True,
    )
    previous_date_end = fields.Date(
        string="Previous End Date",
        related="general_audit_id.previous_date_end",
        readonly=True,
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        readonly=True,
        store=True,
    )
    account_type_set_id = fields.Many2one(
        string="Accoount Type Set",
        comodel_name="client_account_type_set",
        related="general_audit_id.account_type_set_id",
        readonly=True,
        store=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        related="general_audit_id.partner_id",
        store=True,
    )
    accountant_id = fields.Many2one(
        string="Accountant",
        related="general_audit_id.accountant_id",
        store=True,
    )
    title = fields.Char(
        string="Title",
        related="general_audit_id.title",
        store=True,
    )
    parent_type_id = fields.Many2one(
        string="Parent Type",
        comodel_name="general_audit_worksheet_type",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    reviewer_id = fields.Many2one(
        string="Reviewer",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="general_audit_worksheet_conclusion",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    conclusion = fields.Text(
        string="Conclusion Additional Explanation",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.constrains(
        "state",
    )
    def _constrains_state_change_confirm(self):
        for record in self.sudo():
            if record.state == "confirm":
                if not record._check_conclusion():
                    error_message = _(
                        """
                    Context: Confirm worksheet
                    Database ID: %s
                    Problem: Conclusion is not set
                    Solution: Choose conclusion
                    """
                        % (self.id)
                    )
                    raise ValidationError(error_message)

                if not record._check_conclusion_explanation():
                    error_message = _(
                        """
                    Context: Confirm worksheet
                    Database ID: %s
                    Problem: Conclusion explanation is not set
                    Solution: Fill conclusion explanation
                    """
                        % (self.id)
                    )
                    raise ValidationError(error_message)

    def _check_conclusion(self):
        self.ensure_one()
        result = True
        if not self.conclusion_id:
            result = False

        return result

    def _check_conclusion_explanation(self):
        self.ensure_one()
        result = True
        if not self.conclusion:
            result = False

        return result
