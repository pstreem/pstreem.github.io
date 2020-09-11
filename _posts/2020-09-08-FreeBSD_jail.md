---
title: 利用FreeBSD原生Jail来管理jail
date: 2020-09-08 15:09:20
tags: [FreeBSD, Jail]
---

Jail的管理手段有很多, 包含ezjail, cbsd等; 从个人的简单需求以及对于epair的管理来看, 通过原生jail的配置进行管理是最简单的.

# zfs的环境准备

创建相关的zfs
```
# zfs create -o compress=lz4 -o mountpoint=/jails vtank/jails
# zfs create vtank/jails/basejail
```

# basejail环境准备

创建basejail 并且创建基础模板.

```
# wget https://download.freebsd.org/ftp/releases/amd64/11.2-RELEASE/base.txz 
# wget https://download.freebsd.org/ftp/releases/amd64/11.2-RELEASE/lib32.txz
# tar -zxvf ~/base.txz -C /jails/basejail 
# tar -zxvf ~/lib32.txz -C /jails/basejail
# freebsd-update -b /jails/basejail fetch install
# freebsd-update -b /jails/basejail IDS
```

创建snapshot, 制作fullbase的模板

```
# zfs snapshot vtank/jails/basejail@base
# zfs clone vtank/jails/basejail@base vtank/jails/fullbase
# cd /jails/fullbase
# chflags 0 lib/*
# chflags 0 sbin/*
# rm -Rf bin boot lib libexec rescue sbin
# mdkir basejail
# mount_nullfs /jails/basejail /jails/fullbase/basejail
# ln -s basejail/bin
# ln -s basejail/boot
# ln -s basejail/lib
# ln -s basejail/libexec
# ln -s basejail/rescue
# ln -s basejail/sbin
# zfs snapshot vtank/jails/fullbase@base
```

# Jail 配置及启动

基于fullbase模板 , 创建所需的jail

```
# zfs clone vtank/jails/fullbase@base vtank/jails/web
```
每次创建jail, 需要改动/etc/jail.conf配置文件, 样例如下, 采用epair配置网络.

```
host.hostname = "${name}.azming.com";
path = "/jails/${name}";

exec.start = "/bin/sh /etc/rc";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.clean;
allow.raw_sockets;
mount.devfs;
devfs_ruleset="4";

exec.system_user = "root";
exec.jail_user = "root";

vnet;
exec.consolelog = "/var/log/jail_${name}_console.log";

exec.prestart += "cp /etc/resolv.conf $path/etc";
exec.prestart += "cp /etc/hosts $path/etc";

exec.prestart += "ifconfig ${ext_epair} create up";
exec.prestart += "ifconfig bridge0 addm ${ext_epair}a";

exec.prestart += "/sbin/mount -t nullfs -o ro /jails/basejail /jails/$name/basejail" ;

exec.start += "ifconfig ${ext_epair}b $ext_ipadd netmask 255.255.255.0 ";

exec.prestop += "ifconfig ${ext_epair}b -vnet $name";

exec.poststop += "rm $path/etc/resolv.conf";
exec.poststop += "ifconfig bridge0 deletem ${ext_epair}a";
exec.poststop += "ifconfig ${ext_epair}a destroy";
exec.poststop += "umount /jails/$name/basejail";

desktop {
        $ext_epair = "epair10";
        $int_epair = "epair11";
        $ext_ipadd = 192.168.3.250;
        $int_ipadd = 192.168.1.250;
        $gwv4 = "192.168.1.100";
        vnet.interface = "${ext_epair}b", "${int_epair}b";

        exec.prestart += "ifconfig ${int_epair} create up";
        exec.prestart += "ifconfig bridge1 addm ${int_epair}a";
        exec.start += "ifconfig ${int_epair}b $int_ipadd netmask 255.255.255.0 ";
        exec.start += "route add default $gwv4";
        exec.prestop += "ifconfig ${int_epair}b -vnet $name";
        exec.poststop += "ifconfig bridge1 deletem ${int_epair}a";
        exec.poststop += "ifconfig ${int_epair}a destroy";
}
cronrun {
        $ext_epair = "epair20";
        #$int_epair = "epair21";
        $ext_ipadd = 192.168.3.200;
        #$int_ipadd = 192.168.1.200;
        $gwv4 = "192.168.3.1";
        vnet.interface = "${ext_epair}b";
        exec.start += "route add default $gwv4";
}
```
如果不采用epair的方式来配置网络, 配置方案如下:
```
interface = lo1 ;
mount.devfs ;
allow.nomount ;
allow.sysvipc = 0 ;
####
host.hostname = "$name.azming.com" ;
path = "/jail/$name" ;
ip4.addr = 192.168.1.$ip ;
####
#jail for name
jail1 {
        $ip = 1 ;
}
```

# 配置PF能够使jail访问外网以及端口映射

rc.conf配置

```
gateway_enable="YES"

pf_enable="YES"
pf_flags=""
pf_rules="/etc/pf.conf"
pflog_enable="NO"

cloned_interfaces="bridge0 bridge1"
autobridge_interfaces="bridge0 bridge1"
autobridge_bridge0="re0"
autobridge_bridge1="re1"
ifconfig_bridge0="inet 192.168.3.254 netmask 0xffffffff"
ifconfig_bridge1="inet 192.168.1.254 netmask 0xffffffff"
```

pf.conf配置

```
set skip on lo0
#scrub in on vtnet0 all

nat on vtnet0 from 192.168.100.0/24 to any -> (vtnet0)
nat on vtnet0 from 10.0.0.0/16 to any -> (vtnet0)

#ezjail
rdr on vtnet0 inet proto tcp from any to (vtnet0) port 80 -> 192.168.100.100 port 80
rdr on vtnet0 inet proto tcp from any to (vtnet0) port 443 -> 192.168.100.100 port 443

block in on vtnet0 proto tcp from any to any

pass in on vtnet0 proto tcp from any to (vtnet0) port 22 keep state
pass in on vtnet0 proto tcp from any to 192.168.100.100 port 80 keep state
pass in on vtnet0 proto tcp from any to 192.168.100.100 port 443 keep state
pass out on vtnet0 all keep state

pass inet proto icmp all icmp-type echoreq keep state

pass in on lo0 all keep state
pass out on lo0 all keep state
```

# 后续Jail中的工作

```
# jls
# jexec jail_name /bin/csh
# pkg info
# pkg install nginx py37-certbot-nginx
```

# 使用ezjail来管理jail

## install ezjail

use pkg install the package `ezjail`

`pkg install ezjail`

### config the file

modify the `/usr/local/etc/ezjail.conf` file modify the parameters like below :

```
ezjail_use_zfs=YES
ezjail_jailzfs=aliroot/ezjail //the zfs will create by ezjail-admin
ezjail_use_zfs_for_jails=YES
```

there is another parameter like : `ezjail_ftphost=ftp.tw.freebsd.org`

### build the basejail

the basejail will be read only , and ezjail-admin will build basejail .

just install basics . not include ports , manual pages and sources code .

use the command `ezjail-admin install` will install the base OS again .

and you can point the version to install for the command like below :

`ezjail-admin install -r 12.0-RELEASE`

if you want update and install the port or manual or source , can use

`ezjail-admin install -SPM` after above .

some other parameter detail information :

```
ezjail-admin install [-mMpPsS] [-h host] [-r release]
```

```
-m 下载并安装 man 手册页。
-M 下载并安装 man 手册页，但不（重新）安装基本系统。用于基本系统已经安装好，增加 man 手册页。
-p 调用 portsnap 下载安装 ports 树。Tips：下载服务器在哪里设置呢？在 /etc/portsnap.conf。
-P 类似上面，不（重新）安装基本系统。
-s 下载安装源代码。
-S 类似上面，不（重新）安装基本系统。
-h 指定下载服务器。默认使用 ezjail.conf 的服务器。
-r 指定下载的版本。ezjail-admin 会调用 uname -r 来获得默认版本。
```

use the parameter `-i` will build world from world , like `ezjail-admin setup -i`

then ,you can use the `ezjail-admin setup -b` to instalworld.

### keep the ezjail up to date

ezjail can use the freebsd-update tool to keep basejail up to date :

`ezjail-admin update -u` this will upgrade the system release .

`ezjail-admin update -P` this will upgrade the ports tree .

some other parameter detail information :

`ezjail-admin update [-s sourcetree | sourceosversion] [-p] -b | -i | -P | -u | -U`

```
-s 与 -b 或 -i 同用时，指定源代码路径。与 -U 同用时指定用于 freebsd-update 的版本。
-p 调用 portsnap 为基本系统提供 ports 树。
-b make buildworld; make installworld, 更新或安装基本系统。不会清理基本系统的旧文件。
-i make installworld，更新或安装基本系统。如果之前已经 make buildworld 过，这会省很多时间。
-P 仅仅更新 ports。
-u 调用 freebsd-update 更新基本系统，调用 uname -r 获得版本号。注意宿主机系统要同时更新。
-U 调用 freebsd-update 把基本系统升级到和宿主机相同的版本。或者用 UNAME_r 环境变量指定版本。
```

if there is some mistake with `No such file or directory`

you can use this command to fix it:

`mount_nullfs /usr/jails/basejail /basejail`

### start ezjail create a new jail system

```
ezjail-admin create hexo 'lo1|192.168.100.11,em0|192.168.1.50'
```

ezjail-admin start hexo

## create jail automatic by config file

create from flavours  :

`ezjail-admin create -f example hexo 'lo1|192.168.100.1'`



## use the jail to mount the data folder

modify the file `/etc/fstab.*`

add the line :

>  /opt /usr/jails/git/opt nullfs rw,late 0 0

will mount the /opt to the folder in the jail . but use the df in the jail can not see the mount status .

## snapshop and restore

`ezjail-admin snapshot hexo`

if you want rebuild the jail in another machine, use the method:

```
ezjail-admin archive book

ezjail-admin create -a /usr/jails/ezjail_archives/book-201902182303.08.tar.gz book1 'lo1|192.168.100.10'
```



## mount new disk to the os



gpart create -s GPT /dev/vtbd1

gpart add -t freebsd-ufs -a 1M /dev/vtdb1

gpart show vtdb1

newfs -U /dev/vtdb1p1

mount /dev/vtdb1p1

## want use ping inside jail
edit the config per jail
the path is ‘/use/local/etc/ezjail’

every will be have there direct configuration
add the parameters like below:
export jail_jailname_parameters=“allow.raw_sockets=1”

## fix some issue when remove jail
`ezjail_admin delete jail_name`
then, there is a folder need to delete mannal
```
chflags -R noschg /usr/jails/jail_name
rm -Rf /usr/jails/jail_name
```
