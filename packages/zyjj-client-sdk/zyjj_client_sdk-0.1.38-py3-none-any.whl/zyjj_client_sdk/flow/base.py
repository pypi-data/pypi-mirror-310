import io
import json
import logging
from enum import Enum

import numpy as np
from PIL import Image

from zyjj_client_sdk.base.tool import subtitles2srt, async_batch_run, llm_json_parse

from zyjj_client_sdk.base import Base, ApiService, MqttServer, MqttEventType, CloudSourceType
from zyjj_client_sdk.base.entity import TaskInfo
from zyjj_client_sdk.lib import FFMpegService, OSSService
from dataclasses import dataclass
from typing import Callable, Optional, Any
import chardet


class NodeType(Enum):
    BasicStart = 'basic_start'
    BasicEnd = 'basic_end'
    BasicCode = 'basic_code'
    BasicObjectImport = 'basic_object_import'
    BasicObjectExport = 'basic_object_export'
    ToolGetConfig = 'tool_get_config'
    ToolCostPoint = 'tool_cost_point'
    ToolCheckPoint = 'tool_check_point'
    ToolUploadFile = 'tool_upload_file'
    ToolDownloadFile = 'tool_download_file'
    ToolFileParse = 'tool_file_parse'
    ToolFileExport = 'tool_file_export'
    ToolGetTencentToken = 'tool_get_tencent_token'
    ToolGenerateLocalPath = 'tool_generate_local_path'
    ToolFfmpegPoint = 'tool_ffmpeg_point'
    ToolFfmpeg = 'tool_ffmpeg'
    ToolLinkExtra = 'tool_link_extra'


# 节点
@dataclass
class FlowNode:
    node_id: str
    node_type: NodeType
    data: str


@dataclass
class FlowRelation:
    from_id: str
    from_output: str
    to_id: str
    to_input: str


@dataclass
class NodeInfo:
    node_id: str = ''
    node_type: str = ''  # 节点类型
    data: str = ''  # 节点的额外参数
    cost: int = 0  # 执行耗时
    status: int = 0  # 执行状态
    msg: str = ''  # 错误信息


# 给flow节点提供的基本方法
class FlowBase:
    def __init__(
        self,
        base: Base,  # 基本信息
        api: ApiService,  # api服务
        mqtt: MqttServer,  # mqtt服务
        oss: OSSService,  # oss 服务
        global_data: dict,  # 全局数据
        task_info: TaskInfo,  # 任务数据
    ):
        # 一些私有变量，不暴露
        self.__base = base
        self.__ffmpeg = FFMpegService()
        self.__mqtt = mqtt
        self.__global_data = global_data
        self.__task_info = task_info
        self.__node_current: FlowNode | None = None
        self.__node_pre: list[FlowRelation] = []
        self.__node_next: list[FlowRelation] = []
        # 节点的描述信息
        self.__node_desc = {}
        self.__node_log = {}
        # 可以被外部模块使用的变量
        self.api = api
        self.uid = task_info.uid
        self.task_id = task_info.task_id
        self.source = task_info.source
        self.oss = oss

    # 添加节点描述
    def add_desc(self, desc: str):
        if self.__node_current is not None:
            self.__node_desc[self.__node_current.node_id] = desc

    # 获取节点描述
    def get_desc(self) -> dict:
        return self.__node_desc

    # 添加节点日志
    def add_log(self, *args):
        if self.__node_current is None:
            return
        node_id = self.__node_current.node_id
        if node_id not in self.__node_log:
            self.__node_log[node_id] = []
        self.__node_log[self.__node_current.node_id] += [str(arg) for arg in args]

    def get_log(self) -> dict:
        return self.__node_log

    # 获取全局数据
    def get_global(self, key: str, default: Callable[[], Any] = lambda: None):
        data = self.__global_data.get(key)
        if data is None:
            logging.info('init from default')
            data = default()
            if data is not None:
                self.__global_data[key] = data
        return data

    # 设置全局数据
    def set_global(self, key: str, value: Any):
        self.__global_data[key] = value

    # 设置当前节点的关联关系
    def set_flow_relation(self, node: FlowNode, prev: list[FlowRelation], after: list[FlowRelation]):
        self.__node_current = node
        self.__node_pre = prev
        self.__node_next = after

    # 获取输入
    def input_get(self) -> dict:
        return self.__task_info.input

    # 获取当前节点需要哪些输出字段
    def node_output_need(self) -> list[str]:
        return [relation.from_output for relation in self.__node_next]

    # 上传文件
    def oss_upload_file(self, path: str, source=1):
        return self.oss.upload_file(self.uid, path, CloudSourceType(source))

    # 上传文件并获取url
    def oss_upload_file_get_url(self, path: str, source=1):
        path = self.oss.upload_file(self.uid, path, CloudSourceType(source))
        return self.oss.get_url(path, CloudSourceType(source))

    # 生成一个本地路径
    def tool_generate_local_path(self, ext: str) -> str:
        return self.__base.generate_local_file(ext)

    # 获取二进制的编码信息
    @staticmethod
    def tool_get_bytes_encode(data: bytes) -> str:
        return chardet.detect(data)['encoding']
        # {'encoding': 'windows-1251', 'confidence': 0.99, 'language': 'Russian'}

    # 字幕格式转srt
    @staticmethod
    def subtitles2srt(subtitles: list) -> bytes:
        return subtitles2srt(subtitles)

    # 异步批量执行任务
    @staticmethod
    def async_batch_run(**kwargs) -> list:
        return async_batch_run(**kwargs)

    # 获取文件时长
    def ffmpeg_get_duration(self, path: str) -> float:
        return self.__ffmpeg.get_duration(path)

    # 执行ffmpeg任务
    def ffmpeg_execute(self, cmd: str) -> str:
        return self.__ffmpeg.ffmpeg_run(cmd)

    # ffmpeg压缩图片
    def ffmpeg_compress_image(self, img_file: str, quality: int = 5, max_width: int = 1920) -> bytes:
        out = self.tool_generate_local_path('jpg')
        cmd = f"-i {img_file} -q {quality} -vf \"scale='if(gt(iw,{max_width}),{max_width},iw)':'if(gt(ih*{max_width}/iw,ih),ih,ih*{max_width}/iw)'\" {out}"
        self.add_log("cmd", cmd)
        self.ffmpeg_execute(cmd)
        with open(out, "rb") as f:
            return f.read()

    # 触发代码节点
    def tiger_code(self, func_id: str, _input: dict, base=None) -> dict:
        # 获取代码信息
        info = self.api.get_entity_info(func_id)
        code_info = json.loads(info["data"])
        logging.info(f"execute code {code_info}")
        self.add_desc(info['name'])
        tmp = {
            "inputs": [_input[unique] if unique in _input else None for unique in code_info["inputs"]],
            "base": base,
            "func_call": lambda _id, inputs: self.tiger_code(_id, inputs, base)
        }
        exec(f"{code_info['code']}\noutput = handle(*inputs)", tmp)
        out = tmp['output']
        if not isinstance(out, tuple):
            out = (out,)
        output = {}
        for idx, unique in enumerate(code_info["outputs"]):
            output[unique] = out[idx]
        return output

    # mqtt 更新进度
    def mqtt_update_progress(self, progress: float):
        self.__mqtt.send_task_event(self.uid, self.task_id, MqttEventType.Progress, progress)

    # mqtt详情新增
    def mqtt_detail_append(self, data: dict):
        self.__mqtt.send_task_event(self.uid, self.task_id, MqttEventType.DetailAppend, data)

    # 获取prompt
    def entity_get_prompt(self, entity_id: str) -> str:
        return self.api.get_entity_data(entity_id)["prompt"]

    # 字节转Image
    @staticmethod
    def bytes2image(data: bytes) -> Image:
        return Image.open(io.BytesIO(data))

    # 字节转np.array
    def bytes2np(self, data: bytes) -> np.ndarray:
        return np.array(self.bytes2image(data))

    # Image转字节
    @staticmethod
    def image2bytes(img: Image, _format='PNG') -> bytes:
        image_bytes = io.BytesIO()
        img.save(image_bytes, format=_format)
        return image_bytes.getvalue()

    # np.array转字节
    def np2bytes(self, data: np.ndarray, _format='PNG') -> bytes:
        return self.image2bytes(Image.fromarray(data), _format)

    # 知识库查询
    def doc_query(self, query: str, tag: str = 'help', size: int = 1):
        return self.api.doc_query(query, tag, size)

    # 大语言模型解析
    @staticmethod
    def json_parse(data: str) -> dict:
        return llm_json_parse(data)

    # 图片检索
    def img_query(self, embedding: list[float], tag: str, size: int = 1) -> list:
        return self.api.img_query(embedding, tag, size)


# 处理节点定义
node_define = Callable[[FlowBase, dict, Optional[dict]], dict]
