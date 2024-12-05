import nonebot_plugin_alconna
from PIL import Image
from PIL import ImageGrab
import json
import aiohttp
import base64
import time
import io
import re
import asyncio
import aiofiles
from datetime import datetime
import os
import traceback
import random
import ast

from argparse import Namespace

from ..config import config, redis_client, nickname
from ..config import __SUPPORTED_MESSAGEEVENT__, message_event_type
from .translation import translate
from ..backend import AIDRAW
from ..utils import unload_and_reload, pic_audit_standalone, aidraw_parser, run_later, txt_audit
from ..utils.load_balance import sd_LoadBalance, get_vram
from ..utils.prepocess import prepocess_tags
from .safe_method import send_forward_msg, risk_control
from ..aidraw import  send_msg_and_revoke, get_message_at, first_handler
from nonebot import on_shell_command, Bot
from nonebot.adapters import Event
from nonebot.params import CommandArg, Arg, ShellCommandArgs, Matcher, RegexGroup

from nonebot_plugin_alconna import UniMessage, CommandResult, AlconnaResult
from nonebot_plugin_alconna.uniseg import UniMsg
from nonebot import Bot

from nonebot.typing import T_State
from nonebot import logger
from collections import Counter
from copy import deepcopy
from typing import Any, Annotated, Union
from bs4 import BeautifulSoup

current_date = datetime.now().date()
day: str = str(int(datetime.combine(current_date, datetime.min.time()).timestamp()))

header = {
    "content-type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
}

control_net = on_shell_command(
    "以图绘图",
    aliases={"以图生图"},
    parser=aidraw_parser,
    priority=5,
    block=True
)


class SdAPI:

    def __init__(
            self,
            backend_sit: str = "",
            backend_index: int = None,
    ):
        self.backend_site = backend_sit
        self.backend_index = backend_index
        self.config = config
        self.reverse_dict = {value: key for key, value in config.novelai_backend_url_dict.items()}
        self.backend_site_list = config.backend_site_list
        self.backend_name_list = config.backend_name_list

    async def change_model(
            self,
            model_index,
    ):
        self.backend_site = list(config.novelai_backend_url_dict.values())[int(self.backend_index)]

        models_dict = await self.get_models_api(self.backend_index, True)

        data = models_dict[model_index]

        start_time = time.time()

        payload = {"sd_model_checkpoint": data}
        url = "http://" + self.backend_site + "/sdapi/v1/options"
        resp_ = await aiohttp_func("post", url, payload)

        code, end_time = resp_[1], time.time()
        spend_time = end_time - start_time
        spend_time_msg = f",更换模型共耗时{spend_time:.3f}秒"

        return data, spend_time_msg, code

    async def get_models_api(self, backend_index, return_models=False, vae=False):
        self.backend_site = self.config.backend_site_list[int(backend_index)]
        self.backend_index = backend_index
        endpoint = "sd-vae" if vae else "sd-models"
        options_endpoint = "sd_vae" if vae else "sd_model_checkpoint"
        dict_model = {}
        all_models_list = []
        message = []

        resp_ = await aiohttp_func("get", f"http://{self.backend_site}/sdapi/v1/options")
        current_model = resp_[0][options_endpoint]

        message.append(
            f"当前使用模型: {current_model}, 当前后端类型: {self.config.backend_type[self.backend_index]},\t\n\n"
        )

        models_info = await aiohttp_func("get", f"http://{self.backend_site}/sdapi/v1/{endpoint}")
        if models_info[1] == 404:
            models_info = await aiohttp_func("get", f"http://{self.backend_site}/sdapi/v1/sd-modules")

        for n, model_info in enumerate(models_info[0], 1):
            model_name = model_info['model_name'] if vae else model_info['title']
            dict_model[n] = model_name
            message.append(f"{n}. {model_name},\t\n")
            all_models_list.append(model_name)

        message.append(f"总计{n}个模型")

        if return_models:
            return dict_model

        file_path = "data/novelai/vae.json" if vae else "data/novelai/models.json"
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(dict_model, f, indent=4)

        return message

    @staticmethod
    async def super_res_api_func(
            img: str or bytes,
            size: int = 0,
            compress=True,
            upscale=2,
    ):
        '''
        sd超分extra API, size,1为
        '''

        img = img if isinstance(img, bytes) else base64.b64decode(img)
        msg = ""
        max_res = config.novelai_SuperRes_MaxPixels

        if size == 0:
            upscale = 2
        elif size == 1:
            upscale = 3
        ai_draw_instance = AIDRAW()

        if compress:
            new_img = Image.open(io.BytesIO(img)).convert("RGB")
            old_res = new_img.width * new_img.height
            width = new_img.width
            height = new_img.height

            if old_res > pow(max_res, 2):
                new_width, new_height = ai_draw_instance.shape_set(width, height, max_res)
                new_img = new_img.resize((round(new_width), round(new_height)))
                msg = f"原图已经自动压缩至{int(new_width)}*{int(new_height)}"
            else:
                msg = ''

            img_bytes = io.BytesIO()
            new_img.save(img_bytes, format="JPEG")
            img_bytes = img_bytes.getvalue()
        else:
            img_bytes = img

        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        payload = {"image": img_base64}
        payload.update(config.novelai_SuperRes_generate_payload)

        if upscale:
            payload["upscaling_resize"] = upscale

        fifo = AIDRAW()
        lb_resp = await sd_LoadBalance(fifo)
        backend_site = lb_resp[1][0]

        api_url = "http://" + backend_site + "/sdapi/v1/extra-single-image"
        resp_json, sc = await aiohttp_func("post", api_url, payload)

        if sc not in [200, 201]:
            return img_bytes, msg, sc, img_base64
        resp_img = resp_json["image"]
        bytes_img = base64.b64decode(resp_img)
        return bytes_img, msg, sc, resp_img

    @staticmethod
    async def get_qq_img_url(event):
        url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

        if isinstance(event, message_event_type[0]):
            url = re.findall(url_regex, str(event.get_message()))[0][:-1]

        elif isinstance(event, message_event_type[1]):

            reply = event.reply
            for seg in event.message['image']:
                url = seg.data["url"]
            at_id = await get_message_at(event.json())
            # 获取图片url
            if at_id:
                url = f"https://q1.qlogo.cn/g?b=qq&nk={at_id}&s=640"
            if reply:
                for seg in reply.message['image']:
                    url = seg.data["url"]

        return url


class CommandHandler(SdAPI):
    def __init__(self):
        super().__init__()

    async def get_sd_models(
        self,
        index: int,
        model,
        search
    ):

        is_vae = model == "vae"
        is_lora = model == "lora"
        is_emb = model == "emb"

        if model in {"ckpt", "vae"}:
            final_message = await self.get_models_api(index, False, is_vae)
        elif is_lora:
            final_message = (await get_and_process_lora(
                index=index,
                text_msg=search if isinstance(search, str) else None
            ))[1]
        elif is_emb:
            final_message = (await get_and_process_emb(
                index=index,
                text_msg=search if isinstance(search, str) else None
            ))[1]
        else:
            final_message = await self.get_models_api(index, False, False)

        logger.info(f"获取{model}模型")

        await risk_control(final_message, True, revoke_later=True)

    async def get_sd_prompt_style(self, index: int, search):

        filter_styles = []

        styles, sc = await aiohttp_func('get', f"http://{self.config.backend_site_list[index]}/sdapi/v1/prompt-styles")

        if sc not in [200, 201]:
            await UniMessage.text(f"获取预设失败，错误代码 {sc}").finish()

        if isinstance(search, str):
            for i in styles:
                if search in i["name"]:
                    filter_styles.append(i)
        else:
            filter_styles = styles

        resp_list = []
        for index, style in enumerate(filter_styles):
            resp_list.append(f"{index + 1}: {style['name']}: prompt: {style['prompt']}, negative_prompt: {style['negative_prompt']}\n")

        await risk_control('\n'.join(resp_list), False, revoke_later=True)

    async def change_sd_model(
            self,
            index: int,
            model_index: int
    ):
        self.backend_site = config.backend_name_list[index]
        self.backend_index = index

        await risk_control(
            f"收到指令，为后端 {self.backend_site} 更换模型中，后端索引-sd {index}，请等待,期间无法出图",
            False,
            reply_message=True,
            revoke_later=True
        )

        data, spend_time_msg, code = await self.change_model(model_index)

        if code in [200, 201]:

            await risk_control(
                f"更换模型 {data} 成功{spend_time_msg}",
                False,
                reply_message=True,
                revoke_later=True
            )

        else:

            await risk_control(
                f"更换模型失败，错误代码 {code}",
                False,
                reply_message=True,
                revoke_later=True
            )

    async def super_res(
            self, matcher: Matcher, url=None, msg=None
    ):

        img_url_list = []
        img_byte_list = []
        text_msg = ""
        upscale = 0

        if msg:
            if len(msg) > 1:
                for i in msg:
                    img_url_list.append(i.data["url"])
                    upscale = 0
            else:
                img_url_list.append(msg[0].data["url"])
                upscale = 1

            logger.info(f"总共{len(img_url_list)}张图片")

        if url:
            qq_img = await download_img(url)
            qq_img, text_msg, status_code, _ = await self.super_res_api_func(qq_img[1], upscale)
        else:
            for i in img_url_list:
                qq_img = await download_img(i)
                qq_img, text_msg, status_code, _ = await self.super_res_api_func(qq_img[1], upscale)

                if status_code not in [200, 201]:
                    await matcher.finish(f"出错了,错误代码{status_code},请检查服务器")

        img_byte_list.append(qq_img)

        if len(img_byte_list) == 1:
            await UniMessage.image(raw=img_byte_list[0]).send()
        else:
            uni_msg = UniMessage.text('')
            for i in img_byte_list:
                uni_msg += UniMessage.image(raw=i)

            await uni_msg.send()

    async def view_backend(self):
        n = -1
        backend_list = self.config.backend_name_list
        backend_site = self.config.backend_site_list
        message = []
        task_list = []
        fifo = AIDRAW()
        all_tuple = await fifo.load_balance_init()
        for i in backend_site:
            task_list.append(fifo.get_webui_config(i))
        resp_config = await asyncio.gather(*task_list, return_exceptions=True)
        resp_tuple = all_tuple[1][2]
        current_date = datetime.now().date()
        day: str = str(int(datetime.combine(current_date, datetime.min.time()).timestamp()))
        for i, m in zip(resp_tuple, resp_config):
            today_task = 0
            n += 1
            if isinstance(i, (aiohttp.ContentTypeError,
                              TypeError,
                              asyncio.exceptions.TimeoutError,
                              Exception)
                          ):
                message.append(f"{n + 1}.后端{backend_list[n]}掉线😭\t\n")
            else:
                if i[3] in [200, 201]:
                    text_message = ''
                    try:
                        model = m["sd_model_checkpoint"]
                    except:
                        model = ""
                    text_message += f"{n + 1}.后端{backend_list[n]}正常,\t\n模型:{os.path.basename(model)}\n"
                    if i[0]["progress"] in [0, 0.01, 0.0]:
                        text_message += f"后端空闲中\t\n"
                    else:
                        eta = i[0]["eta_relative"]
                        text_message += f"后端繁忙捏,还需要{eta:.2f}秒完成任务\t\n"
                    message.append(text_message)
                else:
                    message.append(f"{n + 1}.后端{backend_list[n]}掉线😭\t\n")

            today_task = 0
            if redis_client:
                r = redis_client[2]
                if r.exists(day):
                    today = r.get(day)
                    today = ast.literal_eval(today.decode("utf-8"))
                    today_task = today["gpu"][backend_list[n]]
            else:
                filename = "data/novelai/day_limit_data.json"
                if os.path.exists(filename):
                    async with aiofiles.open(filename, "r") as f:
                        json_ = await f.read()
                        json_ = json.loads(json_)
                    today_task = json_[day]["gpu"][backend_list[n]]
            message.append(f"今日此后端已画{today_task}张图\t\n")
            vram = await get_vram(backend_site[n])
            message.append(f"{vram}\t\n")

        await risk_control(message, revoke_later=True, md_temple=True)

    async def get_sampler(self):

        fifo = AIDRAW()

        lb_resp = await sd_LoadBalance(fifo)
        self.backend_site = lb_resp[1][0]

        sampler_list = []
        url = "http://" + self.backend_site + "/sdapi/v1/samplers"
        resp_ = await aiohttp_func("get", url)

        for i in resp_[0]:
            sampler = i["name"]
            sampler_list.append(f"{sampler}\t\n")

        await risk_control(sampler_list, md_temple=False)

    @staticmethod
    async def translate(
            msg: UniMsg
    ):

        txt_msg = msg.extract_plain_text()
        en = await translate(txt_msg, "en")
        resp = await txt_audit(en)
        if "yes" in resp:
            en = "1girl"

        await risk_control(message=[en,
                                    "自然语言模型根据发送者发送的文字生成以上内容，其生成内容的准确性和完整性无法保证，不代表本人的态度或观点."]
                           )

    @staticmethod
    async def random_tags(
            event: __SUPPORTED_MESSAGEEVENT__,
            bot: Bot,
            args: Namespace = ShellCommandArgs()
    ):

        chose_tags_list = await get_random_tags()
        resp = await txt_audit(
            str(chose_tags_list)
       )
        if "yes" in resp:
            chose_tags_list = ["1girl"]
        await risk_control([f"以下是为你随机的tag:\n{''.join(chose_tags_list)}"])

        args.tags = chose_tags_list
        args.match = True
        args.pure = True

        await first_handler(bot, event, args)

    @staticmethod
    async def find_image(
            event: __SUPPORTED_MESSAGEEVENT__,
            bot: Bot,
            matcher: Matcher,
            id_: str
    ):

        hash_id = id_.strip()
        directory_path = "data/novelai/output"
        filenames = await asyncio.get_event_loop().run_in_executor(None, get_all_filenames, directory_path)
        txt_file_name, img_file_name = f"{hash_id}.txt", f"{hash_id}.jpg"

        if txt_file_name in list(filenames.keys()):

            txt_content = await asyncio.get_event_loop().run_in_executor(
            None,
            extract_tags_from_file,
            filenames[txt_file_name]
            )

            img_file_path = filenames[img_file_name]
            img_file_path = img_file_path if os.path.exists(img_file_path) else filenames[f"{hash_id}.png"]

            async with aiofiles.open(img_file_path, "rb") as f:
                content = await f.read()

            resp = await txt_audit(str(txt_content))
            if 'yes' in resp:
                txt_content = ''

            msg_list = [f"这是你要找的{hash_id}的图\n", txt_content, UniMessage.image(raw=content)]
        else:
            await matcher.finish("你要找的图不存在")

        result = await pic_audit_standalone(content, return_none=True)

        if isinstance(event, message_event_type[1]):
            from nonebot.adapters.onebot.v11 import PrivateMessageEvent
            if isinstance(event, PrivateMessageEvent):
                await risk_control(msg_list)
                return

            if config.novelai_extra_pic_audit:
                if not result:
                    try:
                        await send_forward_msg(
                            bot,
                            event,
                            event.sender.nickname,
                            str(event.get_user_id()),
                            msg_list
                        )
                    except:
                        await risk_control(msg_list)
                else:
                    await bot.send(event, message="哼！想看涩图，自己看私聊去！")
                    try:
                        await bot.send_private_msg(
                            user_id=event.user_id,
                            message=f"悄悄给你看哦{await UniMessage.image(raw=content).export()}+AI绘图模型根据用户QQ{event.user_id}指令生成图片，可能会生成意料之外的内容，不代表本人观点或者态度"
                        )
                    except:
                        traceback.print_exc()
                        await bot.send(event, f"呜呜,{event.sender.nickname}你不加我好友我怎么发图图给你!")
            else:
                try:
                    await send_forward_msg(bot, event, event.sender.nickname, str(event.get_user_id()), msg_list)
                except:
                    await risk_control(msg_list)

        elif isinstance(event, message_event_type[0]):
            uni_msg = UniMessage.text('')
            for msg in msg_list:
                uni_msg += msg
            if result:
                await risk_control("检测到NSFW图片", reply_message=True, revoke_later=True)
            else:

                await send_msg_and_revoke(uni_msg)

    @staticmethod
    async def word_freq(
            matcher: Matcher
    ):
        pass
        # msg_list = []
        # if redis_client:
        #     r = redis_client[0]
        #     if r.exists("prompts"):
        #         word_list_str = []
        #         word_list = []
        #         byte_word_list = r.lrange("prompts", 0, -1)
        #         for byte_tag in byte_word_list:
        #             word_list.append(ast.literal_eval(byte_tag.decode("utf-8")))
        #         for list_ in word_list:
        #             word_list_str += list_
        #         word_list = word_list_str
        #     else:
        #         await matcher.finish("画几张图图再来统计吧!")
        # else:
        #     word_list = await asyncio.get_event_loop().run_in_executor(None, get_tags_list, False)
        #
        # def count_word_frequency(word_list):
        #     word_frequency = Counter(word_list)
        #     return word_frequency
        #
        # def sort_word_frequency(word_frequency):
        #     sorted_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
        #     return sorted_frequency
        #
        # word_frequency = count_word_frequency(word_list)
        # sorted_frequency = sort_word_frequency(word_frequency)
        # for word, frequency in sorted_frequency[0:240] if len(sorted_frequency) >= 240 else sorted_frequency:
        #     msg_list.append(f"prompt:{word},出现次数:{frequency}\t\n")
        #
        # await risk_control(msg_list)

    @staticmethod
    async def screen_shot(
            matcher: Matcher
    ):
        if config.run_screenshot:
            time_ = str(time.time())
            file_name = f"screenshot_{time_}.png"
            screenshot = ImageGrab.grab()
            screenshot.save(file_name)
            with open(file_name, "rb") as f:
                pic_content = f.read()
                bytes_img = io.BytesIO(pic_content)
            await UniMessage.image(raw=bytes_img).send()
            os.remove(file_name)
        else:
            await matcher.finish("未启动屏幕截图")

    @staticmethod
    async def audit(event: __SUPPORTED_MESSAGEEVENT__):
        url = ""
        reply = event.reply
        for seg in event.message['image']:
            url = seg.data["url"]
        if reply:
            for seg in reply.message['image']:
                url = seg.data["url"]
        if url:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    bytes = await resp.read()
            img_base64 = str(base64.b64encode(bytes), "utf-8")
            message = await pic_audit_standalone(img_base64)

            await risk_control(message, reply_message=True)

    @staticmethod
    async def one_more_generate(
            event: __SUPPORTED_MESSAGEEVENT__,
            bot: Bot,
            matcher: Matcher,
            args: Namespace = ShellCommandArgs()
    ):
        # 读取redis数据
        if redis_client:
            r = redis_client[0]
            if r.exists(str(event.get_user_id())):
                fifo_info = r.lindex(str(event.get_user_id()), -1)
                fifo_info = fifo_info.decode("utf-8")
                fifo_info = ast.literal_eval(fifo_info)
                del fifo_info["seed"]

                for key, value in fifo_info.items():
                    setattr(args, key, value)

                await first_handler(bot, event, args)
            else:
                await matcher.finish("你还没画过图, 这个功能用不了哦!")
        else:
            await matcher.finish("未连接redis, 此功能不可用")

    @staticmethod
    async def another_backend_control(
            matcher: Matcher,
            regex_group: Annotated[tuple[Any, ...], RegexGroup()],
    ):

            operation = regex_group[0]
            msg = regex_group[1]

            if operation == "刷新模型":
                post_end_point_list = ["/sdapi/v1/refresh-loras", "/sdapi/v1/refresh-checkpoints"]
                task_list = []
                for backend in config.backend_site_list:
                    for end_point in post_end_point_list:
                        backend_url = f"http://{backend}{end_point}"
                        task_list.append(aiohttp_func("post", backend_url, {}))
                _ = await asyncio.gather(*task_list, return_exceptions=False)
                await matcher.finish("为所有后端刷新模型成功...")

            elif operation == "卸载模型":
                if not msg:
                    await matcher.finish("你要释放哪个后端的显存捏?")
                if not msg.isdigit():
                    await matcher.finish("笨蛋!后端编号是数字啦!!")
                msg = int(msg)
                try:
                    await unload_and_reload(msg)
                except Exception:
                    logger.error(traceback.format_exc())
                else:
                    await matcher.finish(f"为后端{config.backend_name_list[msg]}重载成功啦!")

            elif operation == "终止生成":
                task_list = []
                extra_msg = ""
                if msg is not None:
                    if msg.isdigit():
                        backend = config.backend_site_list[int(msg)]
                        backend_url = f"http://{backend}/sdapi/v1/interrupt"
                        task_list.append(aiohttp_func("post", backend_url))
                        extra_msg = f"{msg}号后端"
                    else:
                        await matcher.finish("笨蛋!后端编号是数字啦!!")
                else:
                    extra_msg = "所有"
                    for backend in config.backend_site_list:
                        backend_url = f"http://{backend}/sdapi/v1/interrupt"
                        task_list.append(aiohttp_func("post", backend_url))
                _ = await asyncio.gather(*task_list, return_exceptions=False)
                await matcher.finish(f"终止{extra_msg}任务成功")

            elif operation == "获取脚本":
                script_index = None
                script_name = []

                if msg is not None:
                    if "_" in msg:
                        backend = config.backend_site_list[int(msg.split("_")[0])]
                        script_index = int(msg.split("_")[1])
                    else:
                        if msg.isdigit():
                            backend = config.backend_site_list[int(msg)]
                        else:
                            await matcher.finish("笨蛋!后端编号是数字啦!!")

                    backend_url = f"http://{backend}/sdapi/v1/script-info"
                    resp = await aiohttp_func("get", backend_url)
                    for script in resp[0]:
                        name = script["name"]
                        script_name.append(f"{name}\n")
                    if script_index:
                        select_script_args = resp[0][script_index]["args"]
                        print(select_script_args)
                        await risk_control(str(select_script_args))
                    await risk_control(script_name)

                else:
                    await matcher.finish(
                        "请按照以下格式获取脚本信息\n例如 获取脚本0 再使用 获取脚本0_2 查看具体脚本所需的参数")

    @staticmethod
    async def remove_bg(event, bot, msg, matcher: Matcher):
        img_url_list = []
        img_byte_list = []
        if len(msg) > 1:
            for i in msg:
                img_url_list.append(i.data["url"])
        else:
            img_url_list.append(msg[0].data["url"])

        for i in img_url_list:
            qq_img = await download_img(i)
            fifo = AIDRAW()
            await fifo.load_balance_init()
            payload = {
                "input_image": qq_img[0],
                "model": "isnet-anime",
                "alpha_matting": "true",
                "alpha_matting_foreground_threshold": 255,
                "alpha_matting_background_threshold": 50,
                "alpha_matting_erode_size": 20
            }
            resp_data, status_code = await aiohttp_func("post", f"http://{fifo.backend_site}/rembg", payload)
            if status_code not in [200, 201]:
                await matcher.finish(f"出错了,错误代码{status_code},请检查服务器")
            img_byte_list.append(base64.b64decode(resp_data["image"]))
        if len(img_byte_list) == 1:
            img_mes = UniMessage.image(raw=img_byte_list[0]).export()
            await bot.send(
                event=event,
                message=img_mes,
                at_sender=True,
                reply_message=True
            )
        else:
            img_list = []
            for i in img_byte_list:
                img_list.append(f"{UniMessage.image(raw=i).export()}")
            await send_forward_msg(
                bot,
                event,
                event.sender.nickname,
                event.get_user_id(),
                img_list
            )

    @staticmethod
    async def get_png_info(event, bot, matcher: Matcher):

        url = None

        reply = event.reply
        for seg in event.message['image']:
            url = seg.data["url"]
        if reply:
            for seg in reply.message['image']:
                url = seg.data["url"]

        if url:
            fifo = AIDRAW()
            await fifo.load_balance_init()
            img, _ = await download_img(url)
            payload = {
                "image": img
            }
            resp_data, status_code = await aiohttp_func(
                "post",
                f"http://{fifo.backend_site}/sdapi/v1/png-info",
                payload=payload
            )
            if status_code not in [200, 201]:
                await matcher.finish(f"出错了,错误代码{status_code},请检查服务器")
            info = resp_data["info"]
            if info == "":
                await matcher.finish("图片里面没有元数据信息欸\n是不是没有发送原图")

            else:
                parameters = ""
                resp = await txt_audit(str(info))
                if 'yes' in resp:
                    info = ''
                await risk_control([f"这是图片的元数据信息: {info}\n", f"参数: {parameters}"])

        else:
            await matcher.reject("请重新发送图片")

    @staticmethod
    async def random_pic(
            event: __SUPPORTED_MESSAGEEVENT__,
            bot: Bot,
            msg: UniMsg
    ):
        init_dict = {}
        if msg:
            tags = msg.extract_plain_text()
        else:
            tags = await get_random_tags(6)
            tags = ", ".join(tags)
            if not tags:
                tags = "miku"

        fifo = AIDRAW()

        init_dict["tags"] = tags
        _, __, normal_backend = await sd_LoadBalance(fifo)
        random_site = random.choice(normal_backend)
        index = config.backend_site_list.index(random_site)
        init_dict["backend_index"] = index

        args = aidraw_parser

        for key, value in init_dict.items():
            setattr(args, key, value)

        await risk_control(
            f"{nickname}祈祷中...让我们看看随机了什么好模型\n",
            reply_message=True,
            revoke_later=True
        )

        fifo = await first_handler(bot, event, args)

        await risk_control(
            f"主人~, 这是来自{fifo.backend_name}的{fifo.model}模型哦!\n" + f"\n后端索引是{fifo.backend_index}",
            reply_message=True,
            revoke_later=True
        )

    @staticmethod
    async def danbooru(bot: Bot, event: Event, tag: str, limit):

        db_base_url = "https://danbooru.donmai.us"

        if isinstance(limit, int):
            limit = limit

        else:
            limit = 3

        msg = tag
        resp = await aiohttp_func(
            "get",
            f"{db_base_url}/autocomplete?search%5Bquery%5D={msg}&search%5Btype%5D=tag_query&version=1&limit={limit}",
            text=True,
            proxy=True
        )

        soup = BeautifulSoup(resp[0], 'html.parser')
        tags = soup.find_all('li', class_='ui-menu-item')

        data_values = []
        raw_data_values = []
        for tag in tags:
            data_value = tag['data-autocomplete-value']
            raw_data_values.append(data_value)
            data_value_space = data_value.replace('_', ' ') 
            data_values.append(data_value_space)

        tag_image_url = {}
        build_msg = []

        for tag in raw_data_values:
            build_msg.append(f"({tag}:1)")
            tag = tag.replace(' ', '_').replace('(', '%28').replace(')', '%29')

            image_resp = await aiohttp_func(
                "get",
                f"{db_base_url}/posts?tags={tag}",
                text=True,
                proxy=True
            )

            soup = BeautifulSoup(image_resp[0], 'html.parser')
            img_urls = [img['src'] for img in soup.find_all('img') if img['src'].startswith('http')][:2]
            # post_links = [a['href'] for a in soup.find_all('a', class_='post-preview-link') if 'href' in a.attrs][:2]
            # for post in post_links:
            #     target_url = f"{db_base_url}{post}"
            # logger.error(post_links)

            async def process_image(image_url):
                base64_image, bytes_image = await download_img(image_url)
                if await pic_audit_standalone(base64_image, return_none=True):
                    return "太涩了"
                else:
                    unimsg = UniMessage.image(raw=bytes_image)
                    return await unimsg.export()

            async def process_images(img_urls):
                tasks = [process_image(url) for url in img_urls]
                results = await asyncio.gather(*tasks)
                return results

            results = await process_images(img_urls)
            build_msg.extend(results)

            tag_image_url[tag] = img_urls

        resp = await txt_audit(str(data_values))
        if 'yes' in resp:
            data_values = ['1girl']
            await risk_control('\n'.join(data_values), revoke_later=True, reply_message=True)
        else:
            await risk_control('\n'.join(data_values), revoke_later=True, reply_message=True)
            await send_forward_msg(bot, event, bot.self_id, event.get_user_id(), build_msg)

    @staticmethod
    async def set_config(
            matcher: Matcher,
            args: Namespace = ShellCommandArgs()
    ):
        msg_list = ["Stable-Diffusion-WebUI设置\ntips: 可以使用 -s 来搜索设置项, 例如 设置 -s model\n"]
        n = 0
        if args.backend_site is None and not isinstance(args.backend_site, int):
            await matcher.finish("请指定一个后端")
        else:
            site = config.backend_site_list[args.backend_site]
        get_config_site = "http://" + site + "/sdapi/v1/options"
        resp_dict = await aiohttp_func("get", get_config_site)
        index_list = list(resp_dict[0].keys())
        value_list = list(resp_dict[0].values())
        for i, v in zip(index_list, value_list):
            n += 1
            if args.search:
                pattern = re.compile(f".*{args.search}.*", re.IGNORECASE)
                if pattern.match(i):
                    msg_list.append(f"{n}.设置项: {i},设置值: {v}" + "\n")
            else:
                msg_list.append(f"{n}.设置项: {i},设置值: {v}" + "\n")
        if args.index is None and args.value == None:
            await risk_control(msg_list)
        elif args.index is None:
            await matcher.finish("你要设置啥啊!")
        elif args.value is None:
            await matcher.finish("你的设置值捏?")
        else:
            payload = {
                index_list[args.index - 1]: args.value
            }
            try:
                await aiohttp_func("post", get_config_site, payload)
            except Exception as e:
                await matcher.finish(f"出现错误,{str(e)}")
            else:
                await risk_control(f"设置完成{payload}")

    @staticmethod
    async def style(
            matcher: Matcher,
            args: Namespace = ShellCommandArgs()
    ):
        message_list = []
        style_dict = {}
        style_list = []
        if redis_client:
            r = redis_client[1]
            if r.exists("style"):
                style_list = r.lrange("style", 0, -1)
                decoded_styles = []

                for index, style in enumerate(style_list):
                    try:
                        decoded_style = style.decode("utf-8")
                        try:
                            parsed_style = ast.literal_eval(decoded_style)
                            decoded_styles.append(parsed_style)
                        except (ValueError, SyntaxError) as e:
                            pass

                    except (UnicodeDecodeError, AttributeError) as e:
                        pass

                style_list = decoded_styles

            if r.exists("user_style"):
                user_style_list = r.lrange("user_style", 0, -1)
                for index, style in enumerate(user_style_list):
                    try:
                        decoded_style = style.decode("utf-8")
                        style = ast.literal_eval(decoded_style)
                        style_list.append(style)
                    except (ValueError, SyntaxError, UnicodeDecodeError) as e:
                        pass

        else:
            await matcher.finish("需要redis以使用此功能")

        if args.delete:
            delete_name = args.delete[0] if isinstance(args.delete, list) else args.delete
            find_style = False
            style_index = -1
            for style in style_list:
                style_index += 1
                if style["name"] == delete_name:
                    pipe = r.pipeline()
                    r.lset("user_style", style_index, '__DELETED__')
                    r.lrem("user_style", style_index, '__DELETED__')
                    pipe.execute()
                    find_style = True
                    await matcher.finish(f"删除预设{delete_name}成功!")
            if not find_style:
                await matcher.finish(f"没有找到预设{delete_name},是不是打错了!\n另外不支持删除从webui中导入的预设")

        if args.find_style_name:
            matched_styles = UniMessage.text('')
            for style in style_list:
                if args.find_style_name.lower() in style["name"].lower():
                    name, tags, ntags = style["name"], style["prompt"], style["negative_prompt"]
                    matched_styles += f"预设名称: {name}\n\n正面提示词: {tags}\n\n负面提示词: {ntags}\n\n"

            if matched_styles:
                await risk_control(matched_styles)
            else:
                await matcher.finish(f"没有找到预设 {args.find_style_name}")

        if len(args.tags) != 0:
            if args.tags and args.style_name:
                tags = await prepocess_tags(args.tags, False)
                resp = await txt_audit(tags)
                if 'yes' in resp:
                    await matcher.finish(f"提示词涉及违规")
                ntags = "" if args.ntags is None else args.ntags
                style_dict["name"] = args.style_name
                style_dict["prompt"] = tags
                style_dict["negative_prompt"] = ntags
                r.rpush("user_style", str(style_dict))
                await matcher.finish(f"添加预设: {args.style_name}成功!")
            else:
                await matcher.finish("参数不完整, 请检查后重试")
        else:
            for style in style_list:
                name, tags, ntags = style["name"], style["prompt"], style["negative_prompt"]
                message_list.append(f"预设名称: {name}\n\n正面提示词: {tags}\n\n负面提示词: {ntags}\n\n")
            await risk_control(message_list)

    async def get_url(self, event: __SUPPORTED_MESSAGEEVENT__):
        url = await self.get_qq_img_url(event)
        await UniMessage.text(f"图片url是: {url}\n接下来可以用它来进行图片操作了").send()


async def get_random_tags(sample_num=12):
    try:
        if redis_client:
            r = redis_client[0]
            all_tags_list = []
            all_tags_list_str = [] 
            byte_tags_list = r.lrange("prompts", 0, -1)
            for byte_tag in byte_tags_list:
                all_tags_list.append(ast.literal_eval(byte_tag.decode("utf-8")))
            for list_ in all_tags_list:
                if list_ is not None:
                    all_tags_list_str += list_
            unique_strings = []
            for string in all_tags_list_str:
                if string not in unique_strings and string != "":
                    unique_strings.append(string)
            all_tags_list = unique_strings
        else:
            all_tags_list = await asyncio.get_event_loop().run_in_executor(None, get_tags_list)
        chose_tags_list = random.sample(all_tags_list, sample_num)
        return chose_tags_list
    except:
        logger.error(traceback.format_exc())
        return None


async def get_and_process_lora(site='', site_='', text_msg=None, index=None):

    if isinstance(index, int):
        site = config.backend_site_list[index]
        site_ = config.backend_name_list[index]

    loras_list = [f"这是来自webui:{site_}的lora,\t\n注使用例<lora:xxx:0.8>\t\n或者可以使用 -lora 数字索引 , 例如 -lora 1\n"]
    n = 0
    lora_dict = {}
    get_lora_site = "http://" + site + "/sdapi/v1/loras"
    resp_json = await aiohttp_func("get", get_lora_site)
    for item in resp_json[0]:
        i = item["name"]
        n += 1
        lora_dict[n] = i
        if text_msg:
            pattern = re.compile(f".*{text_msg}.*", re.IGNORECASE)
            if pattern.match(i):
                loras_list.append(f"{n}.{i}\t\n")
        else:
            loras_list.append(f"{n}.{i}\t\n")
    new_lora_dict = deepcopy(lora_dict)
    if redis_client:
        r2 = redis_client[1]
        if r2.exists("lora"):
            lora_dict_org = r2.get("lora")
            lora_dict_org = ast.literal_eval(lora_dict_org.decode("utf-8"))
            lora_dict = lora_dict_org[site_]
            lora_dict_org[site_] = lora_dict
            r2.set("lora", str(lora_dict_org))
    else:
        async with aiofiles.open("data/novelai/loras.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(lora_dict))
    return new_lora_dict, loras_list


async def get_and_process_emb(site='', site_='', text_msg=None, index=None):

    if isinstance(index, int):
        site = config.backend_site_list[index]
        site_ = config.backend_name_list[index]

    embs_list = [f"这是来自webui:{site_}的embeddings,\t\n注:直接把emb加到tags里即可使用\t\n中文emb可以使用 -nt 来排除, 例如 -nt 雕雕\n"]
    n = 0
    emb_dict = {}
    get_emb_site = "http://" + site + "/sdapi/v1/embeddings"
    resp_json = await aiohttp_func("get", get_emb_site)
    all_embs = list(resp_json[0]["loaded"].keys())
    for i in all_embs:
        n += 1
        emb_dict[n] = i
        if text_msg:
            pattern = re.compile(f".*{text_msg}.*", re.IGNORECASE)
            if pattern.match(i):
                embs_list.append(f"{n}.{i}\t\n")
        else:
            embs_list.append(f"{n}.{i}\t\n")
    new_emb_dict = deepcopy(emb_dict)
    if redis_client:
        r2 = redis_client[1]
        emb_dict_org = r2.get("emb")
        emb_dict_org = ast.literal_eval(emb_dict_org.decode("utf-8"))
        emb_dict = emb_dict_org[site_]
        emb_dict_org[site_] = emb_dict
        r2.set("emb", str(emb_dict_org))
    else:
        async with aiofiles.open("data/novelai/embs.json", "w", encoding="utf-8") as f:
            await f.write(json.dumps(emb_dict))
    return new_emb_dict, embs_list 


async def download_img(url, proxy=False):
    url = url.replace("gchat.qpic.cn", "multimedia.nt.qq.com.cn")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=config.proxy_site if proxy else None) as resp:
            img_bytes = await resp.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            return img_base64, img_bytes


def extract_tags_from_file(file_path, get_full_content=True) -> str:
    separators = ['，', '。', ","]
    separator_pattern = '|'.join(map(re.escape, separators))
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        if get_full_content:
            return content
    lines = content.split('\n')  # 将内容按行分割成列表
    words = []
    for line in lines:
        if line.startswith('tags='):
            tags_list_ = line.split('tags=')[1].strip()
            words = re.split(separator_pattern, tags_list_.strip())
            words = [re.sub(r'\s+', ' ', word.strip()) for word in words if word.strip()]
            words += words
    return words


def get_tags_list(is_uni=True):
    filenames = get_all_filenames("data/novelai/output", ".txt")
    all_tags_list = []
    for path in list(filenames.values()):
        tags_list = extract_tags_from_file(path, False)
        for tags in tags_list:
            all_tags_list.append(tags)
    if is_uni:
        unique_strings = []
        for string in all_tags_list:
            if string not in unique_strings and string != "":
                unique_strings.append(string)
        return unique_strings
    else:
        return all_tags_list


def get_all_filenames(directory, fileType=None) -> dict:
    file_path_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fileType and not file.endswith(fileType):
                continue
            filepath = os.path.join(root, file)
            file_path_dict[file] = filepath
    return file_path_dict


async def aiohttp_func(way, url, payload={}, text=False, proxy=False):
    try:
        if way == "post":
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1800)) as session:
                async with session.post(
                        url=url,
                        json=payload,
                        proxy=config.proxy_site if proxy else None
                ) as resp:
                    if resp.status in [200, 201]:
                        if text:
                            return await resp.text(), resp.status
                        resp_data = await resp.json()
                        return resp_data, resp.status
                    else:
                        logger.warning(f"http post请求失败，状态码为{resp.status}，返回内容为{await resp.text()}")
                        return None, resp.status
        else:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1800)) as session:
                async with session.get(
                        url=url,
                        proxy=config.proxy_site if proxy else None
                ) as resp:
                    if resp.status in [200, 201]:
                        if text:
                            return await resp.text(), resp.status
                        resp_data = await resp.json()
                        return resp_data, resp.status
                    else:
                        logger.warning(f"http get请求失败，状态码为{resp.status}，返回内容为{await resp.text()}")
                        return None, resp.status
    except Exception:
        traceback.print_exc()
        return None




#
# @control_net_list.handle()
# async def _(event: MessageEvent, bot: __SUPPORTED_BOT__, msg: __SUPPORTED_MESSAGE__ = CommandArg()):
#     await func_init(event)
#     message_model = "可用的controlnet模型\t\n"
#     message_module = "可用的controlnet模块\t\n"
#     if msg:
#         if msg[0].type == "image":
#             img_url = msg[0].data["url"]
#             img_tuple = await download_img(img_url)
#             base64_img = img_tuple[0]
#             payload = {"controlnet_input_images": [base64_img]}
#             config.novelai_cndm.update(payload)
#             resp_ = await aiohttp_func("post", "http://" + site + "/controlnet/detect", config.novelai_cndm)
#             if resp_[1] == 404:
#                 await control_net_list.finish("出错了, 是不是没有安装controlnet插件捏?")
#             image = resp_[0]["images"][0]
#             image = base64.b64decode(image)
#             await control_net_list.finish(message=MessageSegment.image(image))
#
#     resp_1 = await aiohttp_func("get", "http://" + site + "/controlnet/model_list")
#     resp_2 = await aiohttp_func("get", "http://" + site + "/controlnet/module_list")
#     if resp_1[1] == 404:
#         await control_net_list.finish("出错了, 是不是没有安装controlnet插件捏?")
#     if resp_2[1] == 404:
#         model_list = resp_1[0]["model_list"]
#         for a in model_list:
#             message_model += f"{a}\t\n"
#         await bot.send(event=event, message=message_model)
#         await control_net_list.finish("获取control模块失败, 可能是controlnet版本太老, 不支持获取模块列表捏")
#     model_list = resp_1[0]["model_list"]
#     module_list = resp_2[0]["module_list"]
#     module_list = "\n".join(module_list)
#     await risk_control(bot, event, model_list+[module_list], True)

#

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
llm_caption = on_command("llm", aliases={"图片分析"})


@llm_caption.handle()
async def __(state: T_State, png: Message = CommandArg()):
    if png:
        state['png'] = png
    pass


@llm_caption.got("png", "请发送你要分析的图片,请注意")
async def __(event: __SUPPORTED_MESSAGEEVENT__):
    reply = event.reply
    for seg in event.message['image']:
        url = seg.data["url"]
    if reply:
        for seg in reply.message['image']:
            url = seg.data["url"]
    if url:
        img, _ = await download_img(url)
        payload = {
            "image": img,
            "threshold": 0.3
        }
        resp_data, status_code = await aiohttp_func("post", f"http://{config.novelai_tagger_site}/llm/caption", payload)
        if status_code not in [200, 201]:
            await llm_caption.finish(f"出错了,错误代码{status_code},请检查服务器")
        await risk_control([f"llm打标{resp_data['llm']}"])
    else:
        await llm_caption.reject("请重新发送图片")