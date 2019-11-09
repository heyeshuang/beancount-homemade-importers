<http://blog.heysh.xyz/2019/11/07/netease-youqian-with-beancount/>

## Auto initialize some income/expense accounts for Beancount

```bash
python importers/youqian/accountInit.py > New_Accounts.bean
# If
python importers/youqian/accountInit.py Existing_Accounts.bean > New_Accounts.bean
```

## Import Netease Youqian（网易有钱）

```
bean-extract importers/youqian/youqian_expense.import documents.tmp/expense.csv > expense.bean
bean-extract importers/youqian/youqian_income.import documents.tmp/income.csv > income.bean
```

## Other importers

```
# 微信
bean-extract importers/wechat.import documents.tmp/test.csv > test.bean 
# 中国银行
bean-extract importers/boc.import documents.tmp/test.csv > test.bean
# 招商银行
bean-extract importers/cmb.import documents.tmp/test.csv > test.bean
```