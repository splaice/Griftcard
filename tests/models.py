import testify
import simplejson as json
import codecs
from griftcard.models import Griftcard

EXAMPLE_TRANSACTION_HISTORY_JSON = 'tests/example_transaction_history.json'
EXAMPLE_DETAIL_DATA_HTML = 'tests/example_detail_data.html'

class GriftcardTestCase(testify.TestCase):
    @testify.setup
    def setup(self):
        """ You will want to swap these with you valid gift card giftcard
            credentials.
        """
        self.card_number = '4111111111111111'
        self.phone_number = '4155551111'
        self.security_code = '111'

    @testify.teardown
    def teardown(self):
        self.card_number = None
        self.phone_number = None
        self.security_code = None

    def test_transaction_parser(self):
        with open(EXAMPLE_TRANSACTION_HISTORY_JSON) as fn:
            transactions = Griftcard.sanitize_transactions(fn.read())

        testify.assert_equal(transactions[0]['merchant_number'],
            '06078000001FTN1')
        testify.assert_equal(transactions[1]['merchant_number'],
            '4445100033589')
        testify.assert_equal(transactions[2]['merchant_number'],
            '008788430020795')
        testify.assert_equal(transactions[3]['merchant_number'],
            '008788430020795')
        testify.assert_equal(transactions[4]['merchant_number'],
            '4445000951186')
        testify.assert_equal(transactions[5]['merchant_number'],
            '60300000022')

    def test_details_parser(self):
        with codecs.open(EXAMPLE_DETAIL_DATA_HTML, 'r', 'utf-8') as fn:
            html = Griftcard.sanitize_details(fn.read())

        testify.assert_equal(html['card_status'], 'OPEN')
        testify.assert_equal(html['card_balance'], 7.37)

    def test_griftcard(self):
        griftcard = Griftcard(card_number=self.card_number,
                phone_number=self.phone_number,
                security_code=self.security_code)

        testify.assert_equal(griftcard.phone_number, self.phone_number)
        testify.assert_equal(griftcard.card_number, self.card_number)
        testify.assert_equal(griftcard.security_code, self.security_code)
        testify.assert_equal(griftcard.phone_number_last_four,
                self.phone_number[-4:])

        # TODO: replace lame test
        testify.assert_not_equal(griftcard.transactions, None)
        testify.assert_equal(griftcard.balance, 7.37)
