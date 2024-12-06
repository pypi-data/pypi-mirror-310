import os

from art import text2art
from loguru import logger
from .create import PluginCreator

# 使用指定字体和装饰生成UniBot PS的ASCII艺术
UniBotPSText2art = text2art("UniBot-PS", space=1)
print(UniBotPSText2art)


def access() -> None:
    print("UniBot-脚手架")
    creator = PluginCreator()

    name = input(f"插件名 ({creator.pluginInfo.name})# ")
    if name:
        creator.pluginInfo.name = name
        creator.pluginInfo.entry = name + ".py"

    entry = input(f"插件入口 ({creator.pluginInfo.entry})# ")
    if entry:
        creator.pluginInfo.entry = entry
    description = input(f"插件描述 ({creator.pluginInfo.description})# ")
    if description:
        creator.pluginInfo.description = description
    version = input(f"版本 ({creator.pluginInfo.version})# ")
    if version:
        creator.pluginInfo.version = version
    pluginDir = os.path.join(os.getcwd(), creator.pluginInfo.name)

    logger.info(f"开始创建: {pluginDir}")
    result = creator.create()

    if not result:
        logger.info(f"插件 {creator.pluginInfo.name} 创建失败！")
    else:
        logger.info(f"插件 {creator.pluginInfo.name} 创建成功！")