CategoryAsset = {
    "工商银行":"Assets:Bank:ICBC:Card0000",
    "农业银行":"Assets:Bank:ABC:Card0000",
    "微信钱包":"Assets:WeChat:Wallet",
    "我的其他账户":"Assets:Whatever",
    "现金钱包":"Assets:Cash",
    "招商银行":"Liabilities:CreditCards:CMB:Card",
    "支付宝":"Assets:Alipay:YuEBao",
    "中国银行":"Assets:Bank:BOC:Card0000",
    'DEFAULT':'Assets:FIXME'
}
CategoryExpense = {
    '交通':"Expenses:Traffic:Others",
    '交通,打车':'Expenses:Traffic:Taxi',
    '交通,机票':'Expenses:Traffic:Aircraft',
    '交通,火车':'Expenses:Traffic:Train',
    '人情':'Expenses:Gift:Weddings',
    '住房':'Expenses:Charges:Utilities',
    '医疗':'Expenses:Health:Medical',
    '娱乐':'Expenses:Entertainment:Others',
    '投资亏损':'Expenses:StupidTax',
    '文教':'Expenses:Shopping:Books',
    '旅行':'Expenses:Travel',
    '汽车':'Expenses:Traffic:Car',
    '购物':"Expenses:Shopping:Others",
    '购物,数码':'Expenses:Shopping:Electronics',
    '购物,日用':'Expenses:Shopping:Commodities',
    '购物,玩具':'Expenses:Shopping:Hobbies',
    '购物,电器':'Expenses:Shopping:Appliances',
    '购物,美妆':'Expenses:PersonalCare:Hair',
    '购物,运动用品':'Expenses:Shopping:Sports',
    '购物,鞋服':"Expenses:Shopping:Clothing",
    '购物,饰品':"Expenses:Shopping:Clothing",
    '通讯':'Expenses:Charges:Communication',
    '零食烟酒':'Expenses:Food:Snacks',
    '零食烟酒,水果':'Expenses:Food:Snacks',
    '零食烟酒,烟酒':'Expenses:Food:Drinks',
    '零食烟酒,茶水':'Expenses:Food:Drinks',
    '零食烟酒,零食':'Expenses:Food:Snacks',
    '零食烟酒,饮料':'Expenses:Food:Drinks',
    '餐饮':'Expenses:Food:Others',
    '餐饮,三餐':'Expenses:Food:Canteen',
    '餐饮,食材':'Expenses:Food:Ingredients',
    '其他':'Expenses:FIXME',
    'DEFAULT':'Expenses:FIXME'
}
CategoryIncome = {
    '公积金':'Income:Job:HouseProvident',
    '其他收入':'Income:Others', 
    '利息收入':'Income:Rental:CQY', 
    '奖金':'Income:Job:Subsidy', 
    '意外所得':'Income:Others',
    '报销收入':'Income:Reimbursements', 
    '薪资':'Income:Job:Salary', 
    '退款':'Income:Reimbursements',
    'DEFAULT':'Income:FIXME', 

}
CategoryAll = {**CategoryIncome,**CategoryAsset,**CategoryExpense}