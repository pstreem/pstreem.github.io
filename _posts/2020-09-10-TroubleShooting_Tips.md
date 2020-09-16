---
title: 记录各种TroubleShooting&Tips
date: 2020-09-08 15:09:20
tags: [FreeBSD, Jail, Git, DB, NFS]
---

各类故障及技巧的说明汇总


# troubleshooting

## Jail下的postgresql无法正常启动

发现问题： create shared memory segment faile

解决方法：
jail -m jid=3 allow.sysvipc=1
sysctl security.jail.sysvipc_allowed=1


## Pgsql 添加用户

```
su - postgres
```

```
createdb -O user dbname
```

or

```
createdb dbname
GRANT permissions ON DATABASE dbname TO username;
```



## FreeBSD升级版本之后PKG不可用

先强制删除pkg, 然后重新安装.

`pkg remove -f pkg`

`pkg install pkg`


# Tips

## SSH密钥登陆

ssh-keygen
cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
check the permission of :
.ssh  == 700
authorized_keys == 600

>and modify the sshd_config to allow root login


## 使用CertBOt来更新ssl证书

安装certbot,推荐使用nginx插件. `pkg install py37-certbot-nginx`
配置:
```
#certbot --nginx
```

根据提示信息推动即可.

## Github的使用

### install the git tools is the first step

`pkg install -y git`

as you know , you need config the git like thie :

```
git config –global user.name “yourusername”
git config –global user.email “youremailaddress”
```
you can use `git config --list` to check .

the config file is in the floder:

#~/.gitconfig
or
#repo-dir/.git/config

### initialization the folder

create the folder:

```
mkdir /opt/content.git
cd /opt/content.git
git init
git add .
git commit -m 'from BSD'
```

download the README.md to local

modify if you need 

`git add README.md`

or `git add . ` add all file in the folder to repo

### add the remote origin repo

`git remote add origin git@github.com:pstreem/azming.content.git`

### new folder to clone the repo from github

```
mkdir ~/some+folder
cd some+folder
git init
git remote add origin git@github.com:pstreem/azming.blog.git
git pull origin master
> if you want use git pull replace the command above 
git commit -m 'commit from gitlog'
git push -u origin master
```

### pull/push , sync file 

first , you can clone the remote repo to local :

`git clone git@github.com:michaelliao/gitskills.git`
or use https protocal like this :
`git clone https://github.com/pstreem/azming.content.git`

`git pull origin master`

`git push -u origin master`

### some useful commands
>git log
>git status
>git diff


# upgrade FreeBSD from Version A -> B

## double check the version
> freebsd-version

>>11.2-RELEASE-p7

> uname -mrs

>>FreeBSD 11.2-RELEASE-p7 amd64

## update the binary use freebsd-update
> freebsd-update fetch install

> pkg update && pkg upgrade

## use freebsd-update to upgrade

> freebsd-update -r 12.0-RELEASE upgrade

## commit the upgrade

> freebsd-update install

> reboot the system & freebsd-update install again

## upgrade package

after upgrade system , you need upgrade the pkg again use the command as below :
> pkg-static install -f pkg
> pkg update
> pkg upgrade

after pkg upgrade , please use :
> freebsd-update install
double check again

## double check the system version

> freebsd-version

> uname -mrs

> freebsd-update fetch install 

## makesure the system is normally 

> ps auxw
> sockstat -l
> netstat -anp
> top

# FreeBSD Bhyve passthru

## 手动方式

```
devctl detach pci0:4:0:0
devctl set driver pci0:4:0:0 ppt
pciconf -lv
```
modify the configuration in vm, and the line into the conf file:
```
passthru0="4/0/0"

```

## 随系统配置

/boot/loader.conf
```
pptdevs="0/20/0"
```

bhyve VM config:
```
passthru0="0/20/0"
```

