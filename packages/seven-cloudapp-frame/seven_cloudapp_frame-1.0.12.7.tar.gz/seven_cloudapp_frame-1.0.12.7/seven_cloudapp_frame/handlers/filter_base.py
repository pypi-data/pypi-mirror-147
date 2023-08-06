# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-04-24 15:15:19
@LastEditTime: 2022-04-24 15:16:44
@LastEditors: HuangJianYi
@Description: 
"""

from seven_framework.web_tornado.base_handler.base_api_handler import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from urllib.parse import parse_qs


def filter_check_params(must_params=None):
    """
    :description: 参数过滤装饰器 仅限handler使用,
                  提供参数的检查及获取参数功能
                  装饰器使用方法:
                  @client_filter_check_params("param_a,param_b,param_c")  或
                  @client_filter_check_params(["param_a","param_b,param_c"])
                  参数获取方法:
                  self.request_params[param_key]
    :param must_params: 必须传递的参数集合
    :last_editors: HuangJianYi
    """
    def check_params(handler):
        def wrapper(self, **args):
            finally_must_params = must_params
            if hasattr(self, "must_params"):
                finally_must_params = self.must_params
            if type(finally_must_params) == str:
                must_array = finally_must_params.split(",")
            if type(finally_must_params) == list:
                must_array = finally_must_params

            if finally_must_params:
                for must_param in must_array:
                    if not must_param in self.request_params or self.request_params[must_param] == "":
                        self.response_json_error("param_error", "参数错误,缺少必传参数")
                        return

            return handler(self, **args)

        return wrapper

    return check_params


def filter_check_request(check_params=None):
    """
    :description: 请求过滤装饰器 仅限handler使用,
                    提供单用户是否存在对某一接口的达到指定请求数的持续请求的校验
                    装饰器使用方法:
                    @client_filter_check_params("param_a,param_b,param_c")  或
                    @client_filter_check_params(["param_a","param_b,param_c"])
    :param check_params: 校验参数集合
    :last_editors: HuangJianYi
    """
    def check_request(handler):
        def wrapper(self, **args):
            object_id = self.get_open_id()
            if not object_id:
                object_id = self.get_user_id()

            if self.request_params and object_id:

                app_id = self.get_app_id()
                if not app_id:
                    app_id = self.get_source_app_id()

                finally_check_params = []
                if type(check_params) == str:
                    finally_check_params = check_params.split(",")
                if type(check_params) == list:
                    finally_check_params = check_params
                if finally_check_params:
                    sign_params = {key: self.request_params[key] for key in self.request_params if key in finally_check_params}
                else:
                    sign_params = self.request_params
                redis_init = SevenHelper.redis_init()
                middle_key = f"{self.__class__.__name__}_{app_id}_{object_id}_{self.get_signature_md5(sign_params)}"
                if redis_init.get(f"check_request_limit:{middle_key}"):
                    self.response_json_error("request_error", "请求频繁,请稍后再试")
                    return
                cache_key = f"check_request_count:{middle_key}_{str(SevenHelper.get_now_int(fmt='%Y%m%d%H%M'))}"
                cache_value = redis_init.get(cache_key)
                if cache_value:
                    cache_value = int(cache_value)
                    if cache_value >= 30:
                        redis_init.set(f"check_request_limit:{middle_key}", 1, 60)
                        self.response_json_error("request_error", "请求频繁,请稍后再试")
                        return
                redis_init.incr(cache_key, 1)
                redis_init.expire(cache_key, 120)

            return handler(self, **args)

        return wrapper

    return check_request


def filter_check_head_sign(is_check=True, no_check_params=None):
    """
    :description: 头部过滤装饰器 仅限handler使用
    :param is_check: 是否开启校验
    :param no_check_params: 不加入参数校验的参数集合
    :last_editors: HuangJianYi
    """
    def check_head(handler):
        def wrapper(self, **args):
            encrypt_key = config.get_value("encrypt_key", "r8C1JpyAXxrFV26V")
            is_check_head = config.get_value("is_check_head", False)
            if is_check_head == False:
                is_check = False
            else:
                is_check = True
            if is_check == True:
                try:
                    if type(no_check_params) == str:
                        no_check_array = no_check_params.split(",")
                    elif type(no_check_params) == list:
                        no_check_array = no_check_params
                    else:
                        no_check_array = []
                    # 验证是否有设备信息
                    clientheaderinfo_string = self.request.headers._dict.get("Clientheaderinfo")
                    if clientheaderinfo_string:
                        # 将设备信息字符串转为字典类型
                        device_info_dict = self.device_info_dict(clientheaderinfo_string)
                        # 验证签名超时 10分钟过期
                        now_time = TimeHelper.get_now_timestamp(True)
                        if now_time - device_info_dict["timestamp"] > int(1000 * 60 * 10):
                            return self.response_json_error("timestamp", "超时操作")
                        # 验证是否有头部信息签名
                        if not device_info_dict.__contains__("signature_md5"):
                            return self.response_json_error("signature_md5", "缺少参数signature_md5")
                        # 验证头部签名是否成功
                        client_head_dict = dict([(k, v[0]) for k, v in parse_qs(clientheaderinfo_string, True).items() if not k in no_check_array])
                        head_signature_md5 = self.get_signature_md5(client_head_dict, encrypt_key)
                        signature_md5 = device_info_dict["signature_md5"].lower()
                        if signature_md5 != head_signature_md5:
                            return self.response_json_error("signature_fail", "头部签名验证失败")
                    else:
                        return self.response_json_error("no_device_info", "没有提交设备信息")
                except Exception as ex:
                    self.logging_link_error("【头部校验异常】" + traceback.format_exc())
                    return self.response_json_error("error", "头部验证失败")

            return handler(self, **args)

        return wrapper

    return check_head


def filter_check_params_sign(is_check=True, no_check_params=None):
    """
    :description: 请求参数过滤装饰器 仅限handler使用
    :param is_check: 是否开启校验
    :param no_check_params: 不加入参数校验的参数集合
    :last_editors: HuangJianYi
    """
    def check_params(handler):
        def wrapper(self, **args):
            encrypt_key = config.get_value("encrypt_key", "r8C1JpyAXxrFV26V")
            client_encrypt_type = config.get_value("client_encrypt_type", 0)
            server_encrypt_type = config.get_value("server_encrypt_type", 0)
            if ("/server/" in self.request.uri and server_encrypt_type != 2) or ("/client/" in self.request.uri and client_encrypt_type != 2):
                is_check = False
            else:
                is_check = True
            if is_check == True:
                try:
                    if type(no_check_params) == str:
                        no_check_array = no_check_params.split(",")
                    elif type(no_check_params) == list:
                        no_check_array = no_check_params
                    else:
                        no_check_array = []
                    # 验证参数
                    request_param_dict = {}
                    try:
                        if self.request.method == "POST" and "Content-Type" in self.request.headers and self.request.headers["Content-type"].lower().find("application/json") >= 0 and self.request.body:
                            request_param_dict = json.loads(self.request.body)
                        else:
                            request_param_dict = dict([(k, v[0]) for k, v in parse_qs(self.request.query, True).items() if not k in no_check_array])
                    except:
                        pass
                    if not request_param_dict.__contains__("param_signature_md5"):
                        return self.response_json_error("signature_fail", "缺少参数param_signature_md5")
                    check_request_signature_md5 = self.get_signature_md5(request_param_dict, encrypt_key)
                    param_signature_md5 = request_param_dict["param_signature_md5"].lower()
                    if check_request_signature_md5 != param_signature_md5:
                        return self.response_json_error("signature_fail", "参数签名验证失败")

                except Exception as ex:
                    self.logging_link_error("【请求参数校验异常】" + traceback.format_exc())
                    return self.response_json_error("error", "请求参数验证失败")

            return handler(self, **args)

        return wrapper

    return check_params
