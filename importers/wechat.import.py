#!/usr/bin/env python

import os
import sys

import beancount.ingest.extract
from beancount.ingest.importers import csv

beancount.ingest.extract.HEADER = ''

# 问题：
# 1. 不支持区分来自银行卡还是微信钱包
# 2. 不能区分支出还是收入
# 3. 自动分类
CONFIG = [
    csv.Importer(
        {
            csv.Col.DATE: '交易时间',
            csv.Col.PAYEE: '交易对方',
            csv.Col.NARRATION1: '交易类型',
            csv.Col.NARRATION2: '商品',
            csv.Col.AMOUNT_DEBIT: '金额(元)',
            
        },
        account='Assets:WeChat:Wallet',
        currency='CNY',
        skip_lines=16,
        regexps='微信支付账单明细',
        # debug=True
    )
]
