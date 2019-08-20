# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

from eagle import models, api, _
from eagle.exceptions import UserError


class BankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.multi
    def button_draft(self):
        self.state = 'open'


