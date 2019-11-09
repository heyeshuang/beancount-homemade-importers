#!/usr/bin/env python

import os
import sys

import beancount.ingest.extract
from beancount.ingest.importers import csv

beancount.ingest.extract.HEADER = ''

CONFIG = [
    # CMB Credit
    csv.Importer(
        {
            csv.Col.DATE: '记账日期',
            csv.Col.TXN_DATE: '交易日期',
            csv.Col.NARRATION1: '交易摘要',
            csv.Col.AMOUNT_DEBIT: '人民币金额',
            csv.Col.LAST4: '卡号末四位'
        },
        account='Liabilities:CreditCards:CMB:Card',
        currency='CNY',
        last4_map={
            "0000": "招行 0000"
        }
    )
]
