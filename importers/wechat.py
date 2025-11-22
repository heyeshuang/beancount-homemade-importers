# -*- coding: UTF-8 -*-

"""Importer for 微信
"""
__copyright__ = "Copyright (C) 2026  He Yeshuang"
__license__ = "GNU GPLv2"

import csv
import datetime
import re
from enum import Enum
from os import path
from typing import Dict

from beancount.core import  data, flags
from beancount.core.amount import Amount
from beancount.core.number import D
import beangulp
from dateutil.parser import parse

#############################################################
# TODO: 修改此处账户名称                                     #
#############################################################
ignore = ["招商银行"]

accountDict = {
    "中国银行": "Assets:Bank:BOC:Card",
    "招商银行": "Liabilities:CreditCards:CMB:Card",
    "零钱": "Assets:WeChat:Wallet",
    "工商银行": "Assets:Bank:ICBC:Card",
    "/": "Assets:WeChat:Wallet"
}

#############################################################

isSmart = True
try:
    from smart_importer import PredictPostings
    import jieba
    jieba.initialize()
    tokenizer = lambda s: list(jieba.cut(s))

except ImportError:
    isSmart = False

class WechatImporter(beangulp.Importer):
    """An importer for Wechat CSV files."""

    def __init__(self, ignore: list, accountDict: Dict):
        # print(file_type)
        self.accountDict = accountDict
        self.ignore = ignore
        self.currency = "CNY"
        pass

    def account(self, filepath):
        return self.accountDict.get("/")

    def identify(self, filepath):
        # Match if the filename is as downloaded and the header has the unique
        # fields combination we're looking for.
        return (re.search(r"微信支付账单", path.basename(filepath)))

    def filename(self, filepath):
        return 'wechat.{}'.format(path.basename(filepath))

    def file_account(self, _):
        return "Assets:WeChat:Wallet"

    # def date(self, filepath):
    #     # Extract the statement date from the filename.
    #     return datetime.datetime.strptime(path.basename(filepath).split("-")[-1],
    #                                       '%Y%m%d).csv').date()

    def extract(self, filepath, existing_entries=None):
        # Open the CSV file and create directives.
        entries = []
        index = 0
        with open(filepath, encoding="utf-8") as f:
            for _ in range(16):
                next(f)
            for index, row in enumerate(csv.DictReader(f)):
                if "转入零钱通" in row["交易类型"]:
                    continue  # skip the transfer to wechat

                meta = data.new_metadata(filepath, index)
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
                    meta, date, flags.FLAG_OKAY, payee, narration, data.EMPTY_SET, data.EMPTY_SET, [
                        data.Posting(account_1, amount,
                                     None, None, None, None),
                    ])

                if not any(i in account_1_text for i in self.ignore):
                    entries.append(txn)

        # Insert a final balance check.

        return entries

IMPORTERS = [
        WechatImporter(accountDict=accountDict, ignore=ignore)
        # apply_hooks(WechatImporter(accountDict=accountDict), [PredictPostings()])
        # SmartWechatImporter(accountDict=accountDict)
]
HOOKS = []
if isSmart:
            HOOKS= [PredictPostings(string_tokenizer=tokenizer).hook]

if __name__ == "__main__":
    ingest = beangulp.Ingest(IMPORTERS, HOOKS)
    ingest()