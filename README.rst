Griftcard: Python Package for Scraping Pre-Paid Giftcard Information
=========================

This package is meant to enable you to easily access the transaction history
and details of pre-paid credit card gift cards.


Features
--------

- Supports scraping giftcardmall.com pre-paid visa giftcards
- Simple Pythonic interface


Example
---

How to get the details for a giftcard: ::

    from griftcard import Griftcard
    grift = Griftcard(card_number='41111111111111',
        phone_number='555-555-1111', security_code='111')
    print grift.balance
    print grift.transactions


Contribute
----------

#. Fork the project on github to start making your changes
#. Send pull requests with your bug fixes or features
#. Submit and create issues on github
