# -*- coding: utf-8 -*-
# Part of Eagle. See LICENSE file for full copyright and licensing details.

from eagle import api, fields, models
from eagle.exceptions import UserError
from eagle.addons.iap.models import iap

DEFAULT_ENDPOINT = 'https://iap-sms.eagle-erp.com'


class SmsApi(models.AbstractModel):
    _name = 'sms.api'
    _description = 'SMS API'

    @api.model
    def _send_sms(self, numbers, message):
        """ Send sms
        """
        account = self.env['iap.account'].get('sms')
        params = {
            'account_token': account.account_token,
            'numbers': numbers,
            'message': message,
        }
        endpoint = self.env['ir.config_parameter'].sudo().get_param('sms.endpoint', DEFAULT_ENDPOINT)
        r = iap.jsonrpc(endpoint + '/iap/message_send', params=params)
        return True
