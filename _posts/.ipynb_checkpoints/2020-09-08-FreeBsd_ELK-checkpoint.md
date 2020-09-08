---
title: 在FreeBSD下Initialize ELK
date: 2020-09-08 15:49:20
tags: [FreeBSD, ELK]
---

ELK is a summary name by `elasticsearch` `Logstash` `Kibana` this co-package can collect the log and analysis then output the report. suggest: use the filebeat replace logstash .

# install the package use pkg
   `pkg install elasticsearch6 kibana6 logstash6`
   this will install jdk8 in the system automate
   update:
   `pkg insall beats`
   this include : `filebeat` , `heartbea` , `metricbeat` ;
# config the module
## elasticsearch
1. modify the memory about JVM
file path : `/usr/local/etc/elasticsearch/jvm.options`

the values as below will be enough
```
-Xms256M
-Xmx256M
```

## logstash
1. modify the memory about JVM
file path `/usr/local/etc/logstash/jvm.options`


# config and start service

```
sysrc elasticsearch_enable=YES
sysrc filebeat_enable=YES
sysrc kibana_enable=YES
```

# modify maxfiles in sysctl
 max file descriptors [14031] for elasticsearch process is too low, increase to at least [65536]
sysctl kern.maxfiles=65536
sysctl kern.maxfilesperproc=65536