# coding=utf-8

from huoyansdk.sms import SmsClient

# 请将参数替换成自己的
client = SmsClient("access_key_id", "access_key_secret")
res = client.send_sms('手机号', '短信签名', '短信模板Code', '模板参数，JSON字符串')
print(res)
