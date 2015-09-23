__author__ = 'ziguang'
import pprint
pprint.pprint(
{"pr":"90","t":"month","sys":"windows","machine":"default","net":"external","test":"network","company":"GOOGLE","metric":"tcp_stream","links":{"ALI":[{"src":"beijing","target":"shenzhen"},{"src":"beijing","target":"hangzhou"},{"src":"beijing","target":"hongkong"},{"src":"beijing","target":"qingdao"},{"src":"beijing","target":"us"},{"src":"shenzhen","target":"beijing"},{"src":"shenzhen","target":"hongkong"},{"src":"shenzhen","target":"us"},{"src":"hangzhou","target":"beijing"},{"src":"hangzhou","target":"qingdao"},{"src":"hangzhou","target":"us"},{"src":"hongkong","target":"beijing"},{"src":"hongkong","target":"shenzhen"},{"src":"hongkong","target":"hangzhou"},{"src":"hongkong","target":"qingdao"},{"src":"hongkong","target":"us"},{"src":"qingdao","target":"beijing"},{"src":"qingdao","target":"shenzhen"},{"src":"qingdao","target":"hongkong"},{"src":"qingdao","target":"us"},{"src":"us","target":"beijing"},{"src":"us","target":"shenzhen"},{"src":"us","target":"hangzhou"},{"src":"us","target":"hongkong"},{"src":"us","target":"qingdao"}],"AWS":[{"src":"cn","target":"us"},{"src":"cn","target":"virginia"},{"src":"cn","target":"tokyo"},{"src":"us","target":"cn"},{"src":"us","target":"virginia"},{"src":"us","target":"tokyo"},{"src":"virginia","target":"cn"},{"src":"virginia","target":"us"},{"src":"virginia","target":"tokyo"},{"src":"tokyo","target":"cn"},{"src":"tokyo","target":"us"},{"src":"tokyo","target":"virginia"}],"KSYUN":[{"src":"shanghai","target":"beijing"},{"src":"shanghai","target":"hongkong"},{"src":"beijing","target":"shanghai"},{"src":"beijing","target":"hongkong"},{"src":"hongkong","target":"shanghai"},{"src":"hongkong","target":"beijing"}],"QCLOUD":[{"src":"guangzhou","target":"shanghai"},{"src":"guangzhou","target":"hongkong"},{"src":"guangzhou","target":"us"},{"src":"shanghai","target":"guangzhou"},{"src":"shanghai","target":"hongkong"},{"src":"shanghai","target":"us"},{"src":"hongkong","target":"guangzhou"},{"src":"hongkong","target":"shanghai"},{"src":"hongkong","target":"us"},{"src":"us","target":"guangzhou"},{"src":"us","target":"shanghai"},{"src":"us","target":"hongkong"}],"QING":[{"src":"yatai","target":"beijing"},{"src":"yatai","target":"guangdong"},{"src":"beijing","target":"yatai"},{"src":"beijing","target":"guangdong"},{"src":"guangdong","target":"yatai"},{"src":"guangdong","target":"beijing"}],"UCLOUD":[{"src":"beijing","target":"huadong"},{"src":"beijing","target":"us"},{"src":"beijing","target":"yatai"},{"src":"huadong","target":"beijing"},{"src":"huadong","target":"us"},{"src":"huadong","target":"yatai"},{"src":"us","target":"beijing"},{"src":"us","target":"huadong"},{"src":"us","target":"yatai"},{"src":"yatai","target":"beijing"},{"src":"yatai","target":"huadong"},{"src":"yatai","target":"us"}],"AZURE":[{"src":"cndong","target":"cnbei"},{"src":"cndong","target":"westus"},{"src":"cndong","target":"eastus"},{"src":"cnbei","target":"cndong"},{"src":"cnbei","target":"westus"},{"src":"cnbei","target":"eastus"},{"src":"westus","target":"cndong"},{"src":"westus","target":"cnbei"},{"src":"westus","target":"eastus"},{"src":"eastus","target":"cndong"},{"src":"eastus","target":"cnbei"},{"src":"eastus","target":"westus"}],"HUAWEI":[{"src":"huabei","target":"huadong"},{"src":"huabei","target":"huanan"},{"src":"huadong","target":"huabei"},{"src":"huadong","target":"huanan"},{"src":"huanan","target":"huabei"},{"src":"huanan","target":"huadong"}],"GOOGLE":[]}}
)

print({'company': 'GOOGLE',
 'links': {'ALI': [{'src': 'beijing', 'target': 'shenzhen'},
                   {'src': 'beijing', 'target': 'hangzhou'},
                   {'src': 'beijing', 'target': 'hongkong'},
                   {'src': 'beijing', 'target': 'qingdao'},
                   {'src': 'beijing', 'target': 'us'},
                   {'src': 'shenzhen', 'target': 'beijing'},
                   {'src': 'shenzhen', 'target': 'hongkong'},
                   {'src': 'shenzhen', 'target': 'us'},
                   {'src': 'hangzhou', 'target': 'beijing'},
                   {'src': 'hangzhou', 'target': 'qingdao'},
                   {'src': 'hangzhou', 'target': 'us'},
                   {'src': 'hongkong', 'target': 'beijing'},
                   {'src': 'hongkong', 'target': 'shenzhen'},
                   {'src': 'hongkong', 'target': 'hangzhou'},
                   {'src': 'hongkong', 'target': 'qingdao'},
                   {'src': 'hongkong', 'target': 'us'},
                   {'src': 'qingdao', 'target': 'beijing'},
                   {'src': 'qingdao', 'target': 'shenzhen'},
                   {'src': 'qingdao', 'target': 'hongkong'},
                   {'src': 'qingdao', 'target': 'us'},
                   {'src': 'us', 'target': 'beijing'},
                   {'src': 'us', 'target': 'shenzhen'},
                   {'src': 'us', 'target': 'hangzhou'},
                   {'src': 'us', 'target': 'hongkong'},
                   {'src': 'us', 'target': 'qingdao'}],
           'AWS': [{'src': 'cn', 'target': 'us'},
                   {'src': 'cn', 'target': 'virginia'},
                   {'src': 'cn', 'target': 'tokyo'},
                   {'src': 'us', 'target': 'cn'},
                   {'src': 'us', 'target': 'virginia'},
                   {'src': 'us', 'target': 'tokyo'},
                   {'src': 'virginia', 'target': 'cn'},
                   {'src': 'virginia', 'target': 'us'},
                   {'src': 'virginia', 'target': 'tokyo'},
                   {'src': 'tokyo', 'target': 'cn'},
                   {'src': 'tokyo', 'target': 'us'},
                   {'src': 'tokyo', 'target': 'virginia'}],
           'AZURE': [{'src': 'cndong', 'target': 'cnbei'},
                     {'src': 'cndong', 'target': 'westus'},
                     {'src': 'cndong', 'target': 'eastus'},
                     {'src': 'cnbei', 'target': 'cndong'},
                     {'src': 'cnbei', 'target': 'westus'},
                     {'src': 'cnbei', 'target': 'eastus'},
                     {'src': 'westus', 'target': 'cndong'},
                     {'src': 'westus', 'target': 'cnbei'},
                     {'src': 'westus', 'target': 'eastus'},
                     {'src': 'eastus', 'target': 'cndong'},
                     {'src': 'eastus', 'target': 'cnbei'},
                     {'src': 'eastus', 'target': 'westus'}],
           'HUAWEI': [{'src': 'huabei', 'target': 'huadong'},
                      {'src': 'huabei', 'target': 'huanan'},
                      {'src': 'huadong', 'target': 'huabei'},
                      {'src': 'huadong', 'target': 'huanan'},
                      {'src': 'huanan', 'target': 'huabei'},
                      {'src': 'huanan', 'target': 'huadong'}],
           'KSYUN': [{'src': 'shanghai', 'target': 'beijing'},
                     {'src': 'shanghai', 'target': 'hongkong'},
                     {'src': 'beijing', 'target': 'shanghai'},
                     {'src': 'beijing', 'target': 'hongkong'},
                     {'src': 'hongkong', 'target': 'shanghai'},
                     {'src': 'hongkong', 'target': 'beijing'}],
           'QCLOUD': [{'src': 'guangzhou', 'target': 'shanghai'},
                      {'src': 'guangzhou', 'target': 'hongkong'},
                      {'src': 'guangzhou', 'target': 'us'},
                      {'src': 'shanghai', 'target': 'guangzhou'},
                      {'src': 'shanghai', 'target': 'hongkong'},
                      {'src': 'shanghai', 'target': 'us'},
                      {'src': 'hongkong', 'target': 'guangzhou'},
                      {'src': 'hongkong', 'target': 'shanghai'},
                      {'src': 'hongkong', 'target': 'us'},
                      {'src': 'us', 'target': 'guangzhou'},
                      {'src': 'us', 'target': 'shanghai'},
                      {'src': 'us', 'target': 'hongkong'}],
           'QING': [{'src': 'yatai', 'target': 'beijing'},
                    {'src': 'yatai', 'target': 'guangdong'},
                    {'src': 'beijing', 'target': 'yatai'},
                    {'src': 'beijing', 'target': 'guangdong'},
                    {'src': 'guangdong', 'target': 'yatai'},
                    {'src': 'guangdong', 'target': 'beijing'}],
           'UCLOUD': [
                     {'src': 'beijing', 'target': 'yatai'},

                      {'src': 'yatai', 'target': 'beijing'}]},
 'machine': 'default',
 'metric': 'tcp_stream',
 'net': 'external',
 'pr': '90',
 'sys': 'windows',
 't': 'month',
 'test': 'network'})

pprint.pprint({'machine': 'default', 'pr': '90', 'sys': 'windows', 't': 'month', 'links': {'HUAWEI': [{'src': 'huabei', 'target': 'huadong'}, {'src': 'huabei', 'target': 'huanan'}, {'src': 'huadong', 'target': 'huabei'}, {'src': 'huadong', 'target': 'huanan'}, {'src': 'huanan', 'target': 'huabei'}, {'src': 'huanan', 'target': 'huadong'}], 'UCLOUD': [{'src': 'beijing', 'target': 'yatai'}, {'src': 'yatai', 'target': 'beijing'}], 'KSYUN': [{'src': 'shanghai', 'target': 'beijing'}, {'src': 'shanghai', 'target': 'hongkong'}, {'src': 'beijing', 'target': 'shanghai'}, {'src': 'beijing', 'target': 'hongkong'}, {'src': 'hongkong', 'target': 'shanghai'}, {'src': 'hongkong', 'target': 'beijing'}], 'ALI': [{'src': 'beijing', 'target': 'shenzhen'}, {'src': 'beijing', 'target': 'hangzhou'}, {'src': 'beijing', 'target': 'hongkong'}, {'src': 'beijing', 'target': 'qingdao'}, {'src': 'beijing', 'target': 'us'}, {'src': 'shenzhen', 'target': 'beijing'}, {'src': 'shenzhen', 'target': 'hongkong'}, {'src': 'shenzhen', 'target': 'us'}, {'src': 'hangzhou', 'target': 'beijing'}, {'src': 'hangzhou', 'target': 'qingdao'}, {'src': 'hangzhou', 'target': 'us'}, {'src': 'hongkong', 'target': 'beijing'}, {'src': 'hongkong', 'target': 'shenzhen'}, {'src': 'hongkong', 'target': 'hangzhou'}, {'src': 'hongkong', 'target': 'qingdao'}, {'src': 'hongkong', 'target': 'us'}, {'src': 'qingdao', 'target': 'beijing'}, {'src': 'qingdao', 'target': 'shenzhen'}, {'src': 'qingdao', 'target': 'hongkong'}, {'src': 'qingdao', 'target': 'us'}, {'src': 'us', 'target': 'beijing'}, {'src': 'us', 'target': 'shenzhen'}, {'src': 'us', 'target': 'hangzhou'}, {'src': 'us', 'target': 'hongkong'}, {'src': 'us', 'target': 'qingdao'}], 'AZURE': [{'src': 'cndong', 'target': 'cnbei'}, {'src': 'cndong', 'target': 'westus'}, {'src': 'cndong', 'target': 'eastus'}, {'src': 'cnbei', 'target': 'cndong'}, {'src': 'cnbei', 'target': 'westus'}, {'src': 'cnbei', 'target': 'eastus'}, {'src': 'westus', 'target': 'cndong'}, {'src': 'westus', 'target': 'cnbei'}, {'src': 'westus', 'target': 'eastus'}, {'src': 'eastus', 'target': 'cndong'}, {'src': 'eastus', 'target': 'cnbei'}, {'src': 'eastus', 'target': 'westus'}], 'QING': [{'src': 'yatai', 'target': 'beijing'}, {'src': 'yatai', 'target': 'guangdong'}, {'src': 'beijing', 'target': 'yatai'}, {'src': 'beijing', 'target': 'guangdong'}, {'src': 'guangdong', 'target': 'yatai'}, {'src': 'guangdong', 'target': 'beijing'}], 'AWS': [{'src': 'cn', 'target': 'us'}, {'src': 'cn', 'target': 'virginia'}, {'src': 'cn', 'target': 'tokyo'}, {'src': 'us', 'target': 'cn'}, {'src': 'us', 'target': 'virginia'}, {'src': 'us', 'target': 'tokyo'}, {'src': 'virginia', 'target': 'cn'}, {'src': 'virginia', 'target': 'us'}, {'src': 'virginia', 'target': 'tokyo'}, {'src': 'tokyo', 'target': 'cn'}, {'src': 'tokyo', 'target': 'us'}, {'src': 'tokyo', 'target': 'virginia'}], 'QCLOUD': [{'src': 'guangzhou', 'target': 'shanghai'}, {'src': 'guangzhou', 'target': 'hongkong'}, {'src': 'guangzhou', 'target': 'us'}, {'src': 'shanghai', 'target': 'guangzhou'}, {'src': 'shanghai', 'target': 'hongkong'}, {'src': 'shanghai', 'target': 'us'}, {'src': 'hongkong', 'target': 'guangzhou'}, {'src': 'hongkong', 'target': 'shanghai'}, {'src': 'hongkong', 'target': 'us'}, {'src': 'us', 'target': 'guangzhou'}, {'src': 'us', 'target': 'shanghai'}, {'src': 'us', 'target': 'hongkong'}]}, 'net': 'external', 'test': 'network', 'company': 'GOOGLE', 'metric': 'tcp_stream'})