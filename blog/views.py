import re
import markdown
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView
from markdown.extensions.toc import TocExtension
from .models import Post, Category, Tag


class Index(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 5
    ordering = ['-created_time']


# def index(request):
#     if request.session.get('is_login', None):
#         print(333)
#         uid = request.session.get('uid')
#         # uid = int(uid)
#         post_list = Post.objects.filter(id=uid)
#         return render(request, 'blog/index.html', context={'post_list': post_list})
#     return redirect('more:login')


# 文章详情
def detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    # 每次请求了页面，让浏览次数加1
    post.increase_views()
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',  # 多种基础扩展
        'markdown.extensions.codehilite',  # 代码高亮
        # 'markdown.extensions.toc',  # 允许生成markdown目录
        TocExtension(slugify=slugify),  # 使用markdown中文锚点
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc
    # 这里我们正则表达式去匹配生成的目录中包裹在ul标签中的内容，如果不为空，说明目录，就把ul
    # 标签中的值提取出来（目的是只要包含目录内容的最核心部分，多余的HTML标签结构丢掉）赋值给post.toc；否则，将
    # post的toc置为空字符串，然后我们就可以在模板中通过判断post.toc是否为空，来决定是否显示侧栏目录：
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', {'post': post})


# 完善归档功能，使点击归档能够得到相应的文章列表, 日期归档
def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by(
        '-created_time')
    return render(request, 'blog/index.html', {'post_list': post_list})
    # 注意这里created_time是Python的date对象，其有一个year和month属性，我们在页面侧边栏：使用自定义模板标签使用过这个属性。Python中调用属性的方式通常是created_time.year，但是由于这里作为方法的参数列表，所以django要求我们把点替换成了两个下划线，即created_time__year。


# 完善归档功能，使点击归档能够得到相应的文章列表, 分类归档
def category(request, pk):
    cate = get_object_or_404(Category, id=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', {'post_list': post_list})


# 完善归档功能，使点击归档能够得到相应的文章列表, 标签归档
def tag(request, pk):
    t = get_object_or_404(Tag, id=pk)
    post_list = Post.objects.filter(tag=t).order_by('-created_time')
    return render(request, 'blog/index.html', {'post_list': post_list})


# 查找含有搜索关键词的文章
def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_msg='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {
        'post_list': post_list
    })
