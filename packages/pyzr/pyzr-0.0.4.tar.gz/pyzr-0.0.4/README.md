# tools Package
***

## alert 模块
###可用于qywx报警/通知  
from pyzr import Alert  
alert= Alert(name='test', url='https://xxxxxx')  
参数：  
name      报警描述，必传  
url       报警链接，必传  
delay     是否降低报警频率，可选，默认值为 False  
interval  报警频率间隔，可选，在delay为True时才能生效，默认值为 10 (单位：s)  

包含四个方法:  
alert.error('test...')  
alert.warning('test...')  
alert.info('test...')  
alert.statistics('test...')  

***

## phone 模块
###可用于电话告警  
from pyzr import Phone  
phone= Phone(uid='xxxx', url='https://xxxxxx', token='xxxxx', model_code='xxxxx')  
参数：  
uid         创建人id，必传  
url         电话告警链接，必传  
token       电话告警token，必传  
model_code  电话告警模版编号，必传  

包含一个方法:  
phone.alter_phone(mobiles, data)  
参数:  
mobiles   告警发给的人，发给多人使用 list 或 以英文逗号隔开的 str，例如: '18xxx' or '181xxx,182xxx'  
data      电话告警内容，type: dict, 例如: {"system": "xx平台", "server": "xx系统", "error": "xxx", "level": "p0"}  
