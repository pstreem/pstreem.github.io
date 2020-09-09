---
title: 通过Python脚本更新阿里域名解析
date: 2020-09-11 00:26:20
tags: [Python, DNS]
---

通过Python周期性获取外网拨号IP地址, 调用aliyun API来更新DNS解析记录.


自己家里安装了联通的300Mbps的宽带, 希望做一个动态DNS.

在aliyun已经购买了自己的域名, 动态域名的更新, 找了一些资料, 写了一个脚本, 这里稍微记录一下:

# 脚本详细信息

注意中间的四行内容;

1. AccessKey_ID
2. Access_Key_Secret
3. DomainName
4. RR

说明:

access_key, 在阿里云账户管理中, 鼠标移至右上角的个人头像, 可以找到accesskey的申请, 获取后替换;

域名整体是:yourr.domain.com; 分别填写至domainname和rr的位置;

```
#!/usr/bin/env python
#coding=utf-8

import json
from json import load
from urllib.request import urlopen
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
import datetime

#    access_key_id = "-------------"
#    access_key_secret = "---------"

i = str(datetime.datetime.now())
newip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
AccessKey_ID = '------'
Access_Key_Secret = '------'

region_id = "cn-shenzhenI"
DomainName = 'domain.com'
RR = 'yourr'
DomainType = 'A'
UpdateDomain = 'Auto_Lines'
def AliAccessKey(id,Secret,region):
        client = AcsClient(id, Secret, region)
        return client
def GetDNSRecordId(client,DomainName):
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))
        for RecordId in json_data['DomainRecords']['Record']:
            if RR == RecordId['RR']:
                return RecordId['RecordId']
def UpdateDomainRecord(client,RecordId):
    try:
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_Value(newip)
        request.set_Type(DomainType)
        request.set_RR(RR)
        request.set_RecordId(RecordId)
        client.do_action_with_exception(request)
        print("domain:" + DomainName + " host:" + RR + " record_type:" +  DomainType + " record:" +  newip)
    except Exception as e:
        print(i + '    DNS-updated')
def main():
    client = AliAccessKey(AccessKey_ID,Access_Key_Secret,region_id)
    RecordId = GetDNSRecordId(client,DomainName)
    UpdateDomainRecord(client,RecordId)
if __name__ == "__main__" :
    main()
```

# 需要安装的内容

1. Python3.7
2. 通过pip安装的包有:
   - aliyun-python-sdk-alidns
   - aliyun-python-sdk-core
   - aliyun-python-sdk-core-v3
   - aliyunsdkcore

# 采用定时任务进行更新

每10分钟运行一次

```
root@www180:~ # crontab -l
*/10 * * * *  /opt/ddns.py
```