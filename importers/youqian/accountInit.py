#!/usr/bin/env python3
from datetime import date
import sys
from beancount import loader
from beancount.core import compare,data
from beancount.parser import printer
from youqianDict import CategoryAll

entries_existing=[]
if len(sys.argv) > 1:
    filename = sys.argv[1]
    entries_existing, errors, options = loader.load_file(filename)

entries_new=[]
accounts_existing=[i.account for i in entries_existing]
for account_youqian in sorted(set(CategoryAll.values())):
    if account_youqian not in accounts_existing:
        entries_new.append(
            data.Open(
                meta=None,
                booking=None,
                date=date(1970, 1, 1),
                account=account_youqian,
                currencies=["CNY"]
            )
        )

for entry in entries_new:
    printer.print_entry(entry)
