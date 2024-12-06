import os
from loguru import logger
from UniBotPluginsCaffold.types import PluginInformation, PluginType
from UniBotPluginsCaffold.templates.main import MainPyFileUtil
from UniBotPluginsCaffold.templates.manifestJson import ManifestJsonUtil


class PluginCreator:
    def __init__(self) -> None:
        """
        插件创建器
        """
        self.pluginInfo = PluginInformation
        self.pluginInfo.name = "PluginName"
        self.pluginInfo.entry = self.pluginInfo.name + ".py"
        self.pluginInfo.type = PluginType.python
        self.pluginInfo.version = "v0.0.1"
        self.pluginInfo.description = "A QQ bot plugin."
        self.pluginInfo.preload = []
        self.pluginInfo.dependence = []
        self.pluginInfo.optional_dependence = []

    def create(self, output: os.PathLike = os.getcwd()) -> bool:
        """
        开始创建 / Start creating.
        :param output: 输出路径
        :return: bool
        """
        output = os.path.join(output, self.pluginInfo.name)
        # 创建plugin的目录
        if not os.path.isdir(output):
            logger.info(f"路径：{output}不存在，将自动创建...")
            try:
                os.makedirs(output)
            except OSError as e:
                logger.warning(e)
                return False
            except Exception as e:
                logger.error(e)
                return False

        # 创建 entry
        createEntryResult = MainPyFileUtil.create(output, self.pluginInfo)
        if not createEntryResult:
            logger.error("entry文件创建失败！")
            return False
        # 创建 manifest.json 文件
        createManifestJson = ManifestJsonUtil.createManifestJson(output, self.pluginInfo)
        if not createManifestJson:
            logger.error("manifest.json文件创建失败！")
            return False

        return True
