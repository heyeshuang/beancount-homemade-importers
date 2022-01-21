
"""Importer for 招商银行 (China Merchants Bank)
"""
__copyright__ = "Copyright (C) 2019-2021  He Yeshuang"
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
import json

from beancount.core import account, data, position
from beancount.core.amount import Amount
from beancount.core.number import ZERO, D
from beancount.ingest import importer
from dateutil.parser import parse as dateparse


class CmbJSONImporter(importer.ImporterProtocol):
    """An importer for XHR response from [CMB credit card](https://xyk.cmbchina.com/credit-express/bill)"""

    def __init__(self, account=account, currency='CNY'):
        # print(file_type)
        self.account_name: str = account
        self.currency = currency
        pass

    def _finditem(self, obj, key):
        if key in obj:
            return obj[key]
        for k, v in obj.items():
            if isinstance(v, dict):
                return self._finditem(v, key)

    def identify(self, file):
        # Match if the filename is as downloaded and the header has the unique
        # fields combination we're looking for.
        return (
            re.search(r"json", path.basename(file.name))
        )

    def file_name(self, file):
        return 'cmb.{}'.format(path.basename(file.name))

    def file_account(self, _):
        return self.account_name

    def file_date(self, file):
        with open(file.name, 'r') as f:
            raw_data = json.load(f)
            rmbBillInfo = self._finditem(raw_data, "rmbBillInfo")
            return dateparse(rmbBillInfo["billCycleEnd"]).date()

    def extract(self, file, existing_entries=None):
        entries = []
        index = 0
        with open(file.name, 'r') as f:
            raw_data = json.load(f)
            detail = self._finditem(raw_data, "detail")
            rmbBillInfo = self._finditem(raw_data, "rmbBillInfo")

        for d in detail:
            payee, narration = None, None
            if "-" in d["description"]:
                [payee, narration] = d["description"].split("-", maxsplit=1)
            else:
                narration = d["description"]

            txn = data.Transaction(
                meta=data.new_metadata(file.name, lineno=index),
                date=dateparse(d['billDate']).date(),
                flag=self.FLAG,
                payee=payee,
                narration=narration,
                tags=data.EMPTY_SET,
                links=data.EMPTY_SET,
                postings=[
                    data.Posting(
                        self.account_name,
                        Amount(-D(d["amount"]), self.currency),
                        None, None, None, None
                    )
                ]
            )
            entries.append(txn)

        txn_balance = data.Balance(
            account=self.account_name,
            amount=Amount(-D(rmbBillInfo["amount"]), 'CNY'),
            meta=data.new_metadata(file.name, lineno=9999),
            tolerance=None,
            diff_amount=None,
            date=dateparse(rmbBillInfo["billCycleEnd"]).date()
        )
        entries.append(txn_balance)

        return entries

# @PredictPostings()
# @PredictPayees()
# class SmartWechatImporter(WechatImporter):
#     pass
