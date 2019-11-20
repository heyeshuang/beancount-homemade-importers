"""Importer for 
"""
__copyright__ = "Copyright (C) 2019  He Yeshuang"
__license__ = "GNU GPLv2"

import base64
import csv
import datetime
import logging
import re
import sys
from email import parser
from enum import Enum
from os import path
from typing import Dict
from datetime import datetime

from beancount.core import account, data, position
from beancount.core.amount import Amount
from beancount.core.number import ZERO, D
from beancount.ingest import importer
from bs4 import BeautifulSoup
from dateutil.parser import parse as dateparse
# from smart_importer import PredictPayees, PredictPostings


class CmbEmlImporter(importer.ImporterProtocol):
    """An importer for CMB .eml files."""

    def __init__(self, account='Liabilities:CreditCards:CMB:Card'):
        # print(file_type)
        self.account_name:str = account
        self.currency = "CNY"
        pass

    def identify(self, file):
        # Match if the filename is as downloaded and the header has the unique
        # fields combination we're looking for.
        return (
            re.match(r"招商银行信用卡电子账单", path.basename(file.name)) and
            re.search(r"eml", path.basename(file.name))
        )

    def file_name(self, file):
        return 'cmb.{}'.format(path.basename(file.name))

    def file_account(self, _):
        return self.account_name

    def extract(self, file, existing_entries=None):
        # Open the CSV file and create directives.
        entries = []
        index = 0
        with open(file.name,'rb') as f:
            eml = parser.BytesParser().parse(fp=f)
            b=base64.b64decode(eml.get_payload()[0].get_payload())
            d = BeautifulSoup(b,"lxml")
            date_range = d.select('#fixBand38 div font')[0].text.strip()
            transaction_date = dateparse(date_range.split('-')[1].split('(')[0]).date()
            balance = '-' + d.select('#fixBand40 div font')[0].text.replace('￥', '').replace(',', '').strip()
            txn_balance=data.Balance(
                account=self.account_name,
                amount=Amount(D(balance), 'CNY'),
                meta=data.new_metadata(".", 1000),
                tolerance= None,
                diff_amount=None,
                date=transaction_date
            )
            entries.append(txn_balance)
            
            bands = d.select('#fixBand29 #loopBand2>table>tr')
            for band in bands:
                tds = band.select('td #fixBand15 table table td')
                if len(tds) == 0:
                    continue
                trade_date = tds[1].text.strip()
                if trade_date == '':
                    trade_date = tds[2].text.strip()
                date = datetime.strptime(trade_date,'%m%d').replace(year=transaction_date.year).date()
                full_descriptions = tds[3].text.strip().split('-')
                payee = full_descriptions[0]
                narration = '-'.join(full_descriptions[1:])
                real_currency = 'CNY'
                real_price = tds[4].text.replace('￥', '').replace('\xa0', '').strip()
                # print("Importing {} at {}".format(narration, date))
                flag = "*"
                amount =-Amount( D(real_price),real_currency)
                meta = data.new_metadata(file.name, index)
                txn = data.Transaction(
                    meta, date, self.FLAG, payee, narration, data.EMPTY_SET, data.EMPTY_SET, [
                        data.Posting(self.account_name, amount,
                                     None, None, None, None),
                    ])

                entries.append(txn)

        # Insert a final balance check.

        return entries


# @PredictPostings()
# @PredictPayees()
# class SmartWechatImporter(WechatImporter):
#     pass
