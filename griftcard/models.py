# -*- coding: utf-8 -*-
"""
This module contains the primary objects that power Griftcard.

:copyright: (c) 2012 by Sean Plaice.
:license: ISC, see LICENSE for more details.
"""

import requests
import simplejson as json
from datetime import datetime
from BeautifulSoup import BeautifulSoup

from .errors import GriftcardError


class Griftcard(object):
    """ The :class`Griftcard <Griftcard>` object.
        It carries out all the functionality of Griftcard.
    """

    def __init__(self, card_number=None, phone_number=None,
            security_code=None):
        self.card_number = card_number
        self.phone_number = phone_number
        self.phone_number_last_four = phone_number[-4:]
        self.security_code = security_code
        self.base_url = 'https://mygift.giftcardmall.com'
        self.auth_url = self.base_url + '/MyCard'
        self.history_url = self.base_url + '/TransActionHistory'
        self.history_ajax_url = self.history_url + '/_Index'
        self.last_auth = None
        self._details = None
        self._balance = None
        self._status = None
        self._transactions_raw = None
        self._transactions = []
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) ' \
                          'AppleWebKit/534.55.3 (KHTML, like Gecko) ' \
                          'Version/5.1.5 Safari/534.55.3'
        self.headers = {'User-Agent': self.user_agent}
        self.auth_data = {'CardNumber': self.card_number,
                'Last4OfPhone': self.phone_number_last_four,
                'SecurityCode': self.security_code}
        self.session = requests.session()

    @property
    def transactions(self):
        if not self.last_auth:
            self.refresh()

        delta = datetime.utcnow() - self.last_auth
        if delta.seconds > 5 * 60:
            self.refresh()

        return self._transactions

    @property
    def balance(self):
        if not self.last_auth:
            self.refresh()

        delta = datetime.utcnow() - self.last_auth
        if delta.seconds > 5 * 60:
            self.refresh()

        return self._balance

    @property
    def status(self):
        if not self.last_auth:
            self.refresh()

        delta = datetime.utcnow() - self.last_auth
        if delta.seconds > 5 * 60:
            self.refresh()

        return self._status

    def login(self):
        auth_data = {}
        r = self.session.post(self.auth_url, data=self.auth_data,
                headers=self.headers)
        if r.status_code != 200:
            raise GriftcardError('Could not authenticate session. %r' %
                    self.auth_data)

        self.last_auth = datetime.utcnow()

    def logout(self):
        self.last_auth = None

    def fetch_details(self):
        # hit the transaction history page
        r = self.session.get(self.history_url, headers=self.headers)
        if r.status_code != 200:
            raise GriftcardError('Could not authenticate session. %r' %
                    auth_data)

        self.raw_details = r.text
        self._details = self.sanitize_details(self.raw_details)
        self._balance = self._details['card_balance']
        self._status = self._details['card_status']

    def fetch_transactions(self):
        # this should actually validate the time of the last auth
        if not self.last_auth and not self.session:
            self._login()


        # hit the transaction history AJAX end-point while looking like a
        # XMLHttpRequest
        xmlhttprequest_headers = {'X-Requested-With': 'XMLHttpRequest',
                'Referer': self.history_url, 'Origin': self.base_url}
        headers = self.headers
        headers.update(xmlhttprequest_headers)
        r = self.session.post(self.history_ajax_url, headers=headers,
                data={'page': '1', 'size': '10', 'orderBy': '', 'groupBy': '',
                      'filter': ''})
        if r.status_code != 200:
            raise GriftcardError('Could not access transaction history' \
                    'ajax endpoint. %r' % auth_data)

        self.raw_transactions = r.text
        #self._transactions = self.sanitize_transactions(self.raw_transactions)

    def refresh(self):
        self.login()
        self.fetch_details()
        self.fetch_transactions()

    @classmethod
    def sanitize_transactions(cls, raw):
        transactions = json.loads(raw)
        new_transactions = []
        for trans in transactions['data']:
            new_transactions.append({
                'date': trans['Date'],
                'agent_id': trans['AgentId'],
                'merchant_number': trans['MerchantNumber'],
                'merchant_name': trans['MerchantName'],
                'merchant_city': trans['MerchantCity'],
                'merchant_zip': trans['MerchantZip'],
                'description': trans['Description'],
                'reference_number': trans['RetrievalReferenceNumber'],
                'balance': trans['Balance'],
                'authorization_amount': trans['AuthorizationAmount'],
                'value': trans['Value'],
                'amount': trans['Amount'],
                'settlement_amount': trans['SettlementAmount'],
                'security_code': trans['SecurityCode'],
                'status_reason': trans['StatusReason'],
                'adjustment_amount': trans['AdjustmentAmount'],
                'adjustment_reason': trans['AdjustmentReason'],
                'status': trans['Status'],
                'pos_date': trans['POSDate'],
                'type': trans['Type'],
                'tolerance_amount': trans['ToleranceAmount'],
                'details': trans['Details']})

        return new_transactions

    @classmethod
    def sanitize_details(cls, raw):
        soup = BeautifulSoup(raw)

        # get string values
        card_number = soup.find('div',
                id='/CardHeaderForm__namespaceId2/CardHeaderForm:itemId5'
                ).div.string
        card_status = soup.find('div',
                id='/CardHeaderForm__namespaceId2/CardHeaderForm:itemId6'
                ).div.string
        card_balance = soup.find('b', xmlns='http://www.w3.org/1999/xhtml').string

        # cleanup string values
        card_number = card_number.replace(' ', '')
        card_status = card_status.split(':')[1].replace(' ', '')
        card_balance = float(card_balance.split(':')[1].replace(' ', '').replace('$', ''))
        return {'card_number': card_number, 'card_status': card_status,
                'card_balance': card_balance}
