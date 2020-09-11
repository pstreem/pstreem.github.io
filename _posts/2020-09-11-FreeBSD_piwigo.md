---
title: Piwigo是一个开源网路图床
date: 2020-09-11 22:09:20
tags: [FreeBSD, Tools]
---

Piwigo, 是一个开源网络图床, 上传图片在其他站点引用.

# install base pkg

`pkg install nginx php72 mariadb103-server`

`sysrc php_fpm_enable=YES`

`sysrc nginx_enable=YES`

`sysrc mysql_server=YES`

# modify the configuration



## nginx

modify the root location to /usr/local/www/piwigo

add `index.php` to the index list 

high light the php configuration :

```
        location ~ \.php$ {
            root           html;
            fastcgi_pass   192.168.100.7:9000;
            fastcgi_index  index.php;
            #fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
            #fastcgi_param  SCRIPT_FILENAME  $document_root/$fastcgi_script_name;
            fastcgi_param  SCRIPT_FILENAME  /usr/local/www/piwigo/$fastcgi_script_name;
            #fastcgi_param  SCRIPT_FILENAME  $fastcgi_script_name;
            include        fastcgi_params;
        }
```

## php

modify the listen IP address to the lo1 interface 

## mariadb

`mysql -u root`

> create user 'piwigo'@'%' identified by 'piwigo';
>
> create database piwigo;
>
> grant all on piwigo.* to 'piwigo'@'%';

# build up piwigo



`pkg install piwigo`

access the URL like : http://192.168.100.7/

select language to English and input some parameters like Mariadb user/password/dbname etc.

then th piwigo is ready to use .



# backup & restore or upgrade

local configuration in the folder `piwigo/local`

## backup DB

1. install the backup tool : `pkg install xtrabackup` or  use the dump tools 
2. backup
   - mysqldump piwigo_db > piwigo.sql
   - mysqldump --database dbname1 [dbname2 ....] > db_list.sql
   - mysqldump --all-databases > alldatabases.sql
   - mysqldump --all-databases --single-transaction all_databases.sql    //for InnoDB online backup
   - mysqldump --all-databases --master-data=2 > all_databases.sql      //include the binary log
   - mysqldump --all-databases --flush-logs --master-data=2 > all_databases.sql    //include the binary & flush log
3. restore
   - mysql piwigo_db < piwigo.sql 
   - mysql -e "piwigo.sql" piwigo_db 
4. backup and resotre remote host
   - mysqldump --opt piwigo_db | mysql --host=remote_host -C piwigo_db



## prepare the piwigo file

download [download URL](https://piwigo.org/ext/download.php?eid=391) for backup tools

upload the `prep21up.php` to the folder of piwigo 

access the file use browser [update](http://img.azming.com/prep21up.php) and download the `upgrade.zip` file&documents

unzip the zip and export the local o the new piwigo folder .