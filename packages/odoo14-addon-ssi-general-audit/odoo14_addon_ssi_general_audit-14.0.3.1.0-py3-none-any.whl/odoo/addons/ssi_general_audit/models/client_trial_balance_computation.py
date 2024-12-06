# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as eval  # pylint: disable=redefined-builtin


class ClientTrialBalanceComputation(models.Model):
    _name = "client_trial_balance.computation"
    _description = "Accountant Client Trial Balance Computation"

    @api.depends(
        "trial_balance_id",
        "computation_item_id",
        "trial_balance_id.standard_detail_ids",
        "trial_balance_id.standard_detail_ids.balance",
    )
    def _compute_amount(self):
        obj_computation = self.env["client_account_type.computation_item"]
        for document in self:
            amount = 0.0
            criteria = [
                ("computation_id", "=", document.computation_item_id.id),
                (
                    "account_type_set_id",
                    "=",
                    document.trial_balance_id.account_type_set_id.id,
                ),
            ]
            computations = obj_computation.search(criteria)
            if len(computations) > 0:
                computation = computations[0]
                if computation.use_default:
                    python_code = computation.computation_item_id.python_code
                else:
                    python_code = computations[0].python_code

                localdict = document._get_localdict()
                try:
                    eval(
                        python_code,
                        localdict,
                        mode="exec",
                        nocopy=True,
                    )
                    amount = localdict["result"]
                except Exception:
                    amount = 0.0
            document.amount = amount

    trial_balance_id = fields.Many2one(
        string="Trial Balance",
        comodel_name="client_trial_balance",
        required=True,
        ondelete="cascade",
    )
    computation_item_id = fields.Many2one(
        string="Computation Item",
        comodel_name="trial_balance_computation_item",
        required=True,
    )
    amount = fields.Float(string="Amount", compute=False, default=0.0)

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _recompute(self, additional_dict):
        self.ensure_one()
        obj_computation = self.env["client_account_type.computation_item"]
        amount = 0.0
        criteria = [
            ("computation_id", "=", self.computation_item_id.id),
            (
                "account_type_set_id",
                "=",
                self.trial_balance_id.account_type_set_id.id,
            ),
        ]
        computations = obj_computation.search(criteria)
        if len(computations) > 0:
            computation = computations[0]
            if computation.use_default:
                python_code = computation.computation_id.python_code
            else:
                python_code = computations[0].python_code

            localdict = self._get_localdict()
            localdict.update(additional_dict)
            try:
                eval(
                    python_code,
                    localdict,
                    mode="exec",
                    nocopy=True,
                )
                amount = localdict["result"]
                additional_dict.update({self.computation_item_id.code: amount})
            except Exception:
                amount = 0.0
        self.write(
            {
                "amount": amount,
            }
        )
        return additional_dict
