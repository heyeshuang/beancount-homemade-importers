"""Importer for 民生银行借记卡账单pdf
"""

__copyright__ = "Copyright (C) 2019-2024  He Yeshuang"
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
from datetime import datetime, timedelta

from beancount.core import account, data, position
from beancount.core import amount
from beancount.core.amount import Amount
from beancount.core.number import ZERO, D
from beancount.ingest import importer
import pandas as pd
import camelot
# from smart_importer import PredictPayees, PredictPostings


class CmbcPDFImporter(importer.ImporterProtocol):
    """An importer for CMBC PDF files."""

    def __init__(self, account=account):
        # print(file_type)
        self.account_name: str = account
        self.currency = "CNY"
        pass

    def identify(self, file):
        # Match if the filename is as downloaded and the header has the unique
        # fields combination we're looking for.
        return re.search(r"\d{19}\.pdf", path.basename(file.name))

    def file_name(self, file):
        return 'cmbc.{}'.format(path.basename(file.name))

    def file_account(self, _):
        return self.account_name

    def extract(self, file, existing_entries=None):
        # Open the CSV file and create directives.
        entries = []
        index = 0
        tables = camelot.read_pdf(
            file.name,
            flavor='stream', pages="1-end", table_areas=['15,500,825,35'],
            columns=["54,94,170,342,410,450,480,530,565,695"],
            split_text=True, row_tol=10, strip_text='\n'
        )
        dfa = pd.concat([t.df.rename(columns=t.df.iloc[0]).drop([0])
                         for t in tables], ignore_index=True)
        dfa["交易时间"] = pd.to_datetime(dfa["交易时间"]).dt.date
        entries = [
            data.Transaction(
                meta=data.new_metadata(file.name, lineno=index),
                date=tdate,
                flag=self.FLAG,
                payee=payee,
                narration=narration,
                tags=data.EMPTY_SET,
                links=data.EMPTY_SET,
                postings=[
                    data.Posting(
                        self.account_name,
                        Amount(D(amount), self.currency),
                        None, None, None, None
                    )
                ]
            )
            for index, tdate, payee, narration, amount in
            zip(dfa.index, dfa["交易时间"], dfa["对方户名/账号"], dfa["摘要"], dfa["交易金额"])
        ]
        entries.append(
            data.Balance(
                account=self.account_name,
                amount=Amount(
                    D(dfa.iloc[-1]["账户余额"]), self.currency),
                date=dfa.iloc[-1]["交易时间"] + timedelta(days=1),
                tolerance=None,
                diff_amount=None,
                meta=data.new_metadata(file.name, lineno=9999),
            ))
        return entries
