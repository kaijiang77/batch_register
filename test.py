import requests
import json

req = requests.get('https://www.snapmail.cc/emailList/jiangkai@snapmail.cc?isPrefix=True&count=1')
email_text = json.loads(req.text)
print(email_text)