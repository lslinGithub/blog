"""bs_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from bs_blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path(r'mdeditor/', include('mdeditor.urls')),
    path('comments/', include(('comments.urls', 'comments'), namespace='comments')),
    path('more/', include(('more.urls', 'more'), namespace='more')),
    path('captcha/', include('captcha.urls'))
]

# 配置上传文件路径url 我猜
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 自定义django-markdown编辑器功能
# MDEDITOR_CONFIGS = {
# 'default':{
#     'width': '90%',  # 自定义编辑框宽度
#     'heigth': 500,   # 自定义编辑框高度
#     'toolbar': ["undo", "redo", "|",
#                 "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
#                 "h1", "h2", "h3", "h5", "h6", "|",
#                 "list-ul", "list-ol", "hr", "|",
#                 "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
#                 "emoji", "html-entities", "pagebreak", "goto-line", "|",
#                 "help", "info",
#                 "||", "preview", "watch", "fullscreen"],  # 自定义编辑框工具栏
#     'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # 图片上传格式类型
#     'image_folder': 'editor',  # 图片保存文件夹名称
#     'theme': 'default',  # 编辑框主题 ，dark / default
#     'preview_theme': 'default',  # 预览区域主题， dark / default
#     'editor_theme': 'default',  # edit区域主题，pastel-on-dark / default
#     'toolbar_autofixed': True,  # 工具栏是否吸顶
#     'search_replace': True,  # 是否开启查找替换
#     'emoji': True,  # 是否开启表情功能
#     'tex': True,  # 是否开启 tex 图表功能
#     'flow_chart': True,  # 是否开启流程图功能
#     'sequence': True,  # 是否开启序列图功能
#     'watch': True,  # 实时预览
#     'lineWrapping': False,  # 自动换行
#     'lineNumbers': False  # 行号
#     }
# }
