# 服务器配置说明
## 1. 问题描述

如果我i有两台服务器：43.138.46.106和47.92.79.45，怎么设置访问47.92.79.45时将请求转发到43.138.46.106，但是直接访问43.138.46.106显示403，即只能通过访问47.92.79.45将请求转发到43.138.46.106才能正常访问43.138.46.106的资源，请问这个应该怎么设置，请给出nginx文件的详细配置教程

## 2. 解决方案
### 1. 43.138.46.106服务器的nginx配置
在此服务器上部署的是一个django项目

```cat /etc/nginx/conf.d/apps.conf```

```
server {
    listen 80;
    server_name _ localhost;

    root /var/www/html/Podcaster;  
    location /static{ 
        alias /var/www/html/Podcaster/static;
    }
    location / {
        include /etc/nginx/uwsgi_params;
        uwsgi_pass localhost:9001;
    }
}
```
### 2. 47.92.79.45服务器的nginx配置
这里我们使用nginx进行代理转发
```commandline
server {
    listen 80;
    server_name ustb.campus.wobushidalao.top;
    location / {
        proxy_pass http://43.138.46.106;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
这样当访问 ``` ustb.campus.wobushidalao.top ``` 时就可以访问 ```43.138.46.106``` 上的资源了

## 3. 如何启动项目
### 3.1 使用nginx+uwsgi启动
这里顺便补充一下这个Podcaster的博客项目的部署方法

1. 在项目的根目录下新建 ```uwsgi.ini``` 的配置文件
2. 在 ```uwsgi.ini``` 文件中写入如下内容
```ini
[uwsgi]
# 与nginx进行通信的socket端口
socket = 127.0.0.1:9001
# 项目路径
chdir = /var/www/html/Podcaster
# wsgi文件路径，一般在主包下面
wsgi-file = Podcaster/wsgi.py
# 下面的进程、线程数可根据服务器的性能进行自行修改
processes = 4
workers = 4
threads = 4
# 下面的配置建议不要修改，使用默认的
master = True
enable-threads = True
pidfile = uwsgi.pid
daemonize = uwsgi.log
```
3. 使用如下的命令启动uwsgi服务
```commandline
sudo uwsgi --ini uwsgi.ini
```
使用如下的命令停止uwsgi服务
```commandline
sudo uwsgi --stop uwsgi.pid
```
4. nginx文件配置如下
```doctest

server {
    listen 80;
    server_name blog.wobushidalao.top;
        root /var/www/html/Podcaster;  
        location /static{ 
            alias /var/www/html/Podcaster/static;
        }
        location / {
            include /etc/nginx/uwsgi_params;
            uwsgi_pass localhost:9001;
        }
}
```
使用如下的命令重启nginx
```commandline
sudo service nginx reload
```
### 3.2 使用nginx+systemctl封装服务
可参考这篇博客： [Linux封装uwsgi服务【基于systemctl】](https://blog.csdn.net/V123456789987654/article/details/133133638)
1. 创建服务文件
```commandline
sudo vim /etc/systemd/system/podcaster.service
```
2. 在文件中写入如下内容
```doctest
[Unit]
Description=Podcaster Service
After=network.target
 
[Service]
User=root
WorkingDirectory=/var/www/html/Podcaster
ExecStart=uwsgi --ini uwsgi.ini
ExecStop=uwsgi --stop uwsgi.pid
ExecReload=uwsgi --reload uwsgi.pid
Type=forking
Restart=always
 
[Install]
WantedBy=multi-user.target
```
3. 保存后，如果我们想要启用服务，可以这么操作
```commandline
sudo systemctl enable podcaster
```
开启服务
```commandline
sudo systemctl start podcaster
```
停止服务
```commandline
sudo systemctl stop podcaster
```
重启服务
```commandline
sudo systemctl reload podcaster
```
注销服务
```commandline
sudo systemctl disable podcaster
```
## 4.获取帮助
```text
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @time: 2023/9/30 16:45
```