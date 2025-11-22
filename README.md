花了一点时间，把本人现在仍然在使用的importers升级成beancount v3 (beangulp) 版本了。

## 环境设置

建议使用Pixi来进行环境管理，不过不管理也没什么问题。自行按照pixi.toml安装依赖也可以。

使用之前记得在源文件里修改账户名称。

## 微信导入

数据来源：`服务-钱包-账单-右上角-下载账单-用作个人对账`，因为我没搞定，请手动把xlsx文件转成csv。

把转换好的文件放在`documents.tmp/微信支付账单(xxxxxxxx-xxxxxxxx).csv`。
```bash
# 导入
python importers/wechat.py extract documents.tmp/微信支付账单*.csv -e template.bean > temp_wx.bean
# 归档
python importers/wechat.py archive  documents.tmp -o documents
```

### 中国银行借记卡

数据来源：中国银行网上银行（网页版）。

```bash
# 导入
python importers/boc.py extract documents.tmp/AccountTransDetail* -e template.bean >temp_boc.bean
# 归档
python importers/boc.py archive  documents.tmp -o documents
```
### 招商银行信用卡

数据源为信用卡账单电子邮件。需要在招行网银上将账单邮寄方式改为“电子邮件（含明细）”，然后在邮件客户端上下载“招商银行信用卡电子账单xxx.eml”。

之前的JSON方法随着手机页面升级失效了，等下次邮件坏掉的时候我再想办法。


```bash
# 导入
python importers/cmb_eml.py extract documents.tmp/招商银行信用卡* -e template.bean > temp_cmb.bean
# 归档
python importers/cmb_eml.py archive documents.tmp -o documents
```

### 民生银行借记卡

还没搞，欢迎PR。

### 招商银行借记卡

在`手机招商银行-收支明细-右上角-打印流水`那里。

```bash
# 导入
python importers/cmb_debit_pdf.py extract documents.tmp/招商银行交易流水* -e template.bean > temp_cmbd.bean
# 归档
python importers/cmb_debit_pdf.py archive  documents.tmp -o documents 
```

题外话，beancount v2到v3的升级没有我想象得复杂，那里报错点哪里就行，我甚至没vide——当然我也用不明白。