# -*- coding: UTF-8 -*-

"""Importer for 微信
"""
__copyright__ = "Copyright (C) 2019  He Yeshuang"
__license__ = "GNU GPLv2"

import csv
import datetime
import logging
import re
import sys
from enum import Enum
from os import path
from typing import Dict

from beancount.core import account, data, position
from beancount.core.amount import Amount
from beancount.core.number import ZERO, D
from beancount.ingest import importer
from dateutil.parser import parse
from smart_importer import PredictPostings, PredictPayees

class WechatImporter(importer.ImporterProtocol):
    """An importer for Wechat CSV files."""

    def __init__(self, accountDict: Dict):
        # print(file_type)
        self.accountDict = accountDict
        self.currency = "CNY"
        pass

    def identify(self, file):
        # Match if the filename is as downloaded and the header has the unique
        # fields combination we're looking for.
        return (re.search(r"微信支付账单", path.basename(file.name)))

    def file_name(self, file):
        return 'wechat.{}'.format(path.basename(file.name))

    def file_account(self, _):
        return "Assets:WeChat:Wallet"

    def file_date(self, file):
        # Extract the statement date from the filename.
        return datetime.datetime.strptime(path.basename(file.name).split("-")[-1],
                                          '%Y%m%d).csv').date()

    def extract(self, file, existing_entries=None):
        # Open the CSV file and create directives.
        entries = []
        index = 0
        with open(file.name, encoding="utf-8") as f:
            for _ in range(16):
                next(f)
            for index, row in enumerate(csv.DictReader(f)):
                if "转入零钱通" in row["交易类型"]:
                    continue  # skip the transfer to wechat

                meta = data.new_metadata(file.name, index)
                date = parse(row['交易时间']).date()
                raw_amount = D(row['金额(元)'].lstrip("¥"))
                isExpense = True if (row['收/支'] == '支出' or row['收/支'] == '/') else False
                if isExpense:
                    raw_amount = -raw_amount
                amount = Amount(raw_amount, self.currency)
                payee = row['交易对方']
                narration = row['商品']
                account_1_text = row['支付方式']
                account_1 = 'Assets.FIXME'
                # print(raw_amount,narration,account_1_text,account_2_text)
                for asset_k, asset_v in self.accountDict.items():
                    if account_1_text.find(asset_k) != -1:
                        # print(asset_k, asset_v)
                        account_1 = asset_v

                txn = data.Transaction(
                    meta, date, self.FLAG, payee, narration, data.EMPTY_SET, data.EMPTY_SET, [
                        data.Posting(account_1, amount,
                                     None, None, None, None),
                    ])

                entries.append(txn)

        # Insert a final balance check.

        return entries


# @PredictPostings()
# @PredictPayees()
# class SmartWechatImporter(WechatImporter):
#     pass
