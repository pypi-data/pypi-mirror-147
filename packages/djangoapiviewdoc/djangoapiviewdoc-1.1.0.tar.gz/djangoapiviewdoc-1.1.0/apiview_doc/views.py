#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2021/12/14 13:26
    Desc  :
--------------------------------------
"""
from django.shortcuts import render

from apiview_doc.openapi import OpenApi, api_info_list

openapi = OpenApi(
    paths = api_info_list()
)


def get_openapi_docs_url(request):
    context = openapi.__dict__

    return render(request, 'apiview_doc/openapi/index.html', context)
