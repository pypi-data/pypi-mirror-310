import os
from typing import Union
from loguru import logger
from UniBotPluginsCaffold.types import PluginInformation

MainPy = """from KobeBryantAPI import Logger

logger = Logger()


def on_enable():
    logger.info(f"{PLUGIN_NAME} on enable.")


def on_disable():
    logger.info(f"{PLUGIN_NAME} on disable.")
"""


class MainPyFileUtil:
    @staticmethod
    def templateFile(pluginInfo: PluginInformation) -> str:
        """
        读取模版文件
        :type pluginInfo: PluginInformation 插件信息
        :return: str
        """
        result = MainPy.split("\n")
        result[3] = f'PLUGIN_NAME = "{pluginInfo.name}"\n'
        result[3] += f'PLUGIN_DESCRIPTION = "{pluginInfo.description}"\n'
        result[3] += f'PLUGIN_VERSION = "{pluginInfo.version}"\n'
        return "\n".join(result)

    @staticmethod
    def create(output: Union[os.PathLike, str], pluginInfo: PluginInformation) -> bool:
        """
        创建 main.py 文件
        :param output: 输出路径
        :param pluginInfo: 插件信息
        :return: bool
        """
        try:
            with open(os.path.join(output, pluginInfo.entry), "w", encoding="utf-8") as f:
                f.write(MainPyFileUtil.templateFile(pluginInfo))
                return True
        except Exception as e:
            logger.error(e)
        return False
