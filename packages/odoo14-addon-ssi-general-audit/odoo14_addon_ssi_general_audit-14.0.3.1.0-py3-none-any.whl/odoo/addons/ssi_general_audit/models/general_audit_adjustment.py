# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).


from odoo import fields, models, tools


class GeneralAuditAdjustment(models.Model):
    _name = "general_audit.adjustment"
    _description = "Accountant General Audit Standard Adjustment"
    _auto = False

    type_id = fields.Many2one(
        string="Account Type",
        comodel_name="client_account_type",
    )
    general_audit_id = fields.Many2one(
        string="# General Audit",
        comodel_name="general_audit",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="general_audit_id.currency_id",
        store=False,
    )
    debit = fields.Monetary(
        string="Debit",
        currency_id="currency_id",
    )
    credit = fields.Monetary(
        string="Credit",
        currency_id="currency_id",
    )

    def _select(self):
        select_str = """
        SELECT
            row_number() OVER() as id,
            b.general_audit_id AS general_audit_id,
            c.type_id AS type_id,
            SUM(a.debit) AS debit,
            SUM(a.credit) AS credit
        """
        return select_str

    def _from(self):
        from_str = """
        client_adjustment_entry_detail AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN client_adjustment_entry AS b ON a.entry_id = b.id
        JOIN client_account AS c ON a.account_id = c.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        GROUP BY    b.general_audit_id,
                    c.type_id
        """
        return group_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        self._cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._group_by(),
            )
        )
