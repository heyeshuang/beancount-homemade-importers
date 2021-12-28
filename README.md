<http://blog.heysh.xyz/2019/11/07/netease-youqian-with-beancount/>

## 环境设置

建议使用[Anaconda](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
来进行环境管理。我之前用的Poetry在Windows下配置出现了一些小问题。

```bash
conda env create -f environment.yml
conda activate bc
```
当然也可以直接按照`environment.yml`安装需要的Packages。

## Auto initialize some income/expense accounts for Beancount

```bash
python importers/youqian/accountInit.py > New_Accounts.bean
# 如果已经建立了一部分账户
python importers/youqian/accountInit.py Existing_Accounts.bean > New_Accounts.bean
```

## Import Netease Youqian（网易有钱）

```
bean-extract importers/youqian/youqian_expense.import documents.tmp/expense.csv > expense.bean
bean-extract importers/youqian/youqian_income.import documents.tmp/income.csv > income.bean
```

## Other importers

[smart_importer](https://github.com/beancount/smart_importer) needs to be installed to import smartly.

### 微信

数据来源：`支付-钱包-账单-常见问题-下载账单-用作个人对账`

```bash
bean-extract importers/wechat.import documents.tmp/微信支付账单(xxxxxxxx-xxxxxxxx).csv -e 你的参考账本.bean> test.bean 
```

### 中国银行借记卡

数据来源：中国银行网上银行（网页版），需要将UTF-16转换成UTF-8

```bash
bean-extract importers/boc.import documents.tmp/test.csv -e 你的参考账本.bean> test.bean
```
### 招商银行信用卡

数据源为信用卡账单电子邮件。需要在招行网银上将账单邮寄方式改为“电子邮件（含明细）”，然后在邮件客户端上下载“招商银行信用卡电子账单xxx.eml”

```bash
bean-extract importers/cmb_eml.import documents.tmp/招商银行信用卡电子账单xxx.eml -e 你的参考账本.bean> test.bean
```

### 民生银行借记卡

在手机网上银行上可以导出PDF格式的民生银行借记卡账单。通过`Camelot-py`读取PDF。

```bash
bean-extract importers/cmbc_pdf.import documents.tmp/pdf_mxXXXXXX.pdf -e 你的参考账本.bean> test.bean
```

## 可能出现的问题

- 在Windows的CMD下，通过`>`输出的文件编码可能有误，需要在运行命令前设置环境变量：

```CMD
set PYTHONIOENCODING=utf-8:surrogateescape
```


另外感谢[zsxsoft](https://github.com/zsxsoft/my-beancount-scripts)，不得不说，通过eml文件导入账单真是个好主意。
