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