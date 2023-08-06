# djangoapiviewdoc

### 根据装饰器生成api文档

#### 版本<=1.1.0

```python
# settings.py
from apiview_doc.decorator import ApiDoc

APIDOC_DECORATOR = ApiDoc()

# views.py
from project_name.settings import APIDOC_DECORATOR
from rest_framework.generics import GenericAPIView


class PersonLoginAPIView(GenericAPIView):
    """
    @author:    JiChao_Song
    @desc:      用户名、密码登录
    @date:      2021/11/29 17:09
    """

    @APIDOC_DECORATOR.start
    @APIDOC_DECORATOR.ApiTag(value = 'user', desc = '用户管理')
    @APIDOC_DECORATOR.ApiOperation(method = 'POST', path = '/user/login', summary = '用户登录')
    @APIDOC_DECORATOR.ApiParams(value = 'username', require = True, type = 'string', desc = '用户名')
    @APIDOC_DECORATOR.ApiParams(value = 'password', require = True, type = 'string', desc = '密码')
    def post(self, request, *args, **kwargs):
        pass


# url.py
from apiview_doc.decorator import api_doc
from views import PersonLoginAPIView


def docs(request):
    context = api_doc()

    return render(request, 'apiview_doc/docs/index.html', context)


urlpatterns = [
    path('login', PersonLoginAPIView.as_view()),
    path('docs', docs),
]

```

### 启动项目访问 “/docs”

![img.png](img.png)

#### 版本 >= 1.1.0

```python
# settings.py
from apiview_doc.decorator import ApiDoc
from apiview_doc.openapi import ApiImplicitParam, ApiTag, ApiParameters, ApiOperation, ApiDataType, ApiParamType

# views.py
from rest_framework.generics import GenericAPIView


class PersonLoginAPIView(GenericAPIView):
    """
    @author:    JiChao_Song
    @desc:      用户名、密码登录
    @date:      2021/11/29 17:09
    """

    @ApiTag(name = 'user', description = '用户管理')
    @ApiOperation(method = 'POST', path = 'user/login', summary = '用户登录')
    @ApiParameters(params = [
        ApiImplicitParam(description = '用户名', name = 'username', required = True, paramType = ApiParamType.Body,
                         dataType = ApiDataType.String),
        ApiImplicitParam(description = '密码', name = 'password', required = True, paramType = ApiParamType.Body,
                         dataType = ApiDataType.String),
    ])
    def post(self, request, *args, **kwargs):
        pass


# url.py
from views import PersonLoginAPIView
from apiview_doc.openapi import OpenApi, api_info_list

openapi = OpenApi(
    paths = api_info_list()
)


def get_openapi_docs_url(request):
    context = openapi.__dict__

    return render(request, 'apiview_doc/openapi/index.html', context)

urlpatterns = [
    path('login', PersonLoginAPIView.as_view()),
    path('redocs', get_openapi_docs_url),
]

```
### 启动项目访问 “/docs”
![img_3.png](img_3.png)