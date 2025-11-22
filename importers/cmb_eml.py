"""Importer for 招商银行信用卡电子邮件账单 (China Merchants Bank)
"""

__copyright__ = "Copyright (C) 2019-2026  He Yeshuang"
__license__ = "GNU GPLv2"

# import base64
import datetime
import re
from email import parser, policy
from os import path
from datetime import datetime

from beancount.core import data, flags
from beancount.core.amount import Amount
from beancount.core.number import D
# from beancount.ingest import importer
import beangulp
from bs4 import BeautifulSoup
from dateutil.parser import parse as dateparse

#############################################################
# TODO: 修改此处账户名称                                     #
#############################################################

account = "Liabilities:CreditCards:CMB:Card"

#############################################################

isSmart = True
try:
    from smart_importer import PredictPostings
    import jieba
    jieba.initialize()
    def tokenizer(s): return list(jieba.cut(s))
except ImportError:
    isSmart = False



class CmbEmlImporter(beangulp.Importer):
    """An importer for CMB .eml files."""

    def __init__(self, account_name='Liabilities:CreditCards:CMB:Card'):
        # print(file_type)
        self.account_name: str = account_name
        self.currency = "CNY"
        pass

    def identify(self, filepath):
        # Match if the filename is as downloaded and the header has the unique
        # fields combination we're looking for.
        return (
            re.match(r"招商银行信用卡电子账单", path.basename(filepath)) and
            re.search(r"eml", path.basename(filepath))
        )

    def filename(self, filepath):
        return 'cmb.{}'.format(path.basename(filepath))

    def account(self, _):
        return self.account_name

    def extract(self, filepath, existing_entries=None):
        # Open the CSV file and create directives.
        entries = []
        index = 0
        with open(filepath, 'rb') as f:
            eml = parser.BytesParser(policy=policy.default).parse(fp=f)
            # b = base64.b64decode(eml.get_payload()[0].get_payload())
            b = eml.get_payload()[0].get_payload(decode=True).decode("UTF8")
            d = BeautifulSoup(b, "lxml")
            date_range = d.find_all(string=re.compile(
                r'\d{4}\/\d{1,2}\/\d{1,2}-\d{4}\/\d{1,2}\/\d{1,2}'))[0]
            transaction_date = dateparse(
                date_range.split('-')[1].split('(')[0]).date()
            balance = '-' + d.find(src="https://s3gw.cmbimg.com/ll65st0201-emaildmz-prd-1255000089/bill_templet_resource/"  # 不知道其他人是不是的hash是不是和我一样
                                   "email_normal_gold_e_bank_20230112_fb52414c35bf4cf085fec05e40360621")\
                .parent.parent.find_next_sibling(
                    'td').select('font')[0].text.replace('￥', '').replace('¥', '').replace(',', '').strip()
            txn_balance = data.Balance(
                account=self.account_name,
                amount=Amount(D(balance), 'CNY'),
                meta=data.new_metadata(".", 1000),
                tolerance=None,
                diff_amount=None,
                date=transaction_date
            )
            entries.append(txn_balance)

            # 现在不知道是什么jbmn,算了算了
            bands = d.select('#fixBand29 #loopBand2>table>tbody>tr')
            for band in bands:
                tds = band.select('td #fixBand15 table table td')
                if len(tds) == 0:
                    continue
                trade_date = tds[1].text.strip()
                if trade_date == '':
                    trade_date = tds[2].text.strip()
                # date = datetime.strptime(trade_date,'%m%d').replace(year=transaction_date.year).date()
                # print(trade_date)
                date = datetime.strptime(
                    str(transaction_date.year) + trade_date, "%Y%m%d"
                )
                if date.day < 15 and date.month != transaction_date.month:
                    date = date.replace(day=15) #防止之前的balance出现错误
                if date.month == 12 and transaction_date.month == 1:
                    date = date.replace(year=transaction_date.year-1).date()
                else:
                    date = date.replace(year=transaction_date.year).date()
                full_descriptions = tds[3].text.strip().split('-')
                payee = full_descriptions[0]
                narration = '-'.join(full_descriptions[1:])
                real_currency = 'CNY'
                real_price = tds[4].text.replace(
                    '￥', '').replace('\xa0', '').replace('¥', '').strip()
                # print("Importing {} at {}".format(narration, date))
                flag = "*"
                amount = -Amount(D(real_price), real_currency)
                meta = data.new_metadata(filepath, index)
                txn = data.Transaction(
                    meta, date, flags.FLAG_OKAY, payee, narration, data.EMPTY_SET, data.EMPTY_SET, [
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

IMPORTERS = [
        CmbEmlImporter(account)
]
HOOKS = []
if isSmart:
            HOOKS= [PredictPostings(string_tokenizer=tokenizer).hook]

if __name__ == "__main__":
    ingest = beangulp.Ingest(IMPORTERS, HOOKS)
    ingest()