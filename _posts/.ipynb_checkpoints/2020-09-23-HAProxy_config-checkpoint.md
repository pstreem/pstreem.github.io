---
title: 配置HAProxy做为负载均衡前端
date: 2020-09-23 20:56:20
tags: [FreeBSD, HAProxy]
---

在FreeBSD下配置HAproxy, 可以做为多种服务的前端做为负载均衡;

# 软件安装
就是喜欢FreeBSD下面对于软件安装的便捷
`pkg install haproxy`

# 配置更新

haproxy安装完成之后, 在`/usr/local/share/examples/haproxy`目录下有几个参考配置文件.
包含对http, socks, transparent的内容, 可以拷贝一个至`/usr/local/etc`目录下再做修改.

# 配置样例

```
#
# demo config for Proxy mode
# 

global
        maxconn         20000
        ulimit-n	    16384
        log             127.0.0.1 local0 info
        uid             62
        gid             62
        chroot          /var/empty
        nbproc		    4
        daemon

defaults
	mode 		tcp
	log		    global
	balance		source

	retries		3
	option 		redispatch
	option		abortonclose
	timeout		connect 3s
	timeout		client 50000ms
	timeout		server 50000ms

frontend service_in_web
        bind 		    0.0.0.0:80
        mode            tcp          //这里要选择tcp, 选择socks不工作
        #mode           socks
        log             global
        default_backend	out_servers_web

backend out_servers_web
	mode 		tcp
	#mode 		socks
	balance 	roundrobin
	server 		ru0 192.168.3.11:1080 check inter 1000 rise 3 fall 2 weight 1
	server 		jp0 192.168.3.12:1080 check inter 1000 rise 3 fall 2 weight 2

frontend service_in_https
        bind 		    0.0.0.0:443
        mode            tcp
        #mode           socks
        log             global
        default_backend	service_out_https

backend service_out_https
	mode 		tcp
	#mode 		socks
	balance 	roundrobin
	server 		r_https s1.domain.com:443 check inter 300000 rise 3 fall 2 weight 1
	server 		j_https s2.domain.com:443 check inter 300000 rise 3 fall 2 weight 2

listen admin_statue            //这里是针对监控界面的配置信息
	bind 		0.0.0.0:8887
	mode 		http
	log 		global
	stats 		refresh 5s
	stats 		uri /haproxy
	stats 		realm Private lands
	stats 		auth admin:password
	stats 		hide-version
	stats		admin if TRUE
```

