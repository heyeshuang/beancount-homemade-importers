"""Importer for 招商银行借记卡 (China Merchants Bank)
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
from datetime import datetime, timedelta

from beancount.core import account, data, position
from beancount.core import amount
from beancount.core.amount import Amount
from beancount.core.number import ZERO, D
from beancount.ingest import importer
import pandas as pd
import camelot

# from smart_importer import PredictPayees, PredictPostings


class CmbPDFImporter(importer.ImporterProtocol):
    """An importer for CMBC PDF files."""

    def __init__(self, account=account):
        # print(file_type)
        self.account_name: str = account
        self.currency = "CNY"
        pass

    def identify(self, file):
        # Match if the filename is as downloaded and the header has the unique
        # fields combination we're looking for.
        return re.search(r"招商银行交易流水", path.basename(file.name))

    def file_name(self, file):
        return "cmbc.{}".format(path.basename(file.name))

    def file_account(self, _):
        return self.account_name

    def extract(self, file, existing_entries=None):
        # Open the CSV file and create directives.
        entries = []
        index = 0
        all_data = pd.DataFrame()
        tables_first = camelot.read_pdf(
            file.name,
            pages="1",
            flavor="stream",
            table_areas=["0,600,560,40"],
            row_tol=12,
        )
        for table in tables_first:
            df = table.df
            df.drop(index=1, inplace=True)
            all_data = pd.concat(
                [all_data, df.rename(columns=df.iloc[0]).drop([0])], ignore_index=True
            )

        # 处理其他页的表格
        tables_other_pages = camelot.read_pdf(
            file.name, pages="2-end", flavor="stream", row_tol=12
        )  # 其他页的表格解析

        # 将其他页的表格数据添加到 all_data
        for table in tables_other_pages:
            df = table.df
            df.drop(index=1, inplace=True)
            all_data = pd.concat(
                [all_data, df.rename(columns=df.iloc[0]).drop([0])], ignore_index=True
            )
        dfa = all_data
        dfa.replace(to_replace="\n", value="", regex=True, inplace=True)
        dfa["记账日期"] = pd.to_datetime(dfa["记账日期"], errors='coerce').dt.date
        dfa = dfa[~dfa["记账日期"].isna()]  #防止因为列太高产生空行
        # print(dfa)
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
                        None,
                        None,
                        None,
                        None,
                    )
                ],
            )
            for index, tdate, payee, narration, amount in zip(
                dfa.index,
                dfa["记账日期"],
                dfa["交易摘要"],
                dfa["对手信息"],
                dfa["交易金额"],
            )
        ]
        entries.append(
            data.Balance(
                account=self.account_name,
                amount=Amount(D(dfa.iloc[-1]["联机余额"]), self.currency),
                date=dfa.iloc[-1]["记账日期"] + timedelta(days=1),
                tolerance=None,
                diff_amount=None,
                meta=data.new_metadata(file.name, lineno=9999),
            )
        )
        return entries
