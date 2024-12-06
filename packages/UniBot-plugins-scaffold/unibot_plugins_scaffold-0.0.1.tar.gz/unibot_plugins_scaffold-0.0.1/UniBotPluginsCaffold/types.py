from typing import List


class PluginType:
    python: str = "script-python"


class PluginInformation:
    name: str
    entry: str
    type: str
    version: str
    description: str
    preload: List[str]
    passive: bool = False
    dependence: List[str]
    optional_dependence: List[str]


class PluginInformationUtil:
    @staticmethod
    def from_dict(pluginInfo: PluginInformation):
        return {
            "name": pluginInfo.name,
            "entry": pluginInfo.entry,
            "type": pluginInfo.type,
            "version": pluginInfo.version,
            "description": pluginInfo.description,
            "preload": pluginInfo.preload,
            "passive": pluginInfo.passive,
            "dependence": pluginInfo.dependence,
            "optional_dependence": pluginInfo.optional_dependence,
        }

