from . import config, manage
from .aidraw import AIDRAW
from nonebot.plugin import PluginMetadata
from .extension.deepdanbooru import deepdanbooru
from .amusement import today_girl, chatgpt_tagger, vits
from .extension import sd_extra_api_func, aidraw_help, civitai, sd_on_command


__plugin_meta__ = PluginMetadata(
    name="AI绘图",
    description="调用stable-diffusion进行AI绘图",
    usage=f"发送 绘画帮助 获取更多帮助\n基础用法:\n.aidraw[指令] [空格] loli,[参数]\n示例:.aidraw loli,cute,kawaii,\n项目地址:https://github.com/DiaoDaiaChan/nonebot-plugin-stable-diffusion-diao",
    type='application',
    homepage='https://github.com/DiaoDaiaChan/nonebot-plugin-stable-diffusion-diao',
    supported_adapters={"nonebot.adapters.qq", "nonebot.adapters.onebot.v11"}
)
__all__ = ["AIDRAW", "__plugin_meta__"]
