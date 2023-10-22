# README
借助于Scrapy、Scrapyd、ScrapydWeb 实现的爬虫项目，用于定时抓取股票相关的数据，并借助于Docker进行部署。

特别注意，以下几个包含密码的配置文件不允许提交到代码仓库：
- 1、config.ini 包含了数据库地址、用户名、密码等信息
- 2、scrapydweb_settings_v10.py 包含了scrapydweb的配置信息，如登录用的用户名、密码
- 3、scrapy.cfg spider deploy时的敏感信息
- 4、scrapyd.conf 包含了scrapyd的配置信息，如登录用的用户名、密码

以下为本项目经常用到的命令。

## 项目本身
- 0、创建项目：```scrapy startproject projectname```
- 1、生成依赖项清单——将当前项目的依赖项输出到指定文件：```pip freeze > requirements.txt```
- 2、读取依赖项清单——按照指定文件安装需要的项目依赖项：```pip install -r requirements.txt```
- 3、执行爬虫程序：```scrapy crawl/runspider spider_name```
- 4、执行爬虫程序并将结果输入到指定文件：```scrapy crawl/runspider spider_name -o scraped_data.jl```

## Docker 相关
- 0、构建镜像：```docker build -t kaipanla:v0.6 .```
- 1、运行容器：```docker run -d -i -p 6800:6800 -p 5000:5000 imageID```
- 2、导出镜像：```docker save -o image.tar imageID```
- 3、倒入镜像：```docker load -i image.tar```
- 4、查看容器：```docker ps```
- 5、停止容器：```docker stop containerID```
- 6、删除容器：```docker rm -f containerID```
- 7、查看镜像：```docker images```
- 8、删除镜像：```docker rmi imageID```
- 9、给镜像打标签：```docker tag SOURCE_IMAGE[:TAG]/imageID  TARGET_IMAGE[:TAG] ```
- 10、在Docker内安装Python包：```docker exec -it 91062cbf0618 pip install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com ```
- 11、拷贝文件到Docker内部：```sudo docker cp config.ini containerID:/targetDir ```

## 打包模块scrapy-client
- 1、下载打包模块：```pip install scrapy-client```
- 2、修改配置文件scrapy.cfg:
  ```
    [settings]
    default = xxx.settings
    [deploy:vm1]
    url = http://xx.xx.xx.xx:6800/
    project = xxx
  ```
  3、打包给scrapyd服务：```scrapyd-deploy vm1 -p xxx ```