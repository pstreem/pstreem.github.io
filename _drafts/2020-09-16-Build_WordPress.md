---
title: 使用WordPress建立商务站点
date: 2020-09-16 21:53:20
tags: [FreeBSD, WordPress]
---





在FreeBSD系统下使用WordPress建立公司站点



# 安装必要的软件包
总共需要大概1G的空间大小
pkg install mariadb104-server
pkg install wordpress (本身安装了php74, 但是依赖是php72)
pkg install nginx

sysrc nginx_enable="YES"
sysrc php_fpm_enable="YES"

cd /var/run/
chown -R mysql mysql


/usr/local/bin/mysql_secure_installation
cd /usr/local/www/chown -R www wordpress/


            #root           /usr/local/www/wordpress;
            root           /opt/web;
            fastcgi_pass   192.168.1.200:9000;
            fastcgi_index  index.php;
            #fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
            fastcgi_param  SCRIPT_NAME  $fastcgi_script_name;

1. GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'%' IDENTIFIED BY 'mypassword' WITH

      GRANT OPTION;  

  2.FLUSH   PRIVILEGES; 
