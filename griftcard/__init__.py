# -*- coding: utf-8 -*-
"""
griftcard
~~~~~~~~

:copyright: (c) 2012 by Sean Plaice.
:license: ISC, see LICENSE for more details.

"""

__title__ = 'griftcard'
__version__ = '0.0.1'
__description__ = 'Python Package for Scraping Pre-Paid Giftcard Information'
__url__ = 'https://github.com/splaice/griftcard'
__build__ = 0
__author__ = 'Sean Plaice'
__license__ = 'ISC'
__copyright__ = 'Copyright 2012 Sean Plaice'


from . import utils
from .models import Griftcard
from .errors import GriftcardError
