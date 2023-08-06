#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2022/4/21 16:03
    Desc  :
--------------------------------------
"""

from functools import wraps
from typing import List, Any, Dict

from django.conf import settings


class OpenApi:

    def __init__(self, title: str = None, version: str = None, status_code=None, paths=None):
        """

        @type content: object
        """
        self.title = title if title else getattr(settings, 'OPEN_API_TITLE') if hasattr(settings,
                                                                                        'OPEN_API_TITLE') else '接口文档'
        self.version = version if version else getattr(settings, 'OPEN_API_VERSION') if hasattr(settings,
                                                                                                'OPEN_API_VERSION') else 'V1.1.0'
        self.paths = paths
        self.status_code = status_code


API_INFO_DATA_LIST = {}


def get_api_info_by_class_name(class_name) -> dict:
    return API_INFO_DATA_LIST.get(class_name)


def update_api_info(class_name, api_info: dict):
    """更新global_api_doc"""
    if API_INFO_DATA_LIST.get(class_name):
        API_INFO_DATA_LIST[class_name].update(**api_info)
    else:
        API_INFO_DATA_LIST[class_name] = api_info


def get_class_name_by_func(func):
    """根据方法名类方法名获取类名"""
    qual_name = func.__qualname__
    if qual_name == '':
        raise ApiParamException(
            f"{func.__name__}不是类方法"
        )
    class_name = qual_name[:str(qual_name).find('.')]
    return class_name


def api_info_list():
    data = API_INFO_DATA_LIST.copy()
    docs = []
    tags = []
    if data:
        for i in data.keys():
            tag = data.get(i).get('tag')
            if tag and tag not in tags:
                tags.append(tag)
                docs.append({
                    'tag': tag
                })
        for i in data.keys():
            for j in docs:
                if data.get(i).get('tag') == j.get('tag'):
                    if j.get('paths'):
                        j['paths'].append({
                            'path': data.get(i).get('path'),
                            'method': data.get(i).get('method'),
                            'summary': data.get(i).get('summary'),
                            'parameters': data.get(i).get('parameters'),
                        })
                    else:
                        j['paths'] = [
                            {
                                'path': data.get(i).get('path'),
                                'method': data.get(i).get('method'),
                                'summary': data.get(i).get('summary'),
                                'parameters': data.get(i).get('parameters'),
                            }
                        ]

    return docs


class ApiDataType:
    String = 'String'
    Integer = 'Integer'
    Array = 'Array'
    Object = 'Object'
    Boolean = 'Boolean'


class ApiParamType:
    Query = 'query'
    Header = 'header'
    Body = 'body'
    Form = 'form'
    Path = 'path'


class ApiInfoObject:

    def __init__(self, tag=None, path=None, method=None, summary=None, parameters=None, response=None):
        self.tag = tag
        self.path = path
        self.method = method
        self.summary = summary
        self.parameters = parameters
        self.response = response


class ApiParamException(Exception):
    pass


class ApiInvalidTokenException(Exception):
    pass


class Tags:
    def __init__(self, name: str = None, description: str = None):
        self.name = name
        self.description = description


class ApiImplicitParam():

    def __init__(self, name: str, description: str, required: bool, paramType: str, dataType: Any,
                 defaultValue: Any = None):
        self.name = name
        self.description = description
        self.required = required
        self.paramType = paramType
        self.dataType = dataType
        self.defaultValue = defaultValue

    def filter_type(self):
        type_dict = {
            'String': 'str',
            'Integer': 'int',
            'Array': 'list',
            'Object': 'dict',
            'Boolean': 'bool'
        }
        return type_dict.get(self.dataType)

    def check(self, request):
        """
        参数校验
        """
        param = None
        if self.paramType == ApiParamType.Query:
            param = request.GET.get(self.name, None)
        if self.paramType == ApiParamType.Header:
            param = request.headers.copy().get(self.name, None)
        if self.paramType == ApiParamType.Path:
            param = request.query_params.copy().get(self.name, None)
        if self.paramType == ApiParamType.Body:
            param = request.data.copy().get(self.name, None)
        if self.paramType == ApiParamType.Form:
            param = request.form.copy().get(self.name, None)
        if param is None or len(param) == 0:
            raise ApiParamException(
                f'{self.description if self.description and len(self.description) != 0 else self.name}不能为空')
        if not isinstance(param, eval(self.filter_type())):
            raise ApiParamException(
                f'{self.description if self.description and len(self.description) != 0 else self.name}类型错误')


def ApiParameters(params: List[ApiImplicitParam]):
    def decorator(func):
        class_name = get_class_name_by_func(func)
        param_list_dict = []
        for i in params:
            param_list_dict.append(i.__dict__)
        apiInfo = get_api_info_by_class_name(class_name)
        if apiInfo is None:
            apiInfo = ApiInfoObject(parameters = param_list_dict).__dict__
        else:
            apiInfo['parameters'] = param_list_dict
        update_api_info(class_name, apiInfo)

        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            for i in params:
                if i.required:
                    i.check(request = request)
                return func(self, request, *args, **kwargs)

        return wrapper

    return decorator


def ApiTag(name: str, description: str):
    def decorator(func):
        class_name = get_class_name_by_func(func)
        apiInfo = get_api_info_by_class_name(class_name)
        tag = Tags(name = name, description = description).__dict__
        if apiInfo is None:
            apiInfo = ApiInfoObject(tag = tag).__dict__
        else:
            apiInfo['tag'] = tag
        update_api_info(class_name = class_name, api_info = apiInfo)

        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator


def ApiOperation(method: str, path: str, summary: str):
    def decorator(func):
        class_name = get_class_name_by_func(func)
        apiInfo = get_api_info_by_class_name(class_name)
        if apiInfo:
            apiInfo['method'] = method
            apiInfo['path'] = path
            apiInfo['summary'] = summary
        else:
            apiInfo = ApiInfoObject(method = method, path = path, summary = summary).__dict__
        update_api_info(class_name, apiInfo)

        @wraps(func)
        def wrapper(self, request, *args, **kwargs):

            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator


def ApiResponse(responseModel: List[Dict]):
    def decorator(func):
        class_name = get_class_name_by_func(func)
        apiInfo = get_api_info_by_class_name(class_name)
        if apiInfo:
            apiInfo['response'] = responseModel
        else:
            apiInfo = ApiInfoObject(response = responseModel).__dict__
        update_api_info(class_name, apiInfo)

        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator
