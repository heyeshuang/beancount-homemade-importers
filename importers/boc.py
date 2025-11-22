#!/usr/bin/env python


import beangulp.extract
from beangulp.importers import csv
from smart_importer import PredictPostings
import jieba

jieba.initialize()
def tokenizer(s): return list(jieba.cut(s))


#############################################################
# TODO: 修改account账户名称                                  #
#############################################################
IMPORTERS = [
    # BOC Credit
    csv.CSVImporter(
        {
            csv.Col.DATE: '交易日期',
            csv.Col.NARRATION1: '对方账户名称',
            # csv.Col.NARRATION2: '附言',
            csv.Col.AMOUNT_DEBIT: '支出金额',
            csv.Col.AMOUNT_CREDIT: '收入金额',
            csv.Col.BALANCE: '余额'
        
        },
        account='Assets:Bank:BOC:Card', ######### 这里
        currency='CNY',
        regexps='网点名称',
        csv_dialect='excel-tab',
        encoding="UTF-16"
        # categorizer=guess.guess2]
    )
]

HOOKS= [PredictPostings(string_tokenizer=tokenizer).hook]

if __name__ == "__main__":
    ingest = beangulp.Ingest(IMPORTERS, HOOKS)
    ingest()