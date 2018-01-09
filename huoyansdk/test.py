# coding=utf-8

from huoyansdk.sms import SmsClient

# 请将参数替换成自己的
client = SmsClient(access_key_id="access_key_id", access_key_secret="access_key_secret")
res = client.send_sms(phone_number='手机号', sign_name='短信签名', template_code='短信模板Code',
                      template_param='模板参数,JSON字符串,没有就留空')
print(res)
