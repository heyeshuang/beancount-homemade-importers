"""Importer for 网易有钱
"""
__copyright__ = "Copyright (C) 2019  He Yeshuang"
__license__ = "GNU GPLv2"

import csv
from enum import Enum
import sys
import datetime
import re
import logging
from os import path

from dateutil.parser import parse

from beancount.core.number import D
from beancount.core.number import ZERO
from beancount.core import data
from beancount.core import account
from beancount.core.amount import Amount
from beancount.core import position
from beancount.ingest import importer

sys.path.append("./importers")
from youqian.youqianDict import CategoryAsset,CategoryExpense,CategoryIncome
# from .youqianDict import CategoryAsset,CategoryExpense,CategoryIncome

class fileType(Enum):
    EXPENSE=1
    INCOME=2
    TRANSPORT=3 #TODO

class YouqianImporter(importer.ImporterProtocol):
    """An importer for UTrade CSV files (an example investment bank)."""

    def __init__(self,file_type:fileType=fileType.EXPENSE,currency="CNY"):
        self.file_type=file_type
        self.currency=currency
        # print(file_type)

    def identify(self, file):
        # Match if the filename is as downloaded and the header has the unique
        # fields combination we're looking for.
        if re.match("时间,账本,账户,大类,小类,金额,币种,备注,来源", file.head()):
            assert self.file_type==fileType.EXPENSE or fileType.INCOME
            return True
        elif re.match(
            "时间,账本,转出账户,大类,小类,转出金额,转出币种,转入账户,转入币种,转入金额,备注,来源",
            file.head()):
            assert self.file_type==fileType.TRANSPORT
            return True
        return False

    def extract(self, file):
        # Open the CSV file and create directives.
        entries = []
        index = 0
        for index, row in enumerate(csv.DictReader(open(file.name))):
            meta = data.new_metadata(file.name, index)
            date = parse(row['时间']).date()
            raw_amount = D(row['金额'])
            if self.file_type==fileType.EXPENSE:
                raw_amount=-raw_amount
            amount=Amount(raw_amount,self.currency)
            narration = row['备注']
            account_1_text = row['账户']
            account_2_text = (row['大类']+','+row['小类']).rstrip(",")
            account_1,account_2='Assets.FIXME','WHATEVER.FIXME'
            # print(raw_amount,narration,account_1_text,account_2_text)
            for asset_k,asset_v in CategoryAsset.items():
                if account_1_text.find(asset_k)!=-1:
                    # print(asset_k, asset_v)
                    account_1=asset_v
            
            for k,v in {**CategoryExpense,**CategoryIncome}.items():
                if account_2_text.find(k)!=-1:
                    account_2=v

            txn = data.Transaction(
                meta, date, self.FLAG, None, narration, data.EMPTY_SET, data.EMPTY_SET, [
                    data.Posting(account_1, amount,
                                 None, None, None, None),
                    data.Posting(account_2, -amount, None, None, None, None),
                ])


            entries.append(txn)

        # Insert a final balance check.

        return entries

CONFIG=[YouqianImporter(file_type=fileType.INCOME)]
