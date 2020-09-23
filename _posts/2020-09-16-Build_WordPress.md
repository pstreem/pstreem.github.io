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

# 配置daemon启动进程
sysrc nginx_enable="YES"
sysrc php_fpm_enable="YES"


# 故障排查点

当Mysql无法启动的时候, 需要修改的地方:
```
cd /var/run/
chown -R mysql mysql
```


配置Wordpress的目录权限, 可以写入`config.php`文件
```
cd /usr/local/www/chown -R www wordpress/
```

# 配置启动的基础信息


## 配置Mysql的安全特性,主要是给root设置密码.
```
/usr/local/bin/mysql_secure_installation
```


## 配置修改nginx的php的解析
```
            #root           /usr/local/www/wordpress;
            root           /opt/web;
            fastcgi_pass   192.168.1.200:9000;
            fastcgi_index  index.php;
            #fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
            fastcgi_param  SCRIPT_NAME  $fastcgi_script_name;
```

## 配置mysql的数据库账户及创建数据库

mysql -u root -p //根据提示输入密码进行mysql控制台

```
CREATE DATABASE wordpress;

GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress_user'@'%' IDENTIFIED BY 'mypassword' WITH GRANT OPTION;  

FLUSH   PRIVILEGES; 
```

## 后续即可访问wordpress进行后续配置

