---
title: 使用Hexo来管理Markdown完成的文章
date: 2020-09-08 15:29:20
tags: [Hexo, Markdown]
---

build blog use Hexo , and use hexo-admin as the manager UI , start as daemon use pm2

# create the environment
## install base package
`pkg install npm`
`npm install hexo-cli -g`
## initialize the blog folder
`cd /opt/nginx`
`hexo init markdown`
`cd /opt/nginx/markdown`
`npm install `
## update the package for the npm
update package install locally 
`npm update`
update package installed global
`npm update -g`

## plugin install - hexo-admin
in the initialized folder , install the hexo-admin plugin 
`npm install --save hexo-admin`

## create the deploy script
create the file like this , located in the hexo folder and named `hexo-generate.sh`
```
#!/usr/bin/env sh
#hexo clean
hexo g
```
modify the hexo _config.yml , find and edit the line below :
```
deployCommand: './hexo-generate.sh'
```
## git and get the theme
git & clone the NexT theme like this commands ; mostly you need install the `git` package.
`git clone https://github.com/theme-next/hexo-theme-next themes/next`
## start hexo as a service manual
`hexo server -i 192.168.1.5 -p 4000`
## start hexo as a daemon use pm2
running hexo as a service use pm2
`npm install pm2 -g`

and install `pm2-logrotate` manage the log file .

`pm2 install pm2-logrotate`

### config the json and start script

totally 2 file you needed create :

1. hexo-daemon.json

```
{
  "apps": [
    {
      "name": "hexo-server",
      "cwd": "/opt/nginx/markdown",
      "script": "./hexo-running.sh",
      "exec_interpreter": "sh",
      "min_uptime": "30s",
      "max_restarts": 30,
      "exec_mode": "fork",
      "error_file": "./logs/pm2.error.log",
      "out_file": "./logs/pm2.out.log",
      "pid_file": "./logs/hexo-server.pid",
      "watch": [
        "_config.yml",
        "./themes/next/_config.yml"
      ],
      "ignor_watch": [
        "node_modules",
        "logs",
        "public",
        "source"
      ],
      "watch_options": {
        "followSymlinke": false
      }
    }
]}
```

2. hexo-running.sh

```
#!/usr/bin/env sh
hexo server -i 192.168.1.5 -p 4000
```
start pm2 use the command below:
`pm2 start hexo-daemon.json`
some other useful parameter:

```
pm2 list 
pm2 delete [id]
pm2 start app.js
pm2 logs app_name
pm2 monit
```

### add pm2 to start script

if the system is new install , you need double check if the folder is exist `/usr/local/etc/rc.d`

`pm2 startup -u root`

`pm2 save`

`pm2 resurrect`

`pme unstartup rcd` //delete pm2 from the start script


# add search plugins in the hexo ecosystem



`npm install hexo-generator-search --save`

`npm install hexo-generator-searchdb --save`

add the follow content to the hexo config.yml :

```
search:
  path: search.xml
  field: post
  format: html
  limit: 10000
```



# submit the blog to search engine

install the sitmap plugins 

`npm install hexo-generator-sitemap --save`

`npm install hexo-generator-baidu-sitemap --save`

and then build the sitemap file , you need add the config to the hexo _config.yml 

```
sitemap:
    path: sitemap.xml
baidusitemap:
    path: baidusitemap.xml
```

## submit the sitemap to google 

[google 站长工具](https://www.google.com/webmasters/tools)

添加站点验证，然后选择-- 抓取 -- 站点地图 -- 测试等步骤完成

## submit the sitemap to baidu

[baidu 站长工具](http://zhanzhang.baidu.com)

连接提交自己的站点就可以了

# add mermaid/sequence/flowchart diagrams

`npm install hexo-filter-mermaid-diagrams`
`npm install hexo-filter-flowchart`
`npm install hexo-filter-sequence`

modify the _config of hexo:
```
# mermaid chart
mermaid: ## mermaid url https://github.com/knsv/mermaid
  enable: true  # default true
  version: "7.1.2" # default v7.1.2
  options:  # find more api options from https://github.com/knsv/mermaid/blob/master/src/mermaidAPI.js
    #startOnload: true  // default true
```

add the line below in the file of next themes 
`./themes/next/layout/_partials/footer.swig`

```
{% if theme.mermaid.enable %}
  <script src='https://unpkg.com/mermaid@{{ theme.mermaid.version }}/dist/mermaid.min.js'></script>
  <script>
    if (window.mermaid) {
      mermaid.initialize({{ JSON.stringify(theme.mermaid.options) }});
    }
  </script>
{% endif %}
```