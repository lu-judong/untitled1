import requests
import json
from interfaceTest.config.config import *

# fp = open('{}/1.txt'.format(path_dir),'w',encoding='UTF-8')

# fp = open('{}/testFile/test_4_ramsEvalute_charts_34e0bf00d47f4b1ea6c518287ce7a86d.txt'.format(path_dir),'wb')
# a = {"chartsQuery":{
# "chartCodes": [],
# "modelId": "34e0bf00d47f4b1ea6c518287ce7a86d",
# 	"interval": 1
# }
# }
body = {"confModelId": "{}".format("304965548066869248"),


                        }

# a = requests.post(interface_url + "/darams/supplier-rams/chart3", headers={
#                             "Authorization": "18106a67-274d-41c4-876e-5b1dfa4cc75f","Content-Type": "application/json;charset=UTF-8"},params=body
#                ,                                         )
a = requests.post(interface_url+"/darams/model/fmeca/export",headers={"Authorization": "18106a67-274d-41c4-876e-5b1dfa4cc75f"},params=body)

a1 = json.loads(a)

a2 = json.dumps(a1['success'], ensure_ascii=False)
# # fp.write(a.text.encode())
# c = json.loads(fp.read())
# d = json.loads(a.text)
# del c['token']
# del d['token']
# if c == d:
# 	print(1)
# else:
# 	print(2)
# fp.write('1')
# fp.close()

