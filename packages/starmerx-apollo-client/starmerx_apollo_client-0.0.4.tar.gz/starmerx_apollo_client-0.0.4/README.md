#Starmerx Apollo Client


##项目介绍

本项目是Apollo的Client端, 用来获取Apollo配置。
本项目采用长连接, 保持心跳并从ApolloConfig获取配置
获取配置后, 会备份一本在本地磁盘, 和缓存(不是正经缓存, 就是一个类变量)
配置读取顺序:
1. 缓存
2. 网络请求
3. 本地配置


##使用介绍

使用时建议采用单例模式, 全局使用一个实例, Demo如下:

from starmerx_apollo_client.apollo_client import ApolloClient
from utils.env import env

CONFIG_URL = env.get_value('APOLLO_CONFIG_URL', default='')
APP_ID = env.get_value('APOLLO_APP_ID', default='')
APP_SECRET = env.get_value('APOLLO_APP_SECRET', default='')

a_client = ApolloClient(app_id=APP_ID, secret=APP_SECRET, config_url=CONFIG_URL)


##遗留问题

暂只支持python3
长链接那里目前使用没有问题, 后续需要跟进
