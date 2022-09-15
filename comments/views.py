from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from blog.models import Post

# Create your views here.
from .forms import CommentsForm


# 视图函数被 require_POST 装饰器装饰，从装饰器的名字就可以看出，
# 其作用是限制这个视图只能通过 POST 请求触发，因为创建评论需要用户通过表单提交的数据，
# 而提交表单通常都是限定为 POST 请求，这样更加安全。
@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    form = CommentsForm(request.POST)
    # 如果表单数据合法
    if form.is_valid():
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)
        # 将表单与文章关联起来
        comment.post = post
        comment.save()
        # 第一个是当评论成功，即评论数据成功保存到数据库后，因此在comment视图中加一句     。
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        return redirect('blog:detail', post.id)
    # 表单不合法，我们也渲染一个页面给用户
    context = {
        'post': post,
        'form': form
    }
    # 评论未成功，我们也发送一个消息给用户
    messages.add_message(request, messages.ERROR, '请确认表单内容是否有误？', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)
