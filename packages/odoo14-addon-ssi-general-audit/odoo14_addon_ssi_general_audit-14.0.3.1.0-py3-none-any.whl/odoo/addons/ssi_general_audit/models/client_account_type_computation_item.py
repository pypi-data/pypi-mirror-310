# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class ClientAccountTypeComputationItem(models.Model):
    _name = "client_account_type.computation_item"
    _description = "Client Account Type Computation Item"
    _order = "account_type_set_id, sequence, id"

    account_type_set_id = fields.Many2one(
        string="Account Type Set",
        comodel_name="client_account_type_set",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        related="computation_id.sequence",
        store=True,
    )
    computation_id = fields.Many2one(
        string="Computation",
        comodel_name="trial_balance_computation_item",
        required=True,
    )
    use_default = fields.Boolean(
        string="Use Default Computation",
        default=True,
    )
    python_code = fields.Text(
        string="Python Code",
        default="result = 0.0",
    )

    @api.onchange(
        "computation_id",
    )
    def onchange_python_code_code(self):
        self.python_code = "result = 0.0"
        if self.computation_id:
            computation = self.computation_id
            self.python_code = computation.python_code
