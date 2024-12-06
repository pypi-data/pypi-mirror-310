# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class GeneralAuditStandardDetail(models.Model):
    _name = "general_audit.standard_detail"
    _description = "Accountant General Audit Standard Detail"
    _order = "sequence, general_audit_id, id"
    _rec_name = "type_id"

    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
        required=True,
        ondelete="cascade",
    )

    @api.depends(
        "general_audit_id",
        "general_audit_id.home_trial_balance_id",
        "general_audit_id.interim_trial_balance_id",
        "general_audit_id.previous_trial_balance_id",
        "general_audit_id.home_trial_balance_id.state",
        "general_audit_id.interim_trial_balance_id.state",
        "general_audit_id.previous_trial_balance_id.state",
    )
    def _compute_standard_line(self):
        StandardDetail = self.env["client_trial_balance.standard_detail"]
        for record in self:
            home_result = interim_result = previous_result = False
            criteria = [
                ("type_id", "=", record.type_id.id),
            ]
            if record.general_audit_id.home_trial_balance_id:
                criteria_home = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.home_trial_balance_id.id,
                    )
                ]
                home_results = StandardDetail.search(criteria_home)
                if len(home_results) > 0:
                    home_result = home_results[0]

            if record.general_audit_id.interim_trial_balance_id:
                criteria_interim = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.interim_trial_balance_id.id,
                    )
                ]
                interim_results = StandardDetail.search(criteria_interim)
                if len(interim_results) > 0:
                    interim_result = interim_results[0]

            if record.general_audit_id.previous_trial_balance_id:
                criteria_previous = criteria + [
                    (
                        "trial_balance_id",
                        "=",
                        record.general_audit_id.previous_trial_balance_id.id,
                    )
                ]
                previous_results = StandardDetail.search(criteria_previous)
                if len(previous_results) > 0:
                    previous_result = previous_results[0]

            record.home_standard_line_id = home_result
            record.interim_standard_line_id = interim_result
            record.previous_standard_line_id = previous_result

    @api.depends(
        "general_audit_id.adjustment_entry_ids",
        "general_audit_id.adjustment_entry_ids.state",
        "general_audit_id.adjustment_entry_ids.detail_ids.account_id",
        "general_audit_id.adjustment_entry_ids.detail_ids.debit",
        "general_audit_id.adjustment_entry_ids.detail_ids.credit",
    )
    def _compute_standard_adjustment_id(self):
        StandardAdjustment = self.env["general_audit.adjustment"]
        for record in self:
            result = False
            criteria = [
                ("general_audit_id", "=", record.general_audit_id.id),
                ("type_id", "=", record.type_id.id),
            ]
            standard_adjustments = StandardAdjustment.search(criteria)
            if len(standard_adjustments) > 0:
                result = standard_adjustments[0]
            record.standard_adjustment_id = result

    standard_adjustment_id = fields.Many2one(
        string="Standard Adjustment",
        comodel_name="general_audit.adjustment",
        readonly=True,
        compute="_compute_standard_adjustment_id",
        store=True,
    )

    home_standard_line_id = fields.Many2one(
        string="Home Statement TB Standard Line",
        comodel_name="client_trial_balance.standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        store=True,
    )
    interim_standard_line_id = fields.Many2one(
        string="Interim TB Standard Line",
        comodel_name="client_trial_balance.standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        store=True,
    )
    previous_standard_line_id = fields.Many2one(
        string="Previous TB Standard Line",
        comodel_name="client_trial_balance.standard_detail",
        readonly=True,
        compute="_compute_standard_line",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        store=True,
    )
    home_statement_opening_balance = fields.Monetary(
        string="Home Statement Opening Balance",
        related="home_standard_line_id.opening_balance",
        store=True,
        currency_field="currency_id",
    )
    home_statement_balance = fields.Monetary(
        string="Home Statement Balance",
        related="home_standard_line_id.balance",
        store=True,
        currency_field="currency_id",
    )
    interim_opening_balance = fields.Monetary(
        string="Interim Opening Balance",
        related="interim_standard_line_id.opening_balance",
        store=True,
        currency_field="currency_id",
    )
    interim_balance = fields.Monetary(
        string="Interim Balance",
        related="interim_standard_line_id.balance",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "interim_balance",
        "previous_balance",
        "type_id",
    )
    def _compute_extrapolation_balance(self):
        for record in self:
            balance = 0.0
            if record.type_id:
                python_code = record.type_id.python_code
                localdict = record._get_localdict()
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    balance = localdict["result"]
                except Exception:
                    balance = 7.0
            record.extrapolation_balance = balance

    extrapolation_balance = fields.Monetary(
        string="Extrapolation Balance",
        related=False,
        compute="_compute_extrapolation_balance",
        store=True,
        currency_field="currency_id",
    )

    extrapolation_adjustment = fields.Monetary(
        string="Extrapolation Adjustment",
        currency_field="currency_id",
    )

    @api.depends(
        "extrapolation_balance",
        "extrapolation_adjustment",
    )
    def _compute_adjusted_extrapolation_balance(self):
        for record in self:
            result = record.extrapolation_balance + record.extrapolation_adjustment
            record.adjusted_extrapolation_balance = result

    adjusted_extrapolation_balance = fields.Monetary(
        string="Adjusted Extrapolation Balance",
        currency_field="currency_id",
        store=True,
        compute="_compute_adjusted_extrapolation_balance",
    )

    previous_opening_balance = fields.Monetary(
        string="Previous Opening Balance",
        related="previous_standard_line_id.opening_balance",
        store=True,
        currency_field="currency_id",
    )
    previous_balance = fields.Monetary(
        string="Previous Balance",
        related="previous_standard_line_id.balance",
        store=True,
        currency_field="currency_id",
    )

    adjustment_debit = fields.Monetary(
        string="Adjustment Debit",
        related="standard_adjustment_id.debit",
        store=True,
        currency_field="currency_id",
    )
    adjustment_credit = fields.Monetary(
        string="Adjustment Credit",
        related="standard_adjustment_id.credit",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "type_id",
        "adjustment_debit",
        "adjustment_credit",
        "home_statement_balance",
    )
    def _compute_adjustment_audited_balance(self):
        for record in self:
            adjustment = audited = 0.0
            if record.type_id:
                if record.type_id.normal_balance == "dr":
                    adjustment = record.adjustment_debit - record.adjustment_credit
                else:
                    adjustment = record.adjustment_credit - record.adjustment_debit
            audited = record.home_statement_balance + adjustment
            record.audited_balance = audited
            record.adjustment_balance = adjustment

    adjustment_balance = fields.Monetary(
        string="Adjustment Balance",
        compute="_compute_adjustment_audited_balance",
        store=True,
        currency_field="currency_id",
    )
    audited_balance = fields.Monetary(
        string="Audited Balance",
        compute="_compute_adjustment_audited_balance",
        store=True,
        currency_field="currency_id",
    )

    @api.depends(
        "interim_balance",
        "extrapolation_balance",
        "previous_balance",
        "home_statement_balance",
        "audited_balance",
    )
    def _compute_average(self):
        for record in self:
            interim_avg = (record.interim_balance + record.previous_balance) / 2.0
            extrapolation_avg = (
                record.adjusted_extrapolation_balance + record.previous_balance
            ) / 2.0
            home_statement_avg = (
                record.home_statement_balance + record.previous_balance
            ) / 2.0
            audited_avg = (record.audited_balance + record.previous_balance) / 2.0

            record.interim_avg = interim_avg
            record.extrapolation_avg = extrapolation_avg
            record.home_statement_avg = home_statement_avg
            record.audited_avg = audited_avg

    interim_avg = fields.Monetary(
        string="Interim Average",
        compute="_compute_average",
        store=True,
        currency_field="currency_id",
    )
    extrapolation_avg = fields.Monetary(
        string="Extrapolation Average",
        compute="_compute_average",
        store=True,
        currency_field="currency_id",
    )
    home_statement_avg = fields.Monetary(
        string="Home Statement Average",
        compute="_compute_average",
        store=True,
        currency_field="currency_id",
    )
    audited_avg = fields.Monetary(
        string="Audited Average",
        compute="_compute_average",
        store=True,
        currency_field="currency_id",
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
            "standard_detail": self,
            "ga": self.general_audit_id,
        }
