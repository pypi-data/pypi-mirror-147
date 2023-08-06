#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2022/4/15 13:40
    Desc  :
--------------------------------------
"""
import json
from typing import Dict, List

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def get_open_api_info(paths: List[Dict]):
    return mark_safe(json.dumps(paths, ensure_ascii = False))


@register.simple_tag()
def get_path(request):
    print(request.path)
    return request.path


@register.simple_tag()
def get_dict_to_json(val):
    return json.dumps(val, ensure_ascii = False)


@register.simple_tag()
def get_content_by_path(path: str, paths: List[Dict]):
    for i in paths:
        for j in i.get('paths'):
            if j.get('path') == path:
                return mark_safe(json.dumps(j, ensure_ascii = False))
            break
