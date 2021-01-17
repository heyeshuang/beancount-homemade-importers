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

[smart_importer](https://github.com/beancount/smart_importer) needs to be installed to import smartly.

```
pip install smart_importer
```

```
# 微信
bean-extract importers/wechat.import documents.tmp/微信支付账单(xxxxxxxx-xxxxxxxx).csv -f 你的参考账本.bean> test.bean 
# 中国银行
# 首先需要将UTF-16转换成UTF-8
bean-extract importers/boc.import documents.tmp/test.csv -f 你的参考账本.bean> test.bean

# 招商银行
# 数据源：信用卡账单电子邮件
# 需要在招行网银上将账单邮寄方式改为“电子邮件（含明细）”
# 然后在邮件客户端上下载“招商银行信用卡电子账单xxx.eml”
bean-extract importers/cmb_eml.import documents.tmp/招商银行信用卡电子账单xxx.eml -f 你的参考账本.bean> test.bean

```

另外感谢[zsxsoft](https://github.com/zsxsoft/my-beancount-scripts)，不得不说，通过eml文件导入账单真是个好主意。
