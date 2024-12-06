import json
import os.path
from typing import Union
from loguru import logger
from UniBotPluginsCaffold.types import PluginInformation, PluginInformationUtil


class ManifestJsonUtil:
    @staticmethod
    def createManifestJson(output: Union[os.PathLike, str], pluginInfo: PluginInformation) -> bool:
        writeData = PluginInformationUtil.from_dict(pluginInfo)
        try:
            with open(os.path.join(output, 'manifest.json'), 'w', encoding='utf-8') as f:
                f.write(json.dumps(writeData, indent=4))
                return True
        except Exception as e:
            logger.error(e)
        return False
